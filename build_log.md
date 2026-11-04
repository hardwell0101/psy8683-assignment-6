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

- Hash of the `pre-handoff:` commit: `debbc92`. The draft ran in Pilot mode as participant 1. All 104 rows matched the participant 1 list in order.
- Hash of the first commit after the handoff: `d54b2ff`.
- Scope: extend the working Builder draft to meet Q1 through Q10.

List each change the model made in your own words, and for each say whether you kept
it, changed it, or reverted it, and why. A change you cannot explain is a
change you cannot keep.

| Change | Kept / changed / reverted | Why |
| --- | --- | --- |
| | | |


## Final settings

| Setting | Builder implementation |
| --- | --- |
| Trial lists and order | The startup number selects the two-digit relative filename. Sequential loops use rows 0:8 and 8:104, once each. |
| Response mapping | Odd participant numbers use F for word and J for nonword. Even numbers reverse the mapping. The instructions display the assigned keys. |
| Timing | In the 60 Hz windowed pilot, fixation and the blank interval each last 30 frames, the prime 9, practice feedback 60, and the response limit and end screen 120. Target onset follows prime onset by 9 or 60 frames. The full-screen participant 3 run measured 120.042 Hz and used 60, 18, 120 and 240 frames respectively. Its short and long SOAs spanned 18 and 120 frames. |
| Response and scoring | The keyboard clears earlier presses and resets its clock on the target flip. The first valid F or J determines accuracy. A timeout gives accuracy 0 with empty key and RT. |
| Display and onset columns | The text columns read the stimulus objects. The onset columns copy the flip timestamps Builder recorded for those same objects. |

The revised file reopened in Builder and compiled. A separate shortened desktop pilot used scripted responses on three practice and three main trials from participant 2. It exercised both SOAs and all three scoring outcomes. The recorded onsets, text, practice feedback durations, timeout durations, and inter-trial intervals matched the expected values. This diagnostic was separate from the participant runs.

## AI-use note (Part F)

Write this the way you would write a methods paragraph: which parts of the
experiment, the checker, and the written parts were model-generated, what
you asked for, what you had to correct, and anything you rejected. Model use
is expected in this course; an absent or contentless note is what costs
points.
