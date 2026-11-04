"""Output checker for PSY 8683 Assignment 5.

Checks a PsychoPy output file against the trial list it should have used and
against the presentation specification Q1-Q10 (see README.md).

    uv run python check_output.py data/3_ldt_*.csv
    uv run python check_output.py provided/output_files/file_A.csv --lists provided/canonical_trial_lists

For every property, report a verdict and the evidence behind it:

    PASS   the check could have failed and did not
    FAIL   the check failed; say where
    PILOT  the property cannot be observed in the output file; say how you
           established it instead

A check that cannot fail is not evidence. Write each check so that you can
say what output would have made it fail.

Each check_qN returns (verdict, evidence). When a property has a part you can
observe in the file and a part you cannot, return a list of (verdict,
evidence) pairs instead, one per part.

You may write this yourself, generate it, or any mixture. Record which in
build_log.md. Keep the function names below; add any others you like.
"""
import argparse


def read_output(path):
    """Read one PsychoPy output file. Look at the raw file before you decide
    how. Part D asks you to predict what you will find."""
    raise NotImplementedError


def check_q1(output, lists_dir):
    """The run used trial_lists/trials_pNN.csv for the participant entered."""
    raise NotImplementedError


def check_q2(output, lists_dir):
    """Every row ran exactly once, in file order."""
    raise NotImplementedError


def check_q3(output, lists_dir):
    """Sequence of events."""
    raise NotImplementedError


def check_q4(output, lists_dir):
    """One trial: durations and the prime-to-target interval."""
    raise NotImplementedError


def check_q5(output, lists_dir):
    """Durations in whole frames at the measured rate."""
    raise NotImplementedError


def check_q6(output, lists_dir):
    """Keys and the participant's mapping."""
    raise NotImplementedError


def check_q7(output, lists_dir):
    """rt is measured from target onset."""
    raise NotImplementedError


def check_q8(output, lists_dir):
    """prime_shown and target_shown are what was on the screen."""
    raise NotImplementedError


def check_q9(output, lists_dir):
    """prime_onset and target_onset."""
    raise NotImplementedError


def check_q10(output, lists_dir):
    """key, rt, accuracy, timeout, and the ten trial-list columns."""
    raise NotImplementedError


CHECKS = [check_q1, check_q2, check_q3, check_q4, check_q5,
          check_q6, check_q7, check_q8, check_q9, check_q10]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--lists", default="trial_lists")
    args = ap.parse_args()
    for path in args.files:
        output = read_output(path)
        print("=" * 72)
        print(path)
        for check in CHECKS:
            result = check(output, args.lists)
            if isinstance(result, tuple):
                result = [result]
            for verdict, evidence in result:
                print("%-4s %-5s %s" % (check.__name__[6:].upper(), verdict,
                                        evidence))


if __name__ == "__main__":
    main()
