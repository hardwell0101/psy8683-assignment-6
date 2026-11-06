"""File evidence for the presentation checks. All times are in seconds."""
from bisect import bisect_left
from collections import Counter, defaultdict
import math
from pathlib import Path
import re


class Missing(Exception):
    """The file lacks a measurement needed for this part of the spec."""


def cell(row, *names):
    for name in names:
        if name in row:
            vals = set(row[name])
            if len(vals) > 1:
                raise ValueError(f"conflicting duplicate {name}: {sorted(vals)}")
            return next(iter(vals))
    raise Missing("need " + " or ".join(names))


def number(value):
    x = float(value)
    if not math.isfinite(x):
        raise ValueError(f"nonfinite number {value!r}")
    return x


def count(value):
    x = number(value)
    if x < 0 or not x.is_integer():
        raise ValueError(f"expected nonnegative count, got {value!r}")
    return int(x)


# Choose component flip stamps, never substitute routine wall-clock starts/stops.
ROLES = {
    "fix": ("fixation", "fix", "fixationCross", "fix_text", "fixText"),
    "prime": ("prime_text", "primeText", "primeStim", "prime"),
    "target": ("target_text", "targetText", "targetStim", "target"),
    "key": ("decision", "key_resp", "response", "resp", "respKeys"),
    "feedback": ("feedbackText", "feedback_text", "feedbackStim"),
    "iti": ("blankScreen", "itiText", "iti_blank", "blank", "blank_iti"),
    "end": ("endText", "end_text", "endMsg", "end_screen"),
    "instructions": ("instructionText", "instructions_text", "instrText", "instr_text_stim"),
    "break": ("breakText", "break_text", "breakScreen", "break"),
}
NULL_KEYS = ("", "None", "[]")
EPS = 0.00001


def component(row, role, suffix):
    return cell(row, *(name + "." + suffix for name in ROLES[role]))


def stamp(row, role, edge="started"):
    value = component(row, role, edge)
    if not value:
        raise Missing(f"need {role}.{edge} flip stamp on this row")
    return number(value)


class Findings:
    def __init__(self):
        self.parts = defaultdict(lambda: defaultdict(list))

    def add(self, prop, part, verdict, evidence):
        self.parts[prop, part][verdict].append(evidence)

    def check(self, prop, part, line, fn):
        try:
            ok, evidence = fn()
            verdict = "PASS" if ok else "FAIL"
        except Missing as e:
            verdict, evidence = "UNDETERMINED", str(e)
        except (ValueError, TypeError, OverflowError) as e:
            verdict, evidence = "FAIL", str(e)
        self.add(prop, part, verdict, f"line {line}: {evidence}")

    def lines(self):
        for (prop, part), groups in self.parts.items():
            verdict = next(v for v in ("FAIL","UNDETERMINED","PILOT","PASS") if v in groups)
            counts = ", ".join(f"{len(examples)} {v.lower()}" for v, examples in groups.items())
            yield prop, verdict, f"{part} [{counts}]: {groups[verdict][0]}"


def near(actual, desired, tolerance=EPS):
    return abs(actual-desired) <= tolerance, f"{actual:.6f}s vs {desired:.6f}s"


def same(actual, expected):
    return actual == expected, f"{actual!r} vs {expected!r}"


def hz_for(output):
    rates = {round(number(cell(r, "frameRate"))) for _, r in output.records
             if cell(r, "frameRate")}
    if len(rates) != 1 or min(rates) < 1:
        raise ValueError(f"expected one positive rounded display rate, got {rates}")
    return rates.pop()


def target_off(row):
    # Builder can queue the offset only for a timeout. On a response the next
    # feedback or ITI stimulus replaces the target on its first display flip.
    try:
        return stamp(row, "target", "stopped")
    except Missing:
        return stamp(row, "feedback" if cell(row, "phase") == "practice" else "iti")


def fixed_timing(start, stop, expected_frames, hz, flips=None, drops=0):
    measured = (stop-start)*hz
    if stop < start:
        return False, "offset precedes onset"
    if flips:
        indices = []
        for t in (start, stop):
            i = bisect_left(flips, t-EPS)
            if i == len(flips) or abs(flips[i]-t) > EPS:
                break
            indices.append(i)
        if len(indices) == 2:
            actual = indices[1] - indices[0]
            return actual == expected_frames, (f"{actual} logged flip intervals, "
                f"{measured:.2f} elapsed frames, expected {expected_frames}")
    if drops and measured > expected_frames + 0.5:
        raise Missing(f"{measured:.2f} elapsed frames vs {expected_frames} requested, "
                      f"{drops} long interval(s) on trial; need event-aligned flip log to locate them")
    return round(measured) == expected_frames, (f"{measured:.2f} elapsed frames, "
        f"expected {expected_frames}; elapsed estimate at rounded Hz")


