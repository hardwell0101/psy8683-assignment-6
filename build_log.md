# Build log (Part B) and AI-use note (Part E)

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

## Changes after the handoff

- Hash of the `pre-handoff:` commit: `debbc92`. The draft ran in Pilot mode as participant 1. All 104 rows matched the participant 1 list in order.
- Hash of the first commit after the handoff: `d54b2ff`.
- Scope: extend the working Builder draft to meet Q1 through Q10.

The baseline and the revised Builder file can be compared with `git diff debbc92 d54b2ff -- ldt.psyexp`.

| Change from the pilot | Decision | Reason |
| --- | --- | --- |
| Replace the fixed participant 1 filename in both loops with a filename built from the startup number. | Kept | Entering 6 must select `trials_p06.csv`. The same two sequential loops still take the first 8 rows and then the remaining 96. |
| Set the word and nonword keys from the participant number and show them in the opening instructions. | Kept | Participant 3 uses F for words. Participant 6 uses J. The instructions and scoring need to agree. |
| Convert fixation, prime, target onset and the response limit to frame counts using the measured refresh rate. | Kept | A 150 ms interval needs 18 frames on a 120 Hz screen but only 9 at 60 Hz. Measuring the rate avoids using the windowed pilot's frame count in a full-screen run. |
| Add practice feedback, a break that waits for Space, a blank interval after each trial and a timed end screen. | Kept | Practice gives the participant one second to see the outcome. The main block omits feedback and still gives half a second between trials. |
| Score the first valid target-period key against the assigned mapping. Check the last frame for an in-time key before recording a timeout. | Kept | If there is no response within two seconds, key and RT stay empty. Accuracy is zero for both an incorrect press and a timeout, so the separate timeout flag distinguishes them. |
| Save the prime and target from the text objects, and save their Builder flip timestamps. | Kept | These fields show what the program drew and when. The input columns alone describe only what was planned. |

The first participant 6 attempt was rejected. An older Builder draft ran with 6 in the dialog but still loaded participant 1's trials. The replacement used `ldt.py` compiled from the verified final `ldt.psyexp`. The recorded trials then passed both list checks. Commit `aba0d9e` contains the participant 3 run and `de91402` contains the accepted participant 6 run and the compiled script.

## Final settings

| Setting | Builder implementation |
| --- | --- |
| Trial lists and order | The startup number selects the two-digit relative filename. Sequential loops use rows 0:8 and 8:104, once each. |
| Response mapping | Odd participant numbers use F for word and J for nonword. Even numbers reverse the mapping. The instructions display the assigned keys. |
| Timing | In the 60 Hz windowed pilot, fixation and the blank interval each last 30 frames, the prime 9, practice feedback 60, and the response limit and end screen 120. Target onset follows prime onset by 9 or 60 frames. The full-screen participant 3 run measured 120.042 Hz and used 60, 18, 120 and 240 frames respectively. Its short and long SOAs spanned 18 and 120 frames. |
| Response and scoring | The keyboard clears earlier presses and resets its clock on the target flip. The first valid F or J determines accuracy. A timeout gives accuracy 0 with empty key and RT. |
| Display and onset columns | The text columns read the stimulus objects. The onset columns copy the flip timestamps Builder recorded for those same objects. |

The revised file reopened in Builder and compiled. A separate shortened desktop pilot used scripted responses on three practice and three main trials from participant 2. It exercised both SOAs and all three scoring outcomes. The recorded onsets, text, practice feedback durations, timeout durations, and inter-trial intervals matched the expected values. This diagnostic was separate from the participant runs.

## AI-use note (Part E)

I used Codex for Builder guidance while I made the initial instructions, trial routine, and practice and main loops. I supplied the participant 3 predictions before the first complete run and made the keyboard responses in the submitted sessions. After the participant 1 pilot was committed, I used Codex to extend the Builder file to Q1–Q10. Codex wrote the Q1–Q2 checker, ran it on the supplied and recorded files, and drafted the change table, verification report, and reconciliation from the output. During piloting, the keyboard driver had to be repaired and a run labeled `pilot` was repeated with participant ID 1. The first participant 6 attempt used the wrong list and was excluded. The six-trial scripted diagnostic checked the revised build separately from the submitted participant data.
