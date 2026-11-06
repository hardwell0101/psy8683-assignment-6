"""Check lexical-decision output against Q1-Q10 and the frame log against I1-I2.

python check_output.py data/3_ldt_*.csv --participant 3
python check_output.py provided/output_files/*.csv --lists provided/canonical_trial_lists

--participant supplies an independently known run ID when one is available.
For anonymized files the recorded participant fields are the only ID evidence.
Q3-Q10 and I1-I2 report each observable part separately. Use --require-log
for new instrumented runs, and --build to include a documented build inspection.
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

FIELDS = ("participant", "phase", "trial_index", "item_id", "target", "prime",
          "relatedness", "soa", "correct_response", "seed")
ORDER = ("phase", "trial_index", "item_id")
TRIAL_MARKERS = FIELDS[1:-1] + ("prime_shown", "target_shown", "prime_onset", "target_onset")



def integer(value):
    try:
        number = Decimal(value)
        if number.is_finite() and number == number.to_integral_value():
            return str(int(number))
    except InvalidOperation:
        pass
    raise ValueError(f"invalid integer {value!r}")


@dataclass
class Output:
    # Each dictionary value retains *all* cells with that header, in file order.
    records: list
    trials: list
    known_participant: int | None = None


def read_output(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.reader(stream, strict=True)
        header = next(reader, [])
        missing = set(FIELDS) - set(header)
        if missing:
            raise ValueError("missing input columns: " + ", ".join(sorted(missing)))
        records, trials = [], []
        for cells in reader:
            if not any(cells):
                continue
            line = reader.line_num
            if len(cells) != len(header):
                raise ValueError(f"line {line}: {len(cells)} cells for {len(header)} headers")
            row = {}
            for field, value in zip(header, cells):
                row.setdefault(field, []).append(value)
            records.append((line, row))
            if any(any(row.get(field, [])) for field in TRIAL_MARKERS):
                trials.append((line, row))
        return Output(records, trials)


def reference(output, lists_dir):
    # Prefer an independently supplied ID, then a single ID on nontrial rows.
    # Never silently pick one of two disagreeing participant columns.
    trial_lines = {line for line, _ in output.trials}
    all_ids, nontrial_ids = set(), set()
    for line, row in output.records:
        ids = {integer(v) for v in row["participant"] if v}
        all_ids.update(ids)
        if line not in trial_lines:
            nontrial_ids.update(ids)
    if output.known_participant is not None:
        pid = str(output.known_participant)
    elif len(nontrial_ids) == 1:
        pid = next(iter(nontrial_ids))
    elif len(all_ids) == 1:
        pid = next(iter(all_ids))
    else:
        raise ValueError(f"cannot identify one expected participant from {sorted(all_ids)}")
    path = Path(lists_dir) / f"trials_p{int(pid):02d}.csv"
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ValueError(f"{path.name}: unexpected input-list header")
        expected = list(reader)
    if not expected or any(integer(r["participant"]) != pid for r in expected):
        raise ValueError(f"{path.name}: missing rows or inconsistent participant ID")
    return path, expected, pid


def row_values(row, fields):
    values = []
    for field in fields:
        cells = {v for v in row[field] if v != ""}
        if field in ("participant", "trial_index", "soa", "seed"):
            cells = {integer(v) for v in cells}
        if len(cells) != 1:
            raise ValueError(f"{field}: expected one value, found {sorted(cells)}")
        values.append(cells.pop())
    return tuple(values)


def check_q1(output, lists_dir):
    """Each recorded trial must belong to the indicated participant's input."""
    try:
        path, expected, pid = reference(output, lists_dir)
        known = {tuple(r[f] for f in FIELDS) for r in expected}
        if not output.trials:
            raise ValueError("no trial records")
        for line, row in output.records:
            for v in row["participant"]:
                if v and integer(v) != pid:
                    raise ValueError(f"line {line}: participant {v!r} disagrees with {path.name}")
        bad = []
        for line, row in output.trials:
            try:
                values = row_values(row, FIELDS)
                if values not in known:
                    bad.append(f"line {line}: {values[1:4]} does not match all input fields")
            except ValueError as e:
                bad.append(f"line {line}: {e}")
        if bad:
            raise ValueError(f"{path.name}: {len(bad)} unmatched trial records; {bad[0]}")
        result = ("PASS", f"All {len(output.trials)} recorded trials match rows "
                          f"of {path.name} on all ten input fields.")
    except (ValueError, OSError) as e:
        result = ("FAIL", str(e))
    return result


def check_q2(output, lists_dir):
    """Check multiplicity and order using the labeled identity of every row."""
    try:
        path, expected, _ = reference(output, lists_dir)
        wanted = [tuple(r[f] for f in ORDER) for r in expected]
        actual = []
        for line, row in output.trials:
            try:
                actual.append(row_values(row, ORDER))
            except ValueError as e:
                raise ValueError(f"line {line}: {e}") from e
        if actual == wanted:
            return "PASS", (f"{len(actual)}/{len(wanted)} trial identities from {path.name} "
                            "in exact file order (phase, trial_index, item_id).")
        missing = sum((Counter(wanted) - Counter(actual)).values())
        extra = sum((Counter(actual) - Counter(wanted)).values())
        i = next((i for i in range(min(len(wanted), len(actual))) if wanted[i] != actual[i]),
                 min(len(wanted), len(actual)))
        observed = actual[i] if i < len(actual) else "end of output"
        expected_id = wanted[i] if i < len(wanted) else "end of list"
        return "FAIL", (f"{path.name}: {len(actual)} recorded, {len(wanted)} expected; "
                        f"{missing} missing, {extra} excess. First difference at trial "
                        f"{i+1}: expected {expected_id}, observed {observed}.")
    except (ValueError, OSError) as e:
        return "FAIL", str(e)


def main():
    from a6_checks import inspect_file, Missing
    import hashlib
    import json

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+")
    parser.add_argument("--lists", default="trial_lists")
    parser.add_argument("--participant", type=int, help="independently known run ID")
    parser.add_argument("--require-log", action="store_true", help="I1 and I2 are required for this run")
    parser.add_argument("--build", type=Path, help="known source for these files, to attach its manual inspection")
    args = parser.parse_args()
    review = {}
    if args.build:
        digest = hashlib.sha256(args.build.read_bytes()).hexdigest()
        reviews = json.loads((Path(__file__).parent/"evidence"/"build_inspections.json").read_text())
        review = next((r for r in reviews if digest in r["sha256"]), {})
    failed = False
    for path in args.files:
        print(path)
        try:
            output = read_output(path)
            output.known_participant = args.participant
            q1 = check_q1(output, args.lists)
            findings = inspect_file(output, path, q1, args.require_log)
            results = [("Q1", *q1), ("Q2", *check_q2(output, args.lists))]
            for prop, verdict, evidence in findings.lines():
                if verdict == "UNDETERMINED" and evidence.startswith("further evidence") and prop in review.get("settled", {}):
                    verdict, evidence = "PILOT", review["settled"][prop]
                results.append((prop, verdict, evidence))
            results.extend(tuple(item) for item in review.get("diagnostics", []))
        except (ValueError, OSError, csv.Error, Missing) as error:
            results = [(prop, "FAIL" if prop == "Q1" else "UNDETERMINED",
                        f"cannot read complete trial records: {error}")
                       for prop in [*(f"Q{i}" for i in range(1,11)), "I1", "I2"]]
        for prop, verdict, evidence in results:
            print(f"  {prop} {verdict} {evidence}")
            failed |= verdict == "FAIL"
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