def check_logs(output, path, hz, findings, required):
    """Return per-trial flip times only when the entire slice can be verified."""
    path = Path(path)
    log = path.with_name(path.stem + "_frameIntervals.log")
    rows = output.trials
    with_counts = any("dropped_frames" in r for _, r in rows)
    available = log.is_file()
    if not available:
        findings.add("I1", "interval log", "FAIL" if required or with_counts else "UNDETERMINED",
                     f"need matching {log.name}")
    drops = None
    try:
        if not rows:
            raise ValueError("no trials")
        drops = [count(cell(r, "dropped_frames")) for _, r in rows]
        if any(any(r.get("dropped_frames", [])) for line, r in output.records
               if line not in {line for line, _ in rows}):
            raise ValueError("dropped_frames populated outside trials")
        if not available:
            raise Missing("need interval log for comparison")
    except (Missing, ValueError) as e:
        findings.add("I2", "per-trial counts", "FAIL" if required or isinstance(e, ValueError)
                     or (available and not with_counts) else "UNDETERMINED", str(e))
        drops = None
    if not available:
        return {}
    try:
        values = [number(s) for s in re.split(r"[,\s]+", log.read_text().strip()) if s]
        if not values or any(d <= 0 for d in values):
            raise ValueError("expected positive flip intervals in seconds")
    except (OSError, ValueError) as e:
        findings.add("I1", "read intervals", "FAIL", str(e))
        findings.add("I2", "log agreement", "UNDETERMINED", "need a valid interval log")
        return {}
    observed = sum(x > 1.5/hz for x in values)
    if drops is not None:
        findings.add("I2", "whole-run agreement", "PASS" if observed == sum(drops) else "FAIL",
                     f"CSV {sum(drops)}, log {observed} above {1.5/hz:.8f}s")
    # Fall back to the assignment's approximate total when a different build
    # records only the required columns.
    try:
        expected = sum(target_off(r)-stamp(r, "fix")-1/hz for _, r in rows)
        error = sum(values)-expected
        # Each unobserved final display interval can introduce a timing error.
        findings.add("I1", "approximate window coverage",
                     "PASS" if abs(error) <= len(rows)*0.5/hz else "FAIL",
                     f"log {sum(values):.6f}s, display spans less one frame/trial "
                     f"{expected:.6f}s, difference {error:.6f}s")
    except (Missing, ValueError) as e:
        findings.add("I1", "approximate window coverage", "UNDETERMINED", str(e))
    offset, segments = 0, {}
    for idx, (line, row) in enumerate(rows):
        try:
            n = count(cell(row, "recorded_intervals"))
            if n < 1 or offset+n > len(values):
                raise ValueError("invalid trial slice length")
            segment = values[offset:offset+n]
            offset += n
            first = stamp(row, "fix")
            flips = [first]
            for interval in segment:
                flips.append(flips[-1]+interval)
            actual_last = number(cell(row, "trial_last_flip"))
            ok, message = near(flips[-1], actual_last)
            findings.add("I1", "trial slice endpoints", "PASS" if ok else "FAIL",
                         f"line {line}: {message}")
            if ok:
                segments[line] = flips
            if drops is not None:
                findings.check("I2", "trial slice count", line,
                    lambda: same(sum(x > 1.5/hz for x in segment), drops[idx]))
        except Missing as e:
            findings.add("I1", "exact per-trial log boundary", "UNDETERMINED", str(e))
            return {}
        except ValueError as e:
            findings.add("I1", "trial slice", "FAIL", f"line {line}: {e}")
            return {}
    findings.add("I1", "all intervals allocated", "PASS" if offset == len(values) else "FAIL",
                 f"{offset} in trial slices, {len(values)} in log")
    return segments


