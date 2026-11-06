"""Print the frame-count table and every exception for an instrumented run."""
import argparse
from collections import Counter, defaultdict
import math
from pathlib import Path

from a6_checks import cell, count, hz_for, number, stamp
from check_output import read_output


def audit(path):
    output = read_output(path)
    hz = hz_for(output)
    log = path.with_name(path.stem+"_frameIntervals.log")
    values = [number(x) for x in log.read_text().strip().split(",")]
    if not all(t > 0 for t in values):
        raise ValueError("invalid interval")
    counts, exceptions = defaultdict(Counter), []
    offset = 0
    total_drops = 0
    drop_locations = Counter()
    ending_on_target = 0

    def event(label, first, last, desired, line, row, intervals=(), inside=False):
        measured = (last-first)*hz
        counts[(label,desired)][round(measured)] += 1
        if round(measured) == desired:
            return
        if inside:
            local = [(end-start)*1000 for start,end in intervals
                     if start >= first-1e-5 and end <= last+1e-5 and end-start > 1.5/hz]
            explanation = (f"within-event long intervals (ms): {[round(x,3) for x in local]}; "
                           f"trial drops={cell(row,'dropped_frames')}")
        else:
            trial_drops = cell(row, "dropped_frames")
            same_trial = f"trial drops={trial_drops}" if trial_drops else "nontrial row"
            explanation = f"{same_trial}; outside the recording window; the log cannot identify a cause"
        exceptions.append(f"line {line} {label}: {measured:.3f} elapsed vs {desired} planned frames; {explanation}")

    for line,row in output.trials:
        first = stamp(row,"fix")
        n = count(cell(row,"recorded_intervals"))
        segment = values[offset:offset+n]
        offset += n
        end = number(cell(row,"trial_last_flip"))
        drops = sum(x > 1.5/hz for x in segment)
        if len(segment) != n or not math.isclose(first+sum(segment),end,abs_tol=1e-5,rel_tol=0):
            raise ValueError(f"line {line}: frame-log slice/span mismatch")
        if drops != count(cell(row,"dropped_frames")):
            raise ValueError(f"line {line}: drop count mismatch")
        total_drops += drops
        bounds = [first]
        for d in segment:
            bounds.append(bounds[-1]+d)
        pairs = list(zip(bounds,bounds[1:]))
        soa = count(cell(row,"soa"))
        prime = stamp(row, "prime")
        prime_off = stamp(row, "prime", "stopped")
        target = stamp(row, "target")
        prime_frames = round(.15 * hz)
        soa_frames = round(soa * hz / 1000)
        event("fixation", first, stamp(row, "fix", "stopped"), round(.5 * hz), line, row, pairs, True)
        event("prime", prime, prime_off, prime_frames, line, row, pairs, True)
        event(f"SOA {soa}", prime, target, soa_frames, line, row, pairs, True)
        event(f"blank, SOA {soa}", prime_off, target, soa_frames - prime_frames, line, row, pairs, True)
        for onset, removal in pairs:
            if removal - onset <= 1.5 / hz:
                continue
            # The image at the beginning of an interval remains up until its ending flip.
            if removal <= prime + 1e-5:
                stage = "fixation"
            elif removal <= prime_off + 1e-5:
                stage = "prime"
            elif removal <= target + 1e-5:
                stage = "blank"
            else:
                stage = "target"
            drop_locations[stage] += 1
            if abs(removal - target) <= 1e-5:
                ending_on_target += 1
        event("ITI",stamp(row,"iti"),stamp(row,"iti","stopped"),round(.5*hz),line,row)
        if cell(row,"phase") == "practice":
            event("feedback",stamp(row,"feedback"),stamp(row,"feedback","stopped"),hz,line,row)
    for line,row in output.records:
        if any(row.get("endText.started",[])):
            event("end screen",stamp(row,"end"),stamp(row,"end","stopped"),2*hz,line,row)
    if offset != len(values) or total_drops != sum(x > 1.5/hz for x in values):
        raise ValueError("whole-run log/count mismatch")
    print(path)
    print(f"rounded rate = {hz} Hz; {len(output.trials)} trials; {len(values)} intervals; "
          f"{total_drops} drops; longest = {max(values)*1000:.4f} ms")
    for (label,desired),hist in counts.items():
        print(f"{label}: expected {desired}; achieved frames x frequency {dict(sorted(hist.items()))}")
    if sum(drop_locations.values()) != total_drops:
        raise ValueError("event locations do not reconcile with total drops")
    print(f"long intervals by image held: {dict(drop_locations)}; ending on target onset: {ending_on_target}")
    for entry in exceptions:
        print(entry)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files",type=Path,nargs="+")
    for name in parser.parse_args().files:
        audit(name)
