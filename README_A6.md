# PSY 8683 Assignment 6: Verifying the build

Due **Wednesday, November 18, 11:59 pm**. The full assignment, including
grading, is on Canvas. This file covers what changes in your repository, the
two new instrumentation properties, and how to run things.

## What you are doing

In Assignment 5 you built the lexical decision task to the presentation
specification Q1–Q10 and checked Q1 and Q2. Now you check the rest of it:
Q3–Q10 on your own build and on the six provided files, a timing audit of
your build on your own machine, and a data dictionary for its output.

You work in the same repository. Nothing from A5 moves. See the Canvas assignment page for more details.

## Files added for A6

Copy these into the top level of your repository and commit them:

| Path | What it is |
| --- | --- |
| `README_A6.md` | This file. |
| `a6_predictions.md` | Part A. Commit before you run any new check. |
| `a6_report.md` | Part C: the verification report and the timing audit. |

You also finish three files you already have:

| Path | What changes |
| --- | --- |
| `data_dictionary.md` | Part D (its heading still says Part E, from A5). It now describes the output of your *instrumented* build, including the I1 and I2 additions. |
| `check_output.py` | Part E. Extend it to Q3–Q10 and I1–I2, with a new verdict (below). The stub's docstring still describes A5. You may change `CHECKS` and `main()` however you need, for example so an I1 check can find the log file next to the data file. |
| `build_log.md` | Add an A6 section at the end: what you changed for the instrumentation, and the AI-use note for A6 (Part F). |

## A new verdict

Your checker so far reports PASS, FAIL, or PILOT. Add **UNDETERMINED**:

    UNDETERMINED  the evidence in hand cannot settle the property; say what
                  evidence would

PILOT means you settled it some other way, by watching the experiment run
or by reading the build. UNDETERMINED means it is still open. For your own
build, almost nothing should stay UNDETERMINED in the report, because you
can run and read it. For the provided files you have only the file. You
cannot pilot a build you do not have, so their open properties stay
UNDETERMINED, and the report says what would settle each one.

A check that cannot fail is still not evidence. That goes for
UNDETERMINED too: do not use it for something the file could have
settled.

## Running your checker

On your own runs:

```
uv run python check_output.py data/3_ldt_*.csv data/6_ldt_*.csv
uv run python check_output.py data/7_ldt_*.csv data/8_ldt_*.csv
```

On the provided files, against the canonical lists:

```
uv run python check_output.py provided/output_files/*.csv --lists provided/canonical_trial_lists
```

The provided files were made by a build whose component names are not
necessarily yours. The automatic columns PsychoPy writes (`*.started`,
`*.stopped`, and the keyboard's `*.keys`, `*.rt`, `*.corr`) carry the
component's name. Your checker has to know which names mean what, and the
data dictionary is where you work that out.

## About the provided files, again

The six files in `provided/output_files/` were produced by a simulated
participant on a simulated 60 Hz display with perfect timing. Every flip
lands exactly on the frame grid. Your own runs will not look like that, and
that difference is part of what Part C asks about.

## Commit history

Required message prefixes for A6:

- `predictions-a6:` for `a6_predictions.md`, before you run any new check
  (on your files or on the provided ones).
- `instrument:` for the commit that adds I1 and I2.
- `first-run:` for the commit with your first working Q3–Q10 checker's
  output on the six provided files (Part C asks for it).
- `fix:` for any change to the experiment after the tag that fixes a
  Q1–Q10 failure.
- `pre-handoff:` as in A5, if you give the experiment file to a language
  model to edit.