def inspect_file(output, path, q1, require_log=False):
    f = Findings()
    try:
        hz = hz_for(output)
    except (Missing, ValueError) as e:
        hz = None
        f.add("Q5", "display rate", "UNDETERMINED" if isinstance(e, Missing) else "FAIL", str(e))
    segments = check_logs(output, path, hz, f, require_log) if hz else {}
    if output.records:
        header = output.records[0][1]
        for prop, fields in {"Q8":("prime_shown","target_shown"),
                             "Q9":("prime_onset","target_onset"),
                             "Q10":("key","rt","accuracy","timeout")}.items():
            absent = [name for name in fields if name not in header]
            if absent:
                f.add(prop, "required output columns", "FAIL", ", ".join(absent)+" missing")
    phases = [cell(r, "phase") for _, r in output.trials]
    sequence_ok = phases == ["practice"]*8 + ["experimental"]*96
    f.add("Q3", "phase counts and order", "PASS" if sequence_ok else "FAIL", str(dict(Counter(phases))))

    types = []
    previous_iti_stop = None
    trials = {line for line, _ in output.trials}
    for line, row in output.records:
        if line in trials:
            types.append(cell(row, "phase"))
            if previous_iti_stop is not None:
                f.check("Q4", "next fixation after ITI", line,
                        lambda: near(stamp(row,"fix"), previous_iti_stop))
            try:
                previous_iti_stop = stamp(row,"iti","stopped")
            except (Missing,ValueError):
                previous_iti_stop = None
            continue
        for role in ("instructions", "break", "end"):
            try:
                stamp(row, role)
            except Missing:
                continue
            except ValueError as e:
                f.add("Q3", "nontrial screen stamp", "FAIL", f"line {line}: {e}")
                continue
            types.append(role)
            if previous_iti_stop is not None:
                f.check("Q3","screen follows last ITI",line,lambda: near(stamp(row,role),previous_iti_stop))
            previous_iti_stop = None
            if role == "end" and hz:
                for prop in ("Q3", "Q5"):
                    f.check(prop, "end screen duration", line, lambda: fixed_timing(
                        stamp(row, "end"), stamp(row, "end", "stopped"), round(2*hz), hz))
            elif role in ("instructions", "break"):
                keys = ("beginKey.keys", "instr_key.keys", "instr_resp.keys") if role == "instructions" else (
                        "resumeKey.keys", "break_key.keys", "break_resp.keys")
                f.check("Q3", role+" SPACE response", line, lambda: same(cell(row, *keys), "space"))
            break
        else:
            types.append("unidentified")
    wanted = ["instructions"]+["practice"]*8+["break"]+["experimental"]*96+["end"]
    if not any("end" == k for k in types):
        f.add("Q5","end screen duration","UNDETERMINED","need the end stimulus flip stamps")
    if all(k in types for k in ("instructions", "break", "end")):
        f.add("Q3", "screen order", "PASS" if types == wanted else "FAIL", "row sequence compared with specification")
    else:
        f.add("Q3", "screen order", "UNDETERMINED", "need identifiable instruction, break and end screen stamps")

    for line, r in output.trials:
        def check(prop, label, fn):
            f.check(prop, label, line, fn)

        def fixed(label, start, end, seconds, logged=True, prop="Q4"):
            if hz:
                result = lambda: fixed_timing(start(), end(), round(seconds*hz), hz,
                                               segments.get(line) if logged else None, drops if logged else 0)
                check(prop, label, result)
                check("Q5", label+" frame count", result)

        try:
            drops = count(cell(r, "dropped_frames"))
        except (Missing, ValueError):
            drops = 0  # I2 reports any missing or malformed counter.
        practice = cell(r, "phase") == "practice"
        if practice:
            fixed("practice feedback", lambda: stamp(r, "feedback"), lambda: stamp(r, "feedback","stopped"), 1, False, "Q3")
        else:
            def no_feedback():
                start = component(r, "feedback", "started")
                return same(start, "")
            check("Q3", "no main feedback", no_feedback)
        fixed("fixation", lambda: stamp(r, "fix"), lambda: stamp(r, "fix","stopped"), .5)
        fixed("prime", lambda: stamp(r, "prime"), lambda: stamp(r, "prime","stopped"), .15)
        if hz:
            check("Q4", "SOA", lambda: fixed_timing(stamp(r,"prime"),stamp(r,"target"),
                  round(number(cell(r,"soa"))*hz/1000),hz,segments.get(line),drops))
            check("Q5", "SOA frames", lambda: fixed_timing(stamp(r,"prime"),stamp(r,"target"),
                  round(number(cell(r,"soa"))*hz/1000),hz,segments.get(line),drops))
        fixed("ITI", lambda: stamp(r, "iti"), lambda: stamp(r, "iti","stopped"), .5, False)
        check("Q4","fixation to prime transition",lambda: near(stamp(r,"fix","stopped"),stamp(r,"prime")))
        if hz:
            def blank_gap():
                frames = round(number(cell(r,"soa"))*hz/1000) - round(.15*hz)
                return fixed_timing(stamp(r,"prime","stopped"),stamp(r,"target"),
                                    frames,hz,segments.get(line),drops)
            check("Q4","blank interval from prime offset to target",blank_gap)
        for role, transform in (("prime", str.lower), ("target", str.upper)):
            def shown():
                return same(cell(r,role+"_shown"),transform(cell(r,role)))
            check("Q4",role+" recorded content",shown)
            check("Q8",role+" shown vs list",shown)
        # Feedback wording is observable only if the build logged it.
        if practice and any(k in r for k in ("feedback_shown", "feedback_message", "feedbackShown")):
            check("Q3", "feedback wording", lambda: same(
                cell(r,"feedback_shown","feedback_message","feedbackShown"),
                "Too slow" if count(cell(r,"timeout")) else
                "Correct" if count(cell(r,"accuracy")) else "Incorrect"))
        if practice:
            check("Q3", "feedback directly precedes ITI", lambda: near(
                stamp(r,"feedback","stopped"),stamp(r,"iti")))
        check("Q6","accepted recorded key",lambda: (cell(r,"key") in ("","f","j"),repr(cell(r,"key"))))
        def score():
            key, cat = cell(r,"key"), cell(r,"correct_response")
            if cat not in ("word","nonword"):
                raise ValueError(f"unknown category {cat!r}")
            pid = output.known_participant or count(cell(r,"participant"))
            correct_key = "f" if (pid % 2 == 1) == (cat == "word") else "j"
            return same(count(cell(r,"accuracy")),int(key == correct_key))
        check("Q10","accuracy under participant mapping",score)
        check("Q7","keyboard starts on target flip",lambda: near(stamp(r,"key"),stamp(r,"target")))
        for role in ("prime","target"):
            check("Q9",role+" onset vs component flip",lambda: near(number(cell(r,role+"_onset")),stamp(r,role)))
        def encoding():
            key, rt, timeout = cell(r,"key"), cell(r,"rt"), count(cell(r,"timeout"))
            if key in ("f","j"):
                ok = timeout == 0 and 0 <= number(rt) <= 2
            else:
                ok = key == "" and rt == "" and timeout == 1 and count(cell(r,"accuracy")) == 0
            return ok, f"key={key!r}, rt={rt!r}, timeout={timeout}"
        check("Q10","response fields and two-second limit",encoding)
        def raw_response():
            key, rt = cell(r,"key"), cell(r,"rt")
            rawkey = component(r,"key","keys")
            if not key:
                rawrt = component(r,"key","rt")
                return rawkey in NULL_KEYS and rawrt in NULL_KEYS and not rt, f"timeout vs automatic key {rawkey!r}"
            ok, message = near(number(rt),number(component(r,"key","rt")))
            return ok and key == rawkey, message+f", key {key!r} vs {rawkey!r}"
        check("Q7","saved response vs automatic key and RT",raw_response)
        if hz:
            def response_window():
                start = stamp(r,"target")
                duration = target_off(r)-start
                if count(cell(r,"timeout")) == 1:
                    # The final boundary flip is excluded from I1. Add it
                    # to count actual display intervals for the timeout.
                    flips = segments.get(line)
                    if flips and target_off(r) > flips[-1] + EPS:
                        flips = flips + [target_off(r)]
                    return fixed_timing(start, start+duration, round(2*hz), hz, flips, drops)
                key_time = stamp(r,"key") + number(component(r,"key","rt"))
                lag = target_off(r)-key_time
                if lag > 2/hz+EPS and drops:
                    raise Missing(f"replacement lag {lag:.5f}s on trial with a long flip interval; need polling and offset evidence")
                if lag < -EPS or lag > 3/hz:
                    return False, f"replacement flip minus recorded key time = {lag:.5f}s"
                if lag > 2/hz+EPS:
                    raise Missing(f"replacement {lag*hz:.2f} refresh periods after key; "
                                  "need key polling time and flip intervals to attribute delay")
                return True, f"replacement flip {lag:.5f}s after keyboard event"
            check("Q4","target removed on response or deadline",response_window)
            if r.get("timeout") in (["1"], ["1.0"]):
                def deadline():
                    elapsed = stamp(r,"key","stopped")-stamp(r,"target")
                    # A late offset with actual frame loss can reflect display
                    # timing; the queue and the acceptance rule are distinct.
                    if elapsed < 2-.5/hz:
                        return False, f"keyboard closed {elapsed:.5f}s after target"
                    return True, f"keyboard covered deadline, stopped at {elapsed:.5f}s"
                check("Q10","keyboard available through target deadline",deadline)
    if output.trials and not any(cell(r, "timeout") == "1" for _, r in output.trials if "timeout" in r):
        f.add("Q10","timeout case","UNDETERMINED","need a trial without a response through the deadline")
    f.add("Q10","ten unmodified trial-list fields",*q1)
    for prop, need in {
        "Q1":"dialog and relative filename in the build",
        "Q3":"instruction wording, feedback messages and SPACE-only gates in the build",
        "Q4":"fixation glyph and contents of blank screens in the build",
        "Q5":"frame scheduling rule across refresh rates in the build",
        "Q6":"key mapping in instructions, ignored inputs and Escape handling in the build or a pilot",
        "Q7":"first-key selection, event clearing and clock-reset implementation",
        "Q8":"build code reading from stimulus objects",
        "Q9":"independent light sensor aligned to flip time for physical display onset"
    }.items():
        f.add(prop,"further evidence", "UNDETERMINED", "need "+need)
    return f
