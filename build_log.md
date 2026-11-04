# Build log (Part B) and AI-use note (Part F)

## Trial lists

The eight CSVs in `trial_lists/` came from the submitted Assignment 2 output for
participants 1 through 8 at seed 8683. Commit `9d5b9e8` contains these inputs
and the original starter files. The supplied cases use the separate lists in
`provided/canonical_trial_lists/`.

## How the build happened

- `b0a73de` records the initial Builder instructions screen and its SPACE
  response, before the practice and main loops were added.
- `7bdb1c6` records the Q1 and Q2 checker and its first results on the six
  supplied files. Before running it on those files, temporary examples tested
  an intact list, a wrong participant, changed input text, a partial record,
  swapped, missing and extra trials, and a duplicate replacing another trial.
- After preserving those results, the six files were examined for the likely
  Builder settings and their consequences. The evidence is in
  `verification_report.md`.

## Handoff (only if you used a language model on the experiment file)

- Hash of the `pre-handoff:` commit:
- Hash of the first commit after the handoff:
- What you asked for:

List each change the model made in your own words, and for each say whether you kept
it, changed it, or reverted it, and why. A change you cannot explain is a
change you cannot keep.

| Change | Kept / changed / reverted | Why |
| --- | --- | --- |
| | | |


## AI-use note (Part F)

Write this the way you would write a methods paragraph: which parts of the
experiment, the checker, and the written parts were model-generated, what
you asked for, what you had to correct, and anything you rejected. Model use
is expected in this course; an absent or contentless note is what costs
points.
