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

## Assignment 6

Commit `928db57` is the A5 baseline with the three A6 templates. The
experiment and runs 3 and 6 at this checkpoint are the original A5 evidence.
Ibra supplied the predictions in chat using the written A5 findings and the
Mac's reported display setting. Codex calculated the frame counts and mapped
Ibra's rule and three exceptions to the table. Commit `a9fbe92` freezes the
answers before the first new output check. This handoff preserves the same
Builder file and compiled script before Codex adds frame recording.

### Instrumentation and fixes

After the pre-handoff commit (`acf8fcd`), Codex added flip-interval recording
for each trial (`adc14ea`) and recompiled the Builder file in the PsychoPy
Studio 2026.2.2 environment. At the end of each trial the program saves the
change in the number of long intervals, the number of intervals recorded,
and the time of the last recorded flip. After the end screen clears, it
writes all intervals to the participant's paired frame log. The checker
tests each trial separately, including whether the intervals span the time
from fixation onset to its last recorded flip. The long-interval threshold
is 1.5 nominal frame periods. [PsychoPy frame recording](https://psychopy.org/general/timing/detectingFrameDrops.html)

Commit `3bc4c00` preserves the first six-file checker output. Reading
the affected columns afterward showed why F's visible target duration
and the keyboard deadline needed separate tests. Later revisions also
compared the keyboard's automatic scoring with the required mapping.
The submitted A5 experiment could miss a keyboard event timestamped
1.999 s. The saved probe in `ab034c5` reproduced that error on a main
trial. Commit `e7a7ced` checks for queued keys through the deadline on
target removal and uses the final outcome for practice feedback. A
second fix (`937c9c2`) defers writing the log until the display clears
so disk access cannot hold the end screen open.

The final six-trial windowed diagnostic used scripted key events and real
window flips. Both practice and main accepted the 1.999 s probe. All six
trial spans matched their slices of the log, with seven long intervals
among 1,348 recorded. One trial included a deliberate delay. Two ITIs
and one feedback presentation ran long. They lie outside the trial
recording window, so this log cannot establish the causes. The end screen
spanned the planned 240 frame periods. See
`evidence/submission_pilot/verification.txt` and
`evidence/submission_pilot/timing_audit.txt`. The checker also passed
13 tests, including wrong source fields, scoring and per-trial allocation
of frame drops. Results are in `evidence/checker_tests.txt`.

### Full human sessions

I completed all 104 trials in each accepted session and supplied the physical keypresses. My first full run as participant 7 had the chat app open. I excluded that run from the quiet comparison and repeated it using Studio’s participant dialog after closing the other application. Commit `a7b9399` preserves the superseded data. The accepted files in `data/` use the 13h53 basename for 7 and the 12h47 basename for 8. The output files from interrupted or failed launches did not enter the analysis.

For participant 8, Studio ran the same compiled experiment with participant 8 and session 001 supplied at startup through a short launcher. It used the usual data, window, device, experiment and save functions. Only the participant-dialog entry was bypassed. I responded on the keyboard while Chrome played a muted looping video. A preliminary launch outside Studio stopped before any trials. For the quiet repeat I used the normal Builder dialog and the built-in main screen while a second monitor was connected. Studio regenerated the local compiled script with its compile time and source path. The compiled run 7 script and the portable script in Git had identical executable syntax after accounting for the generated source-path metadata. Both runs used the same Builder file.

For each accepted CSV, Codex ran `python3 check_output.py` with the expected participant, `--require-log` and `--build ldt.psyexp`. It independently compared the frame-log slices with the stimulus timestamps using `python3 timing_audit.py`. The 104 per-trial counts and whole-run totals agreed in both sessions. Results are in `evidence/a6_run7.txt`, `evidence/a6_run8.txt` and the two corresponding timing audits.

### AI use for Assignment 6

I asked Codex to handle the technical work and tell me when the assignment needed my input. I supplied my predictions before the new checks, using the written A5 findings to recall the six files. Codex calculated the predicted frame counts, translated my answers into the table, and committed them. After the handoff, Codex generated the instrumentation, compiled the experiment, extended the checker, and wrote the scripted pilot and tests. It drafted the report, data dictionary and reconciliation from the CSVs, frame logs and build. The first checker confused target offset with the keyboard deadline in file F. The corrected version checks both timestamps. I chose to repeat participant 7 when we found the chat had stayed open during the first session. I supplied all participant responses in the two accepted runs. Only the separately labeled diagnostic sessions used simulated key events.
