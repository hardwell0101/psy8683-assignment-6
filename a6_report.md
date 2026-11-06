# Verification report and timing audit

## 1. The submitted A5 build

The A5 experiment is the version in `928db57`. For participants 3 and 6, the
observed screen sequence, prime and target fields, SOAs, key codes, recorded
onsets, and recorded accuracy agreed with the checks. Each file contains eight
practice and 96 main trials. Both rounded display rates were 120 Hz. Reading
the build and probing the response deadline exposed a bug that ordinary key
and RT comparisons missed.

**Q10, last-millisecond response.** In the submitted code the final queue
read occurs during routine cleanup. That code can run before the following
flip removes the target. In participant 3's timeout the routine ended at
156.506740 s and the target offset was 156.514818 s. The CSV cannot tell us
whether anyone actually pressed a key during those 8.08 ms. A scripted test
on the instrumented version of the same response code offered a key stamped
1.999 s. The main trial recorded a timeout. Commit `ab034c5` preserves this
failure. In `e7a7ced` the queue is drained at the target removal flip through
the two-second deadline. Both practice and main tests then accepted 1.999 s.
On pending practice responses, feedback starts one flip after target removal
so the program can use the final response. Feedback still receives its full
frame allotment. Participant 6 had no timeout, so its CSV alone cannot
establish timeout behavior. Section 2 gives the results of the two full runs on the corrected build.

**Q4, response-to-removal delay.** Four response trials took over two nominal
refresh periods from the recorded keypress to the first replacement flip.
Participant 3 had delays of 18.925 and 16.828 ms on CSV lines 4 and 28.
Participant 6 had 20.518 and 16.885 ms on lines 6 and 62. The source clears
the target when Builder polls the key and flips the next screen. The
durations above are measured. Attributing their extra time to polling,
drawing or a delayed flip would require polling timestamps and flip intervals
from those original runs. I1 and I2 were introduced after A5.

**Build inspection and its limits.** The PILOT lines below refer to reading
the source at the stated commit. The criteria were the participant-dependent
relative path (Q1), correct instruction and feedback text, SPACE gates and
routine order (Q3), fixation and blank contents (Q4), frame expressions
(Q5), odd/even mapping and allowed keys (Q6), clearing and resetting on
target flip followed by first-key selection (Q7), and reading both text
objects at trial end (Q8). A hardcoded path, incorrect mapping, wrong gate,
time-based component stop, keyboard reset on fixation, or copying the input
words instead of the text objects would fail the corresponding inspection.
Physical onset in Q9 remains open without a synchronized light sensor.

The checker attaches the documented manual inspection only with an explicit
`--build` whose SHA-256 matches a reviewed source. For reproduction, export
`git show 928db57:ldt.psyexp > /tmp/a6-submitted-build.psyexp` and run
`python3 check_output.py data/3_ldt_*.csv --participant 3 --build /tmp/a6-submitted-build.psyexp`.
Repeat with participant 6. Details follow.

<details><summary>Original run 3 checker output</summary>

```text
data/3_ldt_2026-11-04_12h44.45.576.csv
  Q1 PASS All 104 recorded trials match rows of trials_p03.csv on all ten input fields.
  Q2 PASS 104/104 trial identities from trials_p03.csv in exact file order (phase, trial_index, item_id).
  I1 UNDETERMINED interval log [1 undetermined]: need matching 3_ldt_2026-11-04_12h44.45.576_frameIntervals.log
  I2 UNDETERMINED per-trial counts [1 undetermined]: need dropped_frames
  Q3 PASS phase counts and order [1 pass]: {'practice': 8, 'experimental': 96}
  Q3 PASS instructions SPACE response [1 pass]: line 2: 'space' vs 'space'
  Q4 PASS next fixation after ITI [102 pass]: line 4: 4.423438s vs 4.423438s
  Q3 PASS screen follows last ITI [2 pass]: line 11: 25.048631s vs 25.048631s
  Q3 PASS break SPACE response [1 pass]: line 11: 'space' vs 'space'
  Q3 PASS end screen duration [1 pass]: line 108: 240.04 elapsed frames, expected 240; elapsed estimate at rounded Hz
  Q5 PASS end screen duration [1 pass]: line 108: 240.04 elapsed frames, expected 240; elapsed estimate at rounded Hz
  Q3 PASS screen order [1 pass]: row sequence compared with specification
  Q3 PASS practice feedback [8 pass]: line 3: 119.99 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q5 PASS practice feedback frame count [8 pass]: line 3: 119.99 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q4 PASS fixation [104 pass]: line 3: 60.08 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q5 PASS fixation frame count [104 pass]: line 3: 60.08 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q4 PASS prime [104 pass]: line 3: 18.02 elapsed frames, expected 18; elapsed estimate at rounded Hz
  Q5 PASS prime frame count [104 pass]: line 3: 18.02 elapsed frames, expected 18; elapsed estimate at rounded Hz
  Q4 PASS SOA [104 pass]: line 3: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q5 PASS SOA frames [104 pass]: line 3: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q4 PASS ITI [104 pass]: line 3: 59.99 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q5 PASS ITI frame count [104 pass]: line 3: 59.99 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q4 PASS fixation to prime transition [104 pass]: line 3: 1.248658s vs 1.248658s
  Q4 PASS blank interval from prime offset to target [104 pass]: line 3: 101.98 elapsed frames, expected 102; elapsed estimate at rounded Hz
  Q4 PASS prime recorded content [104 pass]: line 3: 'gravel' vs 'gravel'
  Q8 PASS prime shown vs list [104 pass]: line 3: 'gravel' vs 'gravel'
  Q4 PASS target recorded content [104 pass]: line 3: 'BLODGE' vs 'BLODGE'
  Q8 PASS target shown vs list [104 pass]: line 3: 'BLODGE' vs 'BLODGE'
  Q3 PASS feedback directly precedes ITI [8 pass]: line 3: 3.923509s vs 3.923509s
  Q6 PASS accepted recorded key [104 pass]: line 3: 'j'
  Q6 PASS scored keys agree with specified parity mapping [104 pass]: line 3: 1 vs 1
  Q10 PASS accuracy under participant mapping [104 pass]: line 3: 1 vs 1
  Q7 PASS keyboard starts on target flip [104 pass]: line 3: 2.248698s vs 2.248698s
  Q9 PASS prime onset vs component flip [104 pass]: line 3: 1.248658s vs 1.248658s
  Q9 PASS target onset vs component flip [104 pass]: line 3: 2.248698s vs 2.248698s
  Q10 PASS response fields and two-second limit [104 pass]: line 3: key='j', rt='0.6647626250050962', timeout=0
  Q7 PASS saved response vs automatic key and RT [104 pass]: line 3: 0.664763s vs 0.664763s, key 'j' vs 'j'
  Q4 UNDETERMINED target removed on response or deadline [102 pass, 2 undetermined]: line 4: replacement 2.27 refresh periods after key; need key polling time and flip intervals to attribute delay
  Q3 PASS no main feedback [96 pass]: line 12: '' vs ''
  Q10 PASS keyboard available through target deadline [1 pass]: line 78: keyboard covered deadline, stopped at 1.99990s
  Q10 PASS ten unmodified trial-list fields [1 pass]: All 104 recorded trials match rows of trials_p03.csv on all ten input fields.
  Q1 PILOT Inspected the participant dialog, two-digit listPath, sequential loops and relative file in the corresponding Builder source. Q1 file evidence separately checks the typed ID against the actual list.
  Q3 PILOT Inspected instructions, feedbackText, and Flow: the instructions interpolate the assigned keys, beginKey and resumeKey accept Space, and practice feedbackMessage branches on accuracy and timeout before the ITI.
  Q4 PILOT Inspected fixation.text (+), prime and target frame starts, the empty background during the long-SOA gap, and blankScreen during the ITI. The next feedback or interval flip removes a response-ended target.
  Q5 PILOT Inspected the measured expInfo frameRate rounding, frame-count starts/stops, and targetFrame = fixFrames + round(soa * refreshHz / 1000) in the corresponding source.
  Q6 PILOT Inspected odd/even wordKey and nonwordKey, instruction interpolation, the decision F/J allowlist, and global Escape handling in the compiled loops.
  Q7 PILOT Inspected the compiled loops: clock reset and buffer clearing on the first target flip, subsequent polling, and storage of the first allowed key. Physical device latency remains outside software evidence.
  Q8 PILOT Inspected scoreTrial End Routine: prime_shown and target_shown read prime_text.text and target_text.text, after the trial.
  Q9 UNDETERMINED further evidence [1 undetermined]: need independent light sensor aligned to flip time for physical display onset
  Q10 FAIL Last-frame test at adc14ea with the A5 response logic: a main-trial event at 1.999 s was coded timeout. See evidence/last_frame_before/verification.txt. Fixed at e7a7ced.
```

</details>

<details><summary>Original run 6 checker output</summary>

```text
data/6_ldt_2026-11-04_12h59.17.668.csv
  Q1 PASS All 104 recorded trials match rows of trials_p06.csv on all ten input fields.
  Q2 PASS 104/104 trial identities from trials_p06.csv in exact file order (phase, trial_index, item_id).
  I1 UNDETERMINED interval log [1 undetermined]: need matching 6_ldt_2026-11-04_12h59.17.668_frameIntervals.log
  I2 UNDETERMINED per-trial counts [1 undetermined]: need dropped_frames
  Q3 PASS phase counts and order [1 pass]: {'practice': 8, 'experimental': 96}
  Q3 PASS instructions SPACE response [1 pass]: line 2: 'space' vs 'space'
  Q4 PASS next fixation after ITI [102 pass]: line 4: 3.873741s vs 3.873741s
  Q3 PASS screen follows last ITI [2 pass]: line 11: 27.174437s vs 27.174437s
  Q3 PASS break SPACE response [1 pass]: line 11: 'space' vs 'space'
  Q3 PASS end screen duration [1 pass]: line 108: 239.99 elapsed frames, expected 240; elapsed estimate at rounded Hz
  Q5 PASS end screen duration [1 pass]: line 108: 239.99 elapsed frames, expected 240; elapsed estimate at rounded Hz
  Q3 PASS screen order [1 pass]: row sequence compared with specification
  Q3 PASS practice feedback [8 pass]: line 3: 119.99 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q5 PASS practice feedback frame count [8 pass]: line 3: 119.99 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q4 PASS fixation [104 pass]: line 3: 60.10 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q5 PASS fixation frame count [104 pass]: line 3: 60.10 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q4 PASS prime [104 pass]: line 3: 18.02 elapsed frames, expected 18; elapsed estimate at rounded Hz
  Q5 PASS prime frame count [104 pass]: line 3: 18.02 elapsed frames, expected 18; elapsed estimate at rounded Hz
  Q4 PASS SOA [104 pass]: line 3: 18.02 elapsed frames, expected 18; elapsed estimate at rounded Hz
  Q5 PASS SOA frames [104 pass]: line 3: 18.02 elapsed frames, expected 18; elapsed estimate at rounded Hz
  Q4 PASS ITI [104 pass]: line 3: 59.91 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q5 PASS ITI frame count [104 pass]: line 3: 59.91 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q4 PASS fixation to prime transition [104 pass]: line 3: 1.541212s vs 1.541212s
  Q4 PASS blank interval from prime offset to target [104 pass]: line 3: 0.00 elapsed frames, expected 0; elapsed estimate at rounded Hz
  Q4 PASS prime recorded content [104 pass]: line 3: 'plane' vs 'plane'
  Q8 PASS prime shown vs list [104 pass]: line 3: 'plane' vs 'plane'
  Q4 PASS target recorded content [104 pass]: line 3: 'PILOT' vs 'PILOT'
  Q8 PASS target shown vs list [104 pass]: line 3: 'PILOT' vs 'PILOT'
  Q3 PASS feedback directly precedes ITI [8 pass]: line 3: 3.374488s vs 3.374488s
  Q6 PASS accepted recorded key [104 pass]: line 3: 'f'
  Q6 PASS scored keys agree with specified parity mapping [104 pass]: line 3: 0 vs 0
  Q10 PASS accuracy under participant mapping [104 pass]: line 3: 0 vs 0
  Q7 PASS keyboard starts on target flip [104 pass]: line 3: 1.691419s vs 1.691419s
  Q9 PASS prime onset vs component flip [104 pass]: line 3: 1.541212s vs 1.541212s
  Q9 PASS target onset vs component flip [104 pass]: line 3: 1.691419s vs 1.691419s
  Q10 PASS response fields and two-second limit [104 pass]: line 3: key='f', rt='0.6673451249953359', timeout=0
  Q7 PASS saved response vs automatic key and RT [104 pass]: line 3: 0.667345s vs 0.667345s, key 'f' vs 'f'
  Q4 UNDETERMINED target removed on response or deadline [102 pass, 2 undetermined]: line 6: replacement 2.46 refresh periods after key; need key polling time and flip intervals to attribute delay
  Q3 PASS no main feedback [96 pass]: line 12: '' vs ''
  Q10 UNDETERMINED timeout case [1 undetermined]: need a trial without a response through the deadline
  Q10 PASS ten unmodified trial-list fields [1 pass]: All 104 recorded trials match rows of trials_p06.csv on all ten input fields.
  Q1 PILOT Inspected the participant dialog, two-digit listPath, sequential loops and relative file in the corresponding Builder source. Q1 file evidence separately checks the typed ID against the actual list.
  Q3 PILOT Inspected instructions, feedbackText, and Flow: the instructions interpolate the assigned keys, beginKey and resumeKey accept Space, and practice feedbackMessage branches on accuracy and timeout before the ITI.
  Q4 PILOT Inspected fixation.text (+), prime and target frame starts, the empty background during the long-SOA gap, and blankScreen during the ITI. The next feedback or interval flip removes a response-ended target.
  Q5 PILOT Inspected the measured expInfo frameRate rounding, frame-count starts/stops, and targetFrame = fixFrames + round(soa * refreshHz / 1000) in the corresponding source.
  Q6 PILOT Inspected odd/even wordKey and nonwordKey, instruction interpolation, the decision F/J allowlist, and global Escape handling in the compiled loops.
  Q7 PILOT Inspected the compiled loops: clock reset and buffer clearing on the first target flip, subsequent polling, and storage of the first allowed key. Physical device latency remains outside software evidence.
  Q8 PILOT Inspected scoreTrial End Routine: prime_shown and target_shown read prime_text.text and target_text.text, after the trial.
  Q9 UNDETERMINED further evidence [1 undetermined]: need independent light sensor aligned to flip time for physical display onset
  Q10 FAIL Last-frame test at adc14ea with the A5 response logic: a main-trial event at 1.999 s was coded timeout. See evidence/last_frame_before/verification.txt. Fixed at e7a7ced.
```

</details>

## 2. Timing audit

### Machine and runs

Both sessions used PsychoPy Studio 2026.2.2 in desktop Run mode. The MacBook Pro had an Apple M5 Pro, 48 GB of memory and macOS 27.2. The experiment ran fullscreen on display 0, the built-in Liquid Retina XDR display (3024 × 1964 physical pixels, 1512 × 982 logical points). The Mac reported 120 Hz for the built-in display during setup.

| | Run 7, quiet repeat | Run 8, muted video |
| --- | --- | --- |
| CSV basename, Nov 6 | `7_ldt_2026-11-06_13h53.16.033` | `8_ldt_2026-11-06_12h47.58.644` |
| Measured rate in CSV | 120.24957798166257 Hz | 120.06897963686515 Hz |
| Display configuration | Built-in main display. An unmirrored 4K external monitor was connected. | Built-in display. The Mac reported only the built-in display at setup. |
| Other applications | PsychoPy only for the task. The browser and video server were stopped. ChatGPT reopened after the end screen. | Chrome played a muted, looping 10-second video from PsychoPy’s demo assets. The chat app was open. |
| Trial rows | 8 practice + 96 experimental | 8 practice + 96 experimental |
| Correct responses / timeouts | 80 of 104 / 0 | 17 of 104 / 0 |

The first participant 7 session had finished with the chat app open. I repeated it to meet the quiet condition. The accepted run began at 13:53 and ended at 13:57, before ChatGPT reopened at 13:58. Its predecessor is preserved in commit `a7b9399`. Both sessions had zero recorded drops. Run 8 occurred before the accepted repeat. Chrome’s video frame counter advanced throughout the run, and the player reported muted playback. The differing application and monitor setups limit what two runs can establish about the cause of the timing difference. [Browser playback record](evidence/run8_video.txt)

### Achieved timing

Both measured rates round to 120 Hz. One nominal frame period is 8.333 ms, so I2 counts intervals strictly longer than 12.5 ms. The table uses **elapsed frame periods × number of observations**. For example, 68 × 1 means one fixation lasted about 68 frame periods. The expected count comes from Q5. To compute each observed count, multiply the difference between the event’s two flip timestamps by 120 and round to the nearest integer.

| Event | Expected frames | Run 7 | Run 8 |
| --- | ---: | --- | --- |
| Fixation | 60 | 60 × 104 | 60 × 89, 62 × 5, 63 × 4, 64 × 5, 68 × 1 |
| Prime | 18 | 18 × 104 | 18 × 102, 20 × 1, 21 × 1 |
| Prime-to-target, 150 ms SOA | 18 | 18 × 52 | 18 × 51, 21 × 1 |
| Blank after prime, 150 ms SOA | 0 | 0 × 52 | 0 × 52 |
| Prime-to-target, 1000 ms SOA | 120 | 120 × 52 | 120 × 39, 121 × 1, 122 × 3, 123 × 7, 124 × 2 |
| Blank after prime, 1000 ms SOA | 102 | 102 × 52 | 102 × 39, 103 × 2, 104 × 3, 105 × 6, 106 × 2 |
| Inter-trial interval (ITI) | 60 | 60 × 104 | 60 × 87, 61 × 1, 62 × 10, 63 × 3, 64 × 2, 65 × 1 |
| Practice feedback | 120 | 120 × 8 | 120 × 7, 121 × 1 |
| End screen | 240 | 240 × 1 | 240 × 1 |

The checker recalculated all 208 scores from each participant’s assigned keys. Every stored score agreed, including the incorrect responses in run 8. Both sessions used the same 240-frame maximum target window. Every human trial ended on a keypress, so neither file contains a 240-frame timeout to measure. The opening instructions and the break also ended on a keypress. The build’s separate diagnostic exercised true timeouts as well as presses at 1.999 s. [Timeout pilot](evidence/final_pilot/verification.txt) · [Last-millisecond probe](evidence/submission_pilot/verification.txt)

| Check on the trial window | Run 7 | Run 8 |
| --- | ---: | ---: |
| Intervals in I1, all 104 trial slices combined | 20,502 | 21,221 |
| Intervals longer than 12.5 ms | 0 | 133 |
| Sum of the CSV’s `dropped_frames` column | 0 | 133 |
| Trials with at least one such interval | 0 | 38 |
| Longest interval | 9.8501 ms | 18.7665 ms |

**Run 7.** All fixed-duration events matched their expected elapsed count. Each trial’s logged intervals span fixation onset to the last target flip. The individual slices and the whole log agree with I2. [Checker output](evidence/a6_run7.txt) · [Timing audit](evidence/timing_run7.txt)

**Run 8.** The number of actual flip intervals between the fixation, prime and target boundaries matched the frame settings on every trial. Some intervals took longer than one refresh. The 133 long intervals comprised 50 during fixation, 5 during the prime, 34 during the long-SOA blank and 44 while the target was visible. Exactly one ended on the target-onset flip. The longest interval occurred during the target on practice trial 7. For example, on practice trial 6 (CSV line 8), three long intervals extended the 18-flip prime to 21 elapsed periods. Target onset moved later by the same amount on this short-SOA trial. [Checker output](evidence/a6_run8.txt) · [Timing audit](evidence/timing_run8.txt)

One of eight feedback periods and 17 of 104 ITIs ran long in run 8. The checker flags their **elapsed** durations under Q3/Q4/Q5. Their boundary stamps show how late they finished, but I1 stops at the last target flip. Eleven of the long ITIs followed trials with zero recorded drops. Even when the preceding trial had a drop, its log cannot identify the cause of a later ITI or feedback delay. The frame-count expressions in the build match Q5. Recording every flip in those later routines in a separate diagnostic would distinguish slow flips from an incorrect count. [Run 8 timing audit](evidence/timing_run8.txt)

The target replacement occurred 16.995 ms after a key on experimental trial 75 of run 7 (line 86), and 16.704 ms after a key on experimental trial 33 of run 8 (line 44). Both trials recorded zero drops. The differences slightly exceed two nominal periods. The files establish the delays. Neither contains both the keyboard polling timestamps and the flip interval across target removal needed to explain them. Across all other response trials the replacement was within the checker’s two-period tolerance.

<details><summary>All run 8 fixed-duration exceptions by CSV line</summary>

The entries below show every deviation in the distribution table. A long prime can also lengthen its SOA, so one interval may appear in two event comparisons. For overlapping events the interval contributes only once to the total of 133.

```text
line 6 fixation: 67.981 elapsed vs 60 planned frames; within-event long intervals (ms): [17.594, 14.241, 17.374, 16.998, 16.682, 16.636, 17.193, 16.578]; trial drops=8
line 6 feedback: 121.121 elapsed vs 120 planned frames; trial drops=8; outside the recording window; the log cannot identify a cause
line 8 prime: 21.002 elapsed vs 18 planned frames; within-event long intervals (ms): [17.449, 17.912, 14.0]; trial drops=3
line 8 SOA 150: 21.002 elapsed vs 18 planned frames; within-event long intervals (ms): [17.449, 17.912, 14.0]; trial drops=3
line 15 ITI: 63.016 elapsed vs 60 planned frames; trial drops=1; outside the recording window; the log cannot identify a cause
line 17 SOA 1000: 122.009 elapsed vs 120 planned frames; within-event long intervals (ms): [16.902, 17.358]; trial drops=2
line 17 blank, SOA 1000: 104.061 elapsed vs 102 planned frames; within-event long intervals (ms): [16.902, 17.358]; trial drops=2
line 18 fixation: 63.867 elapsed vs 60 planned frames; within-event long intervals (ms): [18.277, 17.266, 16.569, 13.925]; trial drops=8
line 18 ITI: 62.064 elapsed vs 60 planned frames; trial drops=8; outside the recording window; the log cannot identify a cause
line 20 SOA 1000: 122.863 elapsed vs 120 planned frames; within-event long intervals (ms): [18.296, 16.729, 13.506]; trial drops=7
line 20 blank, SOA 1000: 104.995 elapsed vs 102 planned frames; within-event long intervals (ms): [18.296, 16.729, 13.506]; trial drops=7
line 22 SOA 1000: 121.994 elapsed vs 120 planned frames; within-event long intervals (ms): [18.343, 13.432]; trial drops=2
line 22 blank, SOA 1000: 104.016 elapsed vs 102 planned frames; within-event long intervals (ms): [18.343, 13.432]; trial drops=2
line 23 fixation: 63.895 elapsed vs 60 planned frames; within-event long intervals (ms): [17.31, 17.506, 16.741, 13.801]; trial drops=4
line 24 SOA 1000: 121.168 elapsed vs 120 planned frames; within-event long intervals (ms): [17.132]; trial drops=2
line 24 blank, SOA 1000: 103.313 elapsed vs 102 planned frames; within-event long intervals (ms): [17.132]; trial drops=2
line 24 ITI: 63.040 elapsed vs 60 planned frames; trial drops=2; outside the recording window; the log cannot identify a cause
line 31 ITI: 62.198 elapsed vs 60 planned frames; trial drops=0; outside the recording window; the log cannot identify a cause
line 32 fixation: 62.004 elapsed vs 60 planned frames; within-event long intervals (ms): [18.231, 13.384]; trial drops=2
line 33 ITI: 64.124 elapsed vs 60 planned frames; trial drops=0; outside the recording window; the log cannot identify a cause
line 34 ITI: 61.856 elapsed vs 60 planned frames; trial drops=0; outside the recording window; the log cannot identify a cause
line 36 fixation: 63.024 elapsed vs 60 planned frames; within-event long intervals (ms): [16.963, 17.268, 16.496]; trial drops=8
line 36 SOA 1000: 123.047 elapsed vs 120 planned frames; within-event long intervals (ms): [18.589, 16.92, 15.839]; trial drops=8
line 36 blank, SOA 1000: 104.963 elapsed vs 102 planned frames; within-event long intervals (ms): [18.589, 16.92, 15.839]; trial drops=8
line 38 SOA 1000: 122.151 elapsed vs 120 planned frames; within-event long intervals (ms): [18.098, 13.44]; trial drops=4
line 38 blank, SOA 1000: 104.004 elapsed vs 102 planned frames; within-event long intervals (ms): [18.098, 13.44]; trial drops=4
line 38 ITI: 62.954 elapsed vs 60 planned frames; trial drops=4; outside the recording window; the log cannot identify a cause
line 39 ITI: 60.963 elapsed vs 60 planned frames; trial drops=0; outside the recording window; the log cannot identify a cause
line 40 ITI: 61.995 elapsed vs 60 planned frames; trial drops=0; outside the recording window; the log cannot identify a cause
line 42 fixation: 62.955 elapsed vs 60 planned frames; within-event long intervals (ms): [17.234, 16.63, 13.519]; trial drops=3
line 47 SOA 1000: 123.844 elapsed vs 120 planned frames; within-event long intervals (ms): [17.212, 16.709, 17.171, 14.882]; trial drops=4
line 47 blank, SOA 1000: 105.923 elapsed vs 102 planned frames; within-event long intervals (ms): [17.212, 16.709, 17.171, 14.882]; trial drops=4
line 50 ITI: 64.062 elapsed vs 60 planned frames; trial drops=0; outside the recording window; the log cannot identify a cause
line 52 fixation: 62.957 elapsed vs 60 planned frames; within-event long intervals (ms): [17.093, 17.232, 17.058]; trial drops=3
line 54 ITI: 61.978 elapsed vs 60 planned frames; trial drops=0; outside the recording window; the log cannot identify a cause
line 57 fixation: 63.979 elapsed vs 60 planned frames; within-event long intervals (ms): [17.183, 17.817, 16.722, 16.084]; trial drops=4
line 66 fixation: 63.796 elapsed vs 60 planned frames; within-event long intervals (ms): [18.37, 17.57, 15.715, 16.133]; trial drops=7
line 67 ITI: 61.987 elapsed vs 60 planned frames; trial drops=0; outside the recording window; the log cannot identify a cause
line 69 ITI: 62.197 elapsed vs 60 planned frames; trial drops=0; outside the recording window; the log cannot identify a cause
line 71 fixation: 62.012 elapsed vs 60 planned frames; within-event long intervals (ms): [17.032, 14.878]; trial drops=5
line 71 SOA 1000: 122.984 elapsed vs 120 planned frames; within-event long intervals (ms): [16.939, 17.075, 17.067]; trial drops=5
line 71 blank, SOA 1000: 104.933 elapsed vs 102 planned frames; within-event long intervals (ms): [16.939, 17.075, 17.067]; trial drops=5
line 72 ITI: 65.037 elapsed vs 60 planned frames; trial drops=2; outside the recording window; the log cannot identify a cause
line 79 fixation: 62.003 elapsed vs 60 planned frames; within-event long intervals (ms): [18.067, 16.072]; trial drops=2
line 79 ITI: 61.815 elapsed vs 60 planned frames; trial drops=2; outside the recording window; the log cannot identify a cause
line 82 fixation: 61.981 elapsed vs 60 planned frames; within-event long intervals (ms): [17.004, 15.962]; trial drops=2
line 89 SOA 1000: 123.052 elapsed vs 120 planned frames; within-event long intervals (ms): [16.876, 17.597, 15.22]; trial drops=3
line 89 blank, SOA 1000: 105.103 elapsed vs 102 planned frames; within-event long intervals (ms): [16.876, 17.597, 15.22]; trial drops=3
line 90 ITI: 61.992 elapsed vs 60 planned frames; trial drops=0; outside the recording window; the log cannot identify a cause
line 92 ITI: 61.987 elapsed vs 60 planned frames; trial drops=0; outside the recording window; the log cannot identify a cause
line 93 fixation: 64.066 elapsed vs 60 planned frames; within-event long intervals (ms): [16.703, 16.653, 16.992, 13.621]; trial drops=4
line 94 prime: 20.334 elapsed vs 18 planned frames; within-event long intervals (ms): [18.038, 16.818]; trial drops=3
line 94 SOA 1000: 123.074 elapsed vs 120 planned frames; within-event long intervals (ms): [18.038, 16.818, 16.445]; trial drops=3
line 94 blank, SOA 1000: 102.741 elapsed vs 102 planned frames; within-event long intervals (ms): [16.445]; trial drops=3
line 95 SOA 1000: 123.056 elapsed vs 120 planned frames; within-event long intervals (ms): [17.321, 17.15, 15.391]; trial drops=3
line 95 blank, SOA 1000: 104.946 elapsed vs 102 planned frames; within-event long intervals (ms): [17.321, 17.15, 15.391]; trial drops=3
line 99 SOA 1000: 123.944 elapsed vs 120 planned frames; within-event long intervals (ms): [16.705, 16.966, 16.338, 15.556]; trial drops=4
line 99 blank, SOA 1000: 105.940 elapsed vs 102 planned frames; within-event long intervals (ms): [16.705, 16.966, 16.338, 15.556]; trial drops=4
line 100 SOA 1000: 123.039 elapsed vs 120 planned frames; within-event long intervals (ms): [16.991, 17.564, 13.624]; trial drops=5
line 100 blank, SOA 1000: 105.045 elapsed vs 102 planned frames; within-event long intervals (ms): [16.991, 17.564, 13.624]; trial drops=5
line 101 fixation: 63.018 elapsed vs 60 planned frames; within-event long intervals (ms): [17.481, 17.609, 16.349]; trial drops=3
line 107 fixation: 62.035 elapsed vs 60 planned frames; within-event long intervals (ms): [17.94, 16.801]; trial drops=2
```

</details>

### What the timing evidence establishes

| Property | Verified from software timestamps | Bound and its assumptions | Physical measurement |
| --- | --- | --- | --- |
| Q4, fixation, prime, SOA and ITI | Subtract the corresponding stimulus flip stamps. The interval from prime stop to target start measures the software gap. On trials that end on a key, the replacement stimulus can give the target offset. | The frame grid limits requested durations. How long the target remains after a queued response also depends on when the next poll and flip occur. A delayed refresh can extend an interval. | Measure light at the stimulus location to establish that the intended image appeared and disappeared at those times. |
| Q5, whole frames | For instrumented events inside the recording window, the per-trial intervals reconstruct the flip sequence. Compare the number of actual flips with the frame rule separately from elapsed milliseconds. For feedback, ITI and end screen we have boundary timestamps and estimated elapsed frame counts. | On a stable display at the rounded rate, the nominal rounding error is at most half a frame per specified duration. That bound covers quantization only. Refresh variation, operating-system delays, missed flips and the difference between rounded and actual Hz add uncertainty. | The program cannot certify scan-out position, pixel response or the visible exposure at a location from flip timestamps alone. |
| Q7, reaction time | Compare keyboard start and target flip. The saved RT can be compared to the keyboard's event time. The source establishes which key was selected and when the buffer was cleared. | Polling reveals an event by the next successful poll under normal operation. The recorded event time and the time the program handles it can differ. Without device calibration there is no numeric bound on total physical input latency from this file. | An optical onset sensor and an instrumented switch or response box on a common clock can measure physical RT. |
| Q9, onsets | Compare the custom onset with the corresponding automatic stimulus start on the same software clock. | A software flip timestamp locates the relevant refresh; translating it to a visible onset needs a calibrated display delay and scan-out location. | A photodiode at the relevant location establishes actual luminance onset. |
| Q10, two-second deadline | For a timeout, compare keyboard stop with target start separately from target disappearance. For a response check key, RT, accuracy and timeout and compare the automatic key record. An empty response alone cannot demonstrate a complete listening window. | The scheduled visual cutoff is a whole number of frames. The corrected build checks the queue at offset and compares the recorded RT to 2.000 s. Physical closure near the cutoff carries keyboard timestamp uncertainty. | A calibrated input event relative to measured light onset tests the physical boundary. |

The build uses Python's nearest-integer rounding on the rounded measured
display rate. Counts for 500 ms apply to fixation and ITI; counts for 150 ms
apply to both the prime and the short SOA.

| Hz | 500 ms | 150 ms | Long SOA and feedback, 1 s | End and maximum target, 2 s | Nominal 150 ms interval |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 60 | 30 | 9 | 60 | 120 | 150.00 ms |
| 75 | 38 | 11 | 75 | 150 | 146.67 ms |
| 120 | 60 | 18 | 120 | 240 | 150.00 ms |
| 144 | 72 | 22 | 144 | 288 | 152.78 ms |

At 75 Hz, 37.5 frames rounds to the even integer 38, giving 506.67 ms for
the fixation. These are consequences of the source expressions. The two
human runs measure only the display used for this assignment.

## 3. The six provided files

The table summarizes CSV evidence on the checkable parts. P means those
parts passed. F identifies a contradiction. The shared open parts below apply
to each of A through F, including each P cell.

| File | Q3 sequence | Q4 trial | Q5 frames | Q6 keys | Q7 RT | Q8 shown | Q9 onsets | Q10 coding and inputs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | P | P | P | F, scored mapping | P | P | P | F, accuracy |
| B | P | P | P | P | P | P | P | P |
| C | P | P | P | P | P | P | P | F, wrong participant's inputs |
| D | P | F, prime field | P | P | P | F, prime | P | P |
| E | P | P | P | P | P | P | P | P |
| F | P | P, displayed target duration | P | P | F, clock starts early | P | P | F, keyboard cutoff |

**A.** All 104 planned rows arrived in order. The automatic and custom
accuracy fields recorded zero throughout, although 97 recorded keys match
the assigned category-to-key mapping. Comparing key names to category names
in Builder could produce this pattern. The file establishes a scoring
disagreement, but cannot distinguish that setting from a later overwrite.
An analyst using stored accuracy would report 0/104 rather than 97/104.

**B.** The intended list, shown fields, timing, valid keys and recalculated
scores agree. The file is consistent with sequential loops and a keyboard
starting on the target. An analyst could use those recorded fields for the
tested comparisons. Correct-looking data do not recover the instruction
wording or establish how the text values were obtained.

**C.** The run says participant 7, but the sequence matches participant 1
when the participant field is excluded. A conditions path fixed to list 1
would explain this. Q10 checks the ten columns against the *intended*
participant's list, so this also fails there. An analyst joining conditions
from list 7 would assign the wrong items or conditions. The records alone
cannot establish which path Builder actually opened.

**D.** The planned primes vary, but the shown-prime field is the literal
word `prime` in all 104 trials. A literal Builder text parameter or a
constant in the logger would explain this. Q4 and Q8 fail on the recorded
text. An analyst using only the input word would treat planned priming
conditions as delivered. Reading the display and logging code or observing
the run would separate the two possible explanations.

**E.** The 104 intended trials are present, but 103 occupy a different
position. A random loop within each phase would explain the result. The
8/96 phase structure still passes Q3. An analyst checking only condition
counts would overlook the sequence and a run of five identical response
categories in the main block. This was already an A5 Q2 failure.

**F.** Every keyboard start coincides with fixation, 650 or 1500 ms before
the target. All 50 timeouts are long-SOA trials. On those trials the keyboard
closes 500 ms after target onset although the target stays up for about two
seconds. Starting the keyboard and its two-second timer at fixation explains
both the inflated saved RTs and the reduced response opportunity. An analyst
could mistake this for a behavioral effect of SOA.

**Open evidence in all six.** Q3 needs the build or an observed run for the
actual instruction wording, feedback messages and which other keys the
gates reject. Q4 needs the stimulus definitions or a visual observation for
the fixation glyph and the contents of nominal blanks. Q5 needs the source,
or runs at other rates, for the scheduling rule. Q6 needs the configured
allowlist, instructions and an invalid-key/Escape test for behavior beyond
the recorded keys. Q7 needs the clock-reset, clearing and event-selection
code or a controlled input trace. Q8 needs the logging expression to prove
object provenance. For Q9, exact physical light onset needs a synchronized
sensor. The matching flip stamps do establish software onset. The six files
predate I1/I2 and come with no interval logs.

**First checker and corrections.** Commit `3bc4c00` preserves the first
six-file output before the A6 manual inspection. It caught A's custom
accuracy errors, C's source-list mismatch, D's recorded text error, and F's
early keyboard start. It initially passed Q10's deadline on F because it
used the *target stop* stamp to infer when the keyboard stopped. It also
flagged Q4 response removal on 54 trials by adding the fixation-relative RT
to target onset. The corrected check uses keyboard start plus automatic RT
for the key event, and reads keyboard stop directly on timeouts. In
`232afc4` the corrected verdicts changed to Q4 PASS on the visible target
duration and Q10 FAIL on 50 keyboard deadlines. That commit also selects the
visual `blank` component before considering a routine boundary for the ITI.
In `f1cccf4` Q6 gained a check against automatic keyboard scoring, which
revealed the same scoring fault as Q10 in A. B and E passed the new
checkable properties in both versions. Separate mutations of the B fixture
verify that its passes could turn into failures.

**What A5 could see.** A, D and F passed both old checks. Q1's input
comparison came closest: it established the correct category in A, the
planned prime in D and the planned SOA in F. It never compared the stored
score, shown stimulus or keyboard clock. Q2 established row order and could
not detect any of those three faults.

<details><summary>Final checker output on A through F</summary>

```text
provided/output_files/file_A.csv
  Q1 PASS All 104 recorded trials match rows of trials_p03.csv on all ten input fields.
  Q2 PASS 104/104 trial identities from trials_p03.csv in exact file order (phase, trial_index, item_id).
  I1 UNDETERMINED interval log [1 undetermined]: need matching file_A_frameIntervals.log
  I2 UNDETERMINED per-trial counts [1 undetermined]: need dropped_frames
  Q3 PASS phase counts and order [1 pass]: {'practice': 8, 'experimental': 96}
  Q3 PASS instructions SPACE response [1 pass]: line 2: 'space' vs 'space'
  Q4 PASS next fixation after ITI [102 pass]: line 4: 4.383333s vs 4.383333s
  Q3 PASS screen follows last ITI [2 pass]: line 11: 26.533333s vs 26.533333s
  Q3 PASS break SPACE response [1 pass]: line 11: 'space' vs 'space'
  Q3 PASS end screen duration [1 pass]: line 108: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q5 PASS end screen duration [1 pass]: line 108: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q3 PASS screen order [1 pass]: row sequence compared with specification
  Q3 PASS practice feedback [8 pass]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q5 PASS practice feedback frame count [8 pass]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q4 PASS fixation [104 pass]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q5 PASS fixation frame count [104 pass]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q4 PASS prime [104 pass]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q5 PASS prime frame count [104 pass]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q4 PASS SOA [104 pass]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q5 PASS SOA frames [104 pass]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q4 PASS ITI [104 pass]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q5 PASS ITI frame count [104 pass]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q4 PASS fixation to prime transition [104 pass]: line 3: 1.366667s vs 1.366667s
  Q4 PASS blank interval from prime offset to target [104 pass]: line 3: 51.00 elapsed frames, expected 51; elapsed estimate at rounded Hz
  Q4 PASS prime recorded content [104 pass]: line 3: 'plane' vs 'plane'
  Q8 PASS prime shown vs list [104 pass]: line 3: 'plane' vs 'plane'
  Q4 PASS target recorded content [104 pass]: line 3: 'PILOT' vs 'PILOT'
  Q8 PASS target shown vs list [104 pass]: line 3: 'PILOT' vs 'PILOT'
  Q3 PASS feedback directly precedes ITI [8 pass]: line 3: 3.883333s vs 3.883333s
  Q6 PASS accepted recorded key [104 pass]: line 3: 'f'
  Q6 FAIL scored keys agree with specified parity mapping [97 fail, 7 pass]: line 3: 0 vs 1
  Q10 FAIL accuracy under participant mapping [97 fail, 7 pass]: line 3: 0 vs 1
  Q7 PASS keyboard starts on target flip [104 pass]: line 3: 2.366667s vs 2.366667s
  Q9 PASS prime onset vs component flip [104 pass]: line 3: 1.366667s vs 1.366667s
  Q9 PASS target onset vs component flip [104 pass]: line 3: 2.366667s vs 2.366667s
  Q10 PASS response fields and two-second limit [104 pass]: line 3: key='f', rt='0.4836037519372667', timeout=0
  Q7 PASS saved response vs automatic key and RT [104 pass]: line 3: 0.483604s vs 0.483604s, key 'f' vs 'f'
  Q4 PASS target removed on response or deadline [104 pass]: line 3: replacement flip 0.03306s after keyboard event
  Q3 PASS no main feedback [96 pass]: line 12: '' vs ''
  Q10 PASS keyboard available through target deadline [1 pass]: line 35: keyboard covered deadline, stopped at 2.00000s
  Q10 PASS ten unmodified trial-list fields [1 pass]: All 104 recorded trials match rows of trials_p03.csv on all ten input fields.
  Q1 UNDETERMINED further evidence [1 undetermined]: need dialog and relative filename in the build
  Q3 UNDETERMINED further evidence [1 undetermined]: need instruction wording, feedback messages and SPACE-only gates in the build
  Q4 UNDETERMINED further evidence [1 undetermined]: need fixation glyph and contents of blank screens in the build
  Q5 UNDETERMINED further evidence [1 undetermined]: need frame scheduling rule across refresh rates in the build
  Q6 UNDETERMINED further evidence [1 undetermined]: need key mapping in instructions, ignored inputs and Escape handling in the build or a pilot
  Q7 UNDETERMINED further evidence [1 undetermined]: need first-key selection, event clearing and clock-reset implementation
  Q8 UNDETERMINED further evidence [1 undetermined]: need build code reading from stimulus objects
  Q9 UNDETERMINED further evidence [1 undetermined]: need independent light sensor aligned to flip time for physical display onset
provided/output_files/file_B.csv
  Q1 PASS All 104 recorded trials match rows of trials_p04.csv on all ten input fields.
  Q2 PASS 104/104 trial identities from trials_p04.csv in exact file order (phase, trial_index, item_id).
  I1 UNDETERMINED interval log [1 undetermined]: need matching file_B_frameIntervals.log
  I2 UNDETERMINED per-trial counts [1 undetermined]: need dropped_frames
  Q3 PASS phase counts and order [1 pass]: {'practice': 8, 'experimental': 96}
  Q3 PASS instructions SPACE response [1 pass]: line 2: 'space' vs 'space'
  Q4 PASS next fixation after ITI [102 pass]: line 4: 3.800000s vs 3.800000s
  Q3 PASS screen follows last ITI [2 pass]: line 11: 26.616667s vs 26.616667s
  Q3 PASS break SPACE response [1 pass]: line 11: 'space' vs 'space'
  Q3 PASS end screen duration [1 pass]: line 108: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q5 PASS end screen duration [1 pass]: line 108: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q3 PASS screen order [1 pass]: row sequence compared with specification
  Q3 PASS practice feedback [8 pass]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q5 PASS practice feedback frame count [8 pass]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q4 PASS fixation [104 pass]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q5 PASS fixation frame count [104 pass]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q4 PASS prime [104 pass]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q5 PASS prime frame count [104 pass]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q4 PASS SOA [104 pass]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q5 PASS SOA frames [104 pass]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q4 PASS ITI [104 pass]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q5 PASS ITI frame count [104 pass]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q4 PASS fixation to prime transition [104 pass]: line 3: 1.366667s vs 1.366667s
  Q4 PASS blank interval from prime offset to target [104 pass]: line 3: 0.00 elapsed frames, expected 0; elapsed estimate at rounded Hz
  Q4 PASS prime recorded content [104 pass]: line 3: 'gravel' vs 'gravel'
  Q8 PASS prime shown vs list [104 pass]: line 3: 'gravel' vs 'gravel'
  Q4 PASS target recorded content [104 pass]: line 3: 'BLODGE' vs 'BLODGE'
  Q8 PASS target shown vs list [104 pass]: line 3: 'BLODGE' vs 'BLODGE'
  Q3 PASS feedback directly precedes ITI [8 pass]: line 3: 3.300000s vs 3.300000s
  Q6 PASS accepted recorded key [104 pass]: line 3: 'f'
  Q6 PASS scored keys agree with specified parity mapping [104 pass]: line 3: 1 vs 1
  Q10 PASS accuracy under participant mapping [104 pass]: line 3: 1 vs 1
  Q7 PASS keyboard starts on target flip [104 pass]: line 3: 1.516667s vs 1.516667s
  Q9 PASS prime onset vs component flip [104 pass]: line 3: 1.366667s vs 1.366667s
  Q9 PASS target onset vs component flip [104 pass]: line 3: 1.516667s vs 1.516667s
  Q10 PASS response fields and two-second limit [104 pass]: line 3: key='f', rt='0.7554058535198465', timeout=0
  Q7 PASS saved response vs automatic key and RT [104 pass]: line 3: 0.755406s vs 0.755406s, key 'f' vs 'f'
  Q4 PASS target removed on response or deadline [104 pass]: line 3: replacement flip 0.02793s after keyboard event
  Q3 PASS no main feedback [96 pass]: line 12: '' vs ''
  Q10 PASS keyboard available through target deadline [2 pass]: line 45: keyboard covered deadline, stopped at 2.00000s
  Q10 PASS ten unmodified trial-list fields [1 pass]: All 104 recorded trials match rows of trials_p04.csv on all ten input fields.
  Q1 UNDETERMINED further evidence [1 undetermined]: need dialog and relative filename in the build
  Q3 UNDETERMINED further evidence [1 undetermined]: need instruction wording, feedback messages and SPACE-only gates in the build
  Q4 UNDETERMINED further evidence [1 undetermined]: need fixation glyph and contents of blank screens in the build
  Q5 UNDETERMINED further evidence [1 undetermined]: need frame scheduling rule across refresh rates in the build
  Q6 UNDETERMINED further evidence [1 undetermined]: need key mapping in instructions, ignored inputs and Escape handling in the build or a pilot
  Q7 UNDETERMINED further evidence [1 undetermined]: need first-key selection, event clearing and clock-reset implementation
  Q8 UNDETERMINED further evidence [1 undetermined]: need build code reading from stimulus objects
  Q9 UNDETERMINED further evidence [1 undetermined]: need independent light sensor aligned to flip time for physical display onset
provided/output_files/file_C.csv
  Q1 FAIL trials_p07.csv: 104 unmatched trial records; line 3: ('practice', '1', 'PW4') does not match all input fields
  Q2 FAIL trials_p07.csv: 104 recorded, 104 expected; 104 missing, 104 excess. First difference at trial 1: expected ('practice', '1', 'PW3'), observed ('practice', '1', 'PW4').
  I1 UNDETERMINED interval log [1 undetermined]: need matching file_C_frameIntervals.log
  I2 UNDETERMINED per-trial counts [1 undetermined]: need dropped_frames
  Q3 PASS phase counts and order [1 pass]: {'practice': 8, 'experimental': 96}
  Q3 PASS instructions SPACE response [1 pass]: line 2: 'space' vs 'space'
  Q4 PASS next fixation after ITI [102 pass]: line 4: 4.483333s vs 4.483333s
  Q3 PASS screen follows last ITI [2 pass]: line 11: 26.433333s vs 26.433333s
  Q3 PASS break SPACE response [1 pass]: line 11: 'space' vs 'space'
  Q3 PASS end screen duration [1 pass]: line 108: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q5 PASS end screen duration [1 pass]: line 108: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q3 PASS screen order [1 pass]: row sequence compared with specification
  Q3 PASS practice feedback [8 pass]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q5 PASS practice feedback frame count [8 pass]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q4 PASS fixation [104 pass]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q5 PASS fixation frame count [104 pass]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q4 PASS prime [104 pass]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q5 PASS prime frame count [104 pass]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q4 PASS SOA [104 pass]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q5 PASS SOA frames [104 pass]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q4 PASS ITI [104 pass]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q5 PASS ITI frame count [104 pass]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q4 PASS fixation to prime transition [104 pass]: line 3: 1.366667s vs 1.366667s
  Q4 PASS blank interval from prime offset to target [104 pass]: line 3: 51.00 elapsed frames, expected 51; elapsed estimate at rounded Hz
  Q4 PASS prime recorded content [104 pass]: line 3: 'metal' vs 'metal'
  Q8 PASS prime shown vs list [104 pass]: line 3: 'metal' vs 'metal'
  Q4 PASS target recorded content [104 pass]: line 3: 'COPPER' vs 'COPPER'
  Q8 PASS target shown vs list [104 pass]: line 3: 'COPPER' vs 'COPPER'
  Q3 PASS feedback directly precedes ITI [8 pass]: line 3: 3.983333s vs 3.983333s
  Q6 PASS accepted recorded key [104 pass]: line 3: 'f'
  Q6 PASS scored keys agree with specified parity mapping [104 pass]: line 3: 1 vs 1
  Q10 PASS accuracy under participant mapping [104 pass]: line 3: 1 vs 1
  Q7 PASS keyboard starts on target flip [104 pass]: line 3: 2.366667s vs 2.366667s
  Q9 PASS prime onset vs component flip [104 pass]: line 3: 1.366667s vs 1.366667s
  Q9 PASS target onset vs component flip [104 pass]: line 3: 2.366667s vs 2.366667s
  Q10 PASS response fields and two-second limit [104 pass]: line 3: key='f', rt='0.5843092762578408', timeout=0
  Q7 PASS saved response vs automatic key and RT [104 pass]: line 3: 0.584309s vs 0.584309s, key 'f' vs 'f'
  Q4 PASS target removed on response or deadline [104 pass]: line 3: replacement flip 0.03236s after keyboard event
  Q3 PASS no main feedback [96 pass]: line 12: '' vs ''
  Q10 PASS keyboard available through target deadline [2 pass]: line 29: keyboard covered deadline, stopped at 2.00000s
  Q10 FAIL ten unmodified trial-list fields [1 fail]: trials_p07.csv: 104 unmatched trial records; line 3: ('practice', '1', 'PW4') does not match all input fields
  Q1 UNDETERMINED further evidence [1 undetermined]: need dialog and relative filename in the build
  Q3 UNDETERMINED further evidence [1 undetermined]: need instruction wording, feedback messages and SPACE-only gates in the build
  Q4 UNDETERMINED further evidence [1 undetermined]: need fixation glyph and contents of blank screens in the build
  Q5 UNDETERMINED further evidence [1 undetermined]: need frame scheduling rule across refresh rates in the build
  Q6 UNDETERMINED further evidence [1 undetermined]: need key mapping in instructions, ignored inputs and Escape handling in the build or a pilot
  Q7 UNDETERMINED further evidence [1 undetermined]: need first-key selection, event clearing and clock-reset implementation
  Q8 UNDETERMINED further evidence [1 undetermined]: need build code reading from stimulus objects
  Q9 UNDETERMINED further evidence [1 undetermined]: need independent light sensor aligned to flip time for physical display onset
provided/output_files/file_D.csv
  Q1 PASS All 104 recorded trials match rows of trials_p02.csv on all ten input fields.
  Q2 PASS 104/104 trial identities from trials_p02.csv in exact file order (phase, trial_index, item_id).
  I1 UNDETERMINED interval log [1 undetermined]: need matching file_D_frameIntervals.log
  I2 UNDETERMINED per-trial counts [1 undetermined]: need dropped_frames
  Q3 PASS phase counts and order [1 pass]: {'practice': 8, 'experimental': 96}
  Q3 PASS instructions SPACE response [1 pass]: line 2: 'space' vs 'space'
  Q4 PASS next fixation after ITI [102 pass]: line 4: 3.650000s vs 3.650000s
  Q3 PASS screen follows last ITI [2 pass]: line 11: 26.450000s vs 26.450000s
  Q3 PASS break SPACE response [1 pass]: line 11: 'space' vs 'space'
  Q3 PASS end screen duration [1 pass]: line 108: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q5 PASS end screen duration [1 pass]: line 108: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q3 PASS screen order [1 pass]: row sequence compared with specification
  Q3 PASS practice feedback [8 pass]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q5 PASS practice feedback frame count [8 pass]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q4 PASS fixation [104 pass]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q5 PASS fixation frame count [104 pass]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q4 PASS prime [104 pass]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q5 PASS prime frame count [104 pass]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q4 PASS SOA [104 pass]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q5 PASS SOA frames [104 pass]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q4 PASS ITI [104 pass]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q5 PASS ITI frame count [104 pass]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q4 PASS fixation to prime transition [104 pass]: line 3: 1.366667s vs 1.366667s
  Q4 PASS blank interval from prime offset to target [104 pass]: line 3: 0.00 elapsed frames, expected 0; elapsed estimate at rounded Hz
  Q4 FAIL prime recorded content [104 fail]: line 3: 'prime' vs 'gravel'
  Q8 FAIL prime shown vs list [104 fail]: line 3: 'prime' vs 'gravel'
  Q4 PASS target recorded content [104 pass]: line 3: 'BLODGE' vs 'BLODGE'
  Q8 PASS target shown vs list [104 pass]: line 3: 'BLODGE' vs 'BLODGE'
  Q3 PASS feedback directly precedes ITI [8 pass]: line 3: 3.150000s vs 3.150000s
  Q6 PASS accepted recorded key [104 pass]: line 3: 'f'
  Q6 PASS scored keys agree with specified parity mapping [104 pass]: line 3: 1 vs 1
  Q10 PASS accuracy under participant mapping [104 pass]: line 3: 1 vs 1
  Q7 PASS keyboard starts on target flip [104 pass]: line 3: 1.516667s vs 1.516667s
  Q9 PASS prime onset vs component flip [104 pass]: line 3: 1.366667s vs 1.366667s
  Q9 PASS target onset vs component flip [104 pass]: line 3: 1.516667s vs 1.516667s
  Q10 PASS response fields and two-second limit [104 pass]: line 3: key='f', rt='0.6164674831760522', timeout=0
  Q7 PASS saved response vs automatic key and RT [104 pass]: line 3: 0.616467s vs 0.616467s, key 'f' vs 'f'
  Q4 PASS target removed on response or deadline [104 pass]: line 3: replacement flip 0.01687s after keyboard event
  Q3 PASS no main feedback [96 pass]: line 12: '' vs ''
  Q10 PASS keyboard available through target deadline [4 pass]: line 31: keyboard covered deadline, stopped at 2.00000s
  Q10 PASS ten unmodified trial-list fields [1 pass]: All 104 recorded trials match rows of trials_p02.csv on all ten input fields.
  Q1 UNDETERMINED further evidence [1 undetermined]: need dialog and relative filename in the build
  Q3 UNDETERMINED further evidence [1 undetermined]: need instruction wording, feedback messages and SPACE-only gates in the build
  Q4 UNDETERMINED further evidence [1 undetermined]: need fixation glyph and contents of blank screens in the build
  Q5 UNDETERMINED further evidence [1 undetermined]: need frame scheduling rule across refresh rates in the build
  Q6 UNDETERMINED further evidence [1 undetermined]: need key mapping in instructions, ignored inputs and Escape handling in the build or a pilot
  Q7 UNDETERMINED further evidence [1 undetermined]: need first-key selection, event clearing and clock-reset implementation
  Q8 UNDETERMINED further evidence [1 undetermined]: need build code reading from stimulus objects
  Q9 UNDETERMINED further evidence [1 undetermined]: need independent light sensor aligned to flip time for physical display onset
provided/output_files/file_E.csv
  Q1 PASS All 104 recorded trials match rows of trials_p05.csv on all ten input fields.
  Q2 FAIL trials_p05.csv: 104 recorded, 104 expected; 0 missing, 0 excess. First difference at trial 1: expected ('practice', '1', 'PN2'), observed ('practice', '2', 'PW2').
  I1 UNDETERMINED interval log [1 undetermined]: need matching file_E_frameIntervals.log
  I2 UNDETERMINED per-trial counts [1 undetermined]: need dropped_frames
  Q3 PASS phase counts and order [1 pass]: {'practice': 8, 'experimental': 96}
  Q3 PASS instructions SPACE response [1 pass]: line 2: 'space' vs 'space'
  Q4 PASS next fixation after ITI [102 pass]: line 4: 3.666667s vs 3.666667s
  Q3 PASS screen follows last ITI [2 pass]: line 11: 26.400000s vs 26.400000s
  Q3 PASS break SPACE response [1 pass]: line 11: 'space' vs 'space'
  Q3 PASS end screen duration [1 pass]: line 108: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q5 PASS end screen duration [1 pass]: line 108: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q3 PASS screen order [1 pass]: row sequence compared with specification
  Q3 PASS practice feedback [8 pass]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q5 PASS practice feedback frame count [8 pass]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q4 PASS fixation [104 pass]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q5 PASS fixation frame count [104 pass]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q4 PASS prime [104 pass]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q5 PASS prime frame count [104 pass]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q4 PASS SOA [104 pass]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q5 PASS SOA frames [104 pass]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q4 PASS ITI [104 pass]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q5 PASS ITI frame count [104 pass]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q4 PASS fixation to prime transition [104 pass]: line 3: 1.366667s vs 1.366667s
  Q4 PASS blank interval from prime offset to target [104 pass]: line 3: 0.00 elapsed frames, expected 0; elapsed estimate at rounded Hz
  Q4 PASS prime recorded content [104 pass]: line 3: 'onion' vs 'onion'
  Q8 PASS prime shown vs list [104 pass]: line 3: 'onion' vs 'onion'
  Q4 PASS target recorded content [104 pass]: line 3: 'GARLIC' vs 'GARLIC'
  Q8 PASS target shown vs list [104 pass]: line 3: 'GARLIC' vs 'GARLIC'
  Q3 PASS feedback directly precedes ITI [8 pass]: line 3: 3.166667s vs 3.166667s
  Q6 PASS accepted recorded key [104 pass]: line 3: 'f'
  Q6 PASS scored keys agree with specified parity mapping [104 pass]: line 3: 1 vs 1
  Q10 PASS accuracy under participant mapping [104 pass]: line 3: 1 vs 1
  Q7 PASS keyboard starts on target flip [104 pass]: line 3: 1.516667s vs 1.516667s
  Q9 PASS prime onset vs component flip [104 pass]: line 3: 1.366667s vs 1.366667s
  Q9 PASS target onset vs component flip [104 pass]: line 3: 1.516667s vs 1.516667s
  Q10 PASS response fields and two-second limit [104 pass]: line 3: key='f', rt='0.6260179830846937', timeout=0
  Q7 PASS saved response vs automatic key and RT [104 pass]: line 3: 0.626018s vs 0.626018s, key 'f' vs 'f'
  Q4 PASS target removed on response or deadline [104 pass]: line 3: replacement flip 0.02398s after keyboard event
  Q3 PASS no main feedback [96 pass]: line 12: '' vs ''
  Q10 PASS keyboard available through target deadline [1 pass]: line 105: keyboard covered deadline, stopped at 2.00000s
  Q10 PASS ten unmodified trial-list fields [1 pass]: All 104 recorded trials match rows of trials_p05.csv on all ten input fields.
  Q1 UNDETERMINED further evidence [1 undetermined]: need dialog and relative filename in the build
  Q3 UNDETERMINED further evidence [1 undetermined]: need instruction wording, feedback messages and SPACE-only gates in the build
  Q4 UNDETERMINED further evidence [1 undetermined]: need fixation glyph and contents of blank screens in the build
  Q5 UNDETERMINED further evidence [1 undetermined]: need frame scheduling rule across refresh rates in the build
  Q6 UNDETERMINED further evidence [1 undetermined]: need key mapping in instructions, ignored inputs and Escape handling in the build or a pilot
  Q7 UNDETERMINED further evidence [1 undetermined]: need first-key selection, event clearing and clock-reset implementation
  Q8 UNDETERMINED further evidence [1 undetermined]: need build code reading from stimulus objects
  Q9 UNDETERMINED further evidence [1 undetermined]: need independent light sensor aligned to flip time for physical display onset
provided/output_files/file_F.csv
  Q1 PASS All 104 recorded trials match rows of trials_p08.csv on all ten input fields.
  Q2 PASS 104/104 trial identities from trials_p08.csv in exact file order (phase, trial_index, item_id).
  I1 UNDETERMINED interval log [1 undetermined]: need matching file_F_frameIntervals.log
  I2 UNDETERMINED per-trial counts [1 undetermined]: need dropped_frames
  Q3 PASS phase counts and order [1 pass]: {'practice': 8, 'experimental': 96}
  Q3 PASS instructions SPACE response [1 pass]: line 2: 'space' vs 'space'
  Q4 PASS next fixation after ITI [102 pass]: line 4: 3.666667s vs 3.666667s
  Q3 PASS screen follows last ITI [2 pass]: line 11: 32.050000s vs 32.050000s
  Q3 PASS break SPACE response [1 pass]: line 11: 'space' vs 'space'
  Q3 PASS end screen duration [1 pass]: line 108: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q5 PASS end screen duration [1 pass]: line 108: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q3 PASS screen order [1 pass]: row sequence compared with specification
  Q3 PASS practice feedback [8 pass]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q5 PASS practice feedback frame count [8 pass]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q4 PASS fixation [104 pass]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q5 PASS fixation frame count [104 pass]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q4 PASS prime [104 pass]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q5 PASS prime frame count [104 pass]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q4 PASS SOA [104 pass]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q5 PASS SOA frames [104 pass]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q4 PASS ITI [104 pass]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q5 PASS ITI frame count [104 pass]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q4 PASS fixation to prime transition [104 pass]: line 3: 1.366667s vs 1.366667s
  Q4 PASS blank interval from prime offset to target [104 pass]: line 3: 0.00 elapsed frames, expected 0; elapsed estimate at rounded Hz
  Q4 PASS prime recorded content [104 pass]: line 3: 'cloth' vs 'cloth'
  Q8 PASS prime shown vs list [104 pass]: line 3: 'cloth' vs 'cloth'
  Q4 PASS target recorded content [104 pass]: line 3: 'VELVET' vs 'VELVET'
  Q8 PASS target shown vs list [104 pass]: line 3: 'VELVET' vs 'VELVET'
  Q3 PASS feedback directly precedes ITI [8 pass]: line 3: 3.166667s vs 3.166667s
  Q6 PASS accepted recorded key [104 pass]: line 3: 'j'
  Q6 PASS scored keys agree with specified parity mapping [104 pass]: line 3: 1 vs 1
  Q10 PASS accuracy under participant mapping [104 pass]: line 3: 1 vs 1
  Q7 FAIL keyboard starts on target flip [104 fail]: line 3: 0.866667s vs 1.516667s
  Q9 PASS prime onset vs component flip [104 pass]: line 3: 1.366667s vs 1.366667s
  Q9 PASS target onset vs component flip [104 pass]: line 3: 1.516667s vs 1.516667s
  Q10 PASS response fields and two-second limit [104 pass]: line 3: key='j', rt='1.2666782862236232', timeout=0
  Q7 PASS saved response vs automatic key and RT [104 pass]: line 3: 1.266678s vs 1.266678s, key 'j' vs 'j'
  Q4 PASS target removed on response or deadline [104 pass]: line 3: replacement flip 0.03332s after keyboard event
  Q10 FAIL keyboard available through target deadline [50 fail]: line 5: keyboard closed 0.50000s after target
  Q3 PASS no main feedback [96 pass]: line 12: '' vs ''
  Q10 PASS ten unmodified trial-list fields [1 pass]: All 104 recorded trials match rows of trials_p08.csv on all ten input fields.
  Q1 UNDETERMINED further evidence [1 undetermined]: need dialog and relative filename in the build
  Q3 UNDETERMINED further evidence [1 undetermined]: need instruction wording, feedback messages and SPACE-only gates in the build
  Q4 UNDETERMINED further evidence [1 undetermined]: need fixation glyph and contents of blank screens in the build
  Q5 UNDETERMINED further evidence [1 undetermined]: need frame scheduling rule across refresh rates in the build
  Q6 UNDETERMINED further evidence [1 undetermined]: need key mapping in instructions, ignored inputs and Escape handling in the build or a pilot
  Q7 UNDETERMINED further evidence [1 undetermined]: need first-key selection, event clearing and clock-reset implementation
  Q8 UNDETERMINED further evidence [1 undetermined]: need build code reading from stimulus objects
  Q9 UNDETERMINED further evidence [1 undetermined]: need independent light sensor aligned to flip time for physical display onset
```

</details>

<details><summary>First checker output preserved in 3bc4c00</summary>

```text
provided/output_files/file_A.csv
  Q1 PASS All 104 recorded trials match rows of trials_p03.csv on all ten input fields.
  Q2 PASS 104/104 trial identities from trials_p03.csv in exact file order (phase, trial_index, item_id).
  I1 UNDETERMINED interval log [1]: need matching file_A_frameIntervals.log
  I2 UNDETERMINED per-trial counts [1]: need dropped_frames
  Q3 PASS phase counts and order [1]: {'practice': 8, 'experimental': 96}
  Q3 PASS instructions SPACE response [1]: line 2: 'space' vs 'space'
  Q3 PASS break SPACE response [1]: line 11: 'space' vs 'space'
  Q3 PASS end screen duration [1]: line 108: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q3 PASS screen order [1]: row sequence compared with specification
  Q3 PASS practice feedback [8]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q5 PASS practice feedback frame count [8]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q4 PASS fixation [104]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q5 PASS fixation frame count [104]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q4 PASS prime [104]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q5 PASS prime frame count [104]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q4 PASS SOA [104]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q5 PASS SOA frames [104]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q4 PASS ITI [104]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q5 PASS ITI frame count [104]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q4 PASS fixation to prime transition [104]: line 3: 1.366667s vs 1.366667s
  Q4 PASS prime recorded content [104]: line 3: 'plane' vs 'plane'
  Q8 PASS prime shown vs list [104]: line 3: 'plane' vs 'plane'
  Q4 PASS target recorded content [104]: line 3: 'PILOT' vs 'PILOT'
  Q8 PASS target shown vs list [104]: line 3: 'PILOT' vs 'PILOT'
  Q6 PASS accepted recorded key [104]: line 3: 'f'
  Q10 FAIL accuracy under participant mapping [97]: line 3: 0 vs 1
  Q10 PASS accuracy under participant mapping [7]: line 10: 0 vs 0
  Q7 PASS keyboard starts on target flip [104]: line 3: 2.366667s vs 2.366667s
  Q9 PASS prime onset vs component flip [104]: line 3: 1.366667s vs 1.366667s
  Q9 PASS target onset vs component flip [104]: line 3: 2.366667s vs 2.366667s
  Q10 PASS response fields and two-second limit [104]: line 3: key='f', rt='0.4836037519372667', timeout=0
  Q7 PASS saved response vs automatic key and RT [104]: line 3: 0.483604s vs 0.483604s, key 'f' vs 'f'
  Q4 PASS target removed on response or deadline [104]: line 3: target off 0.51667s after onset, RT 0.48360s
  Q3 PASS no main feedback [96]: line 12: '' vs ''
  Q10 PASS timeout referenced to target onset [1]: line 35: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q10 PASS ten unmodified trial-list fields [1]: All 104 recorded trials match rows of trials_p03.csv on all ten input fields.
  Q1 UNDETERMINED further evidence [1]: need dialog and relative filename in the build
  Q3 UNDETERMINED further evidence [1]: need instruction wording, feedback messages and SPACE-only gates in the build
  Q4 UNDETERMINED further evidence [1]: need fixation glyph and contents of blank screens in the build
  Q5 UNDETERMINED further evidence [1]: need frame scheduling rule across refresh rates in the build
  Q6 UNDETERMINED further evidence [1]: need key mapping in instructions, ignored inputs and Escape handling in the build or a pilot
  Q7 UNDETERMINED further evidence [1]: need first-key selection, event clearing and clock-reset implementation
  Q8 UNDETERMINED further evidence [1]: need build code reading from stimulus objects
  Q9 UNDETERMINED further evidence [1]: need independent light sensor aligned to flip time for physical display onset
provided/output_files/file_B.csv
  Q1 PASS All 104 recorded trials match rows of trials_p04.csv on all ten input fields.
  Q2 PASS 104/104 trial identities from trials_p04.csv in exact file order (phase, trial_index, item_id).
  I1 UNDETERMINED interval log [1]: need matching file_B_frameIntervals.log
  I2 UNDETERMINED per-trial counts [1]: need dropped_frames
  Q3 PASS phase counts and order [1]: {'practice': 8, 'experimental': 96}
  Q3 PASS instructions SPACE response [1]: line 2: 'space' vs 'space'
  Q3 PASS break SPACE response [1]: line 11: 'space' vs 'space'
  Q3 PASS end screen duration [1]: line 108: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q3 PASS screen order [1]: row sequence compared with specification
  Q3 PASS practice feedback [8]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q5 PASS practice feedback frame count [8]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q4 PASS fixation [104]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q5 PASS fixation frame count [104]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q4 PASS prime [104]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q5 PASS prime frame count [104]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q4 PASS SOA [104]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q5 PASS SOA frames [104]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q4 PASS ITI [104]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q5 PASS ITI frame count [104]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q4 PASS fixation to prime transition [104]: line 3: 1.366667s vs 1.366667s
  Q4 PASS prime recorded content [104]: line 3: 'gravel' vs 'gravel'
  Q8 PASS prime shown vs list [104]: line 3: 'gravel' vs 'gravel'
  Q4 PASS target recorded content [104]: line 3: 'BLODGE' vs 'BLODGE'
  Q8 PASS target shown vs list [104]: line 3: 'BLODGE' vs 'BLODGE'
  Q6 PASS accepted recorded key [104]: line 3: 'f'
  Q10 PASS accuracy under participant mapping [104]: line 3: 1 vs 1
  Q7 PASS keyboard starts on target flip [104]: line 3: 1.516667s vs 1.516667s
  Q9 PASS prime onset vs component flip [104]: line 3: 1.366667s vs 1.366667s
  Q9 PASS target onset vs component flip [104]: line 3: 1.516667s vs 1.516667s
  Q10 PASS response fields and two-second limit [104]: line 3: key='f', rt='0.7554058535198465', timeout=0
  Q7 PASS saved response vs automatic key and RT [104]: line 3: 0.755406s vs 0.755406s, key 'f' vs 'f'
  Q4 PASS target removed on response or deadline [104]: line 3: target off 0.78333s after onset, RT 0.75541s
  Q3 PASS no main feedback [96]: line 12: '' vs ''
  Q10 PASS timeout referenced to target onset [2]: line 45: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q10 PASS ten unmodified trial-list fields [1]: All 104 recorded trials match rows of trials_p04.csv on all ten input fields.
  Q1 UNDETERMINED further evidence [1]: need dialog and relative filename in the build
  Q3 UNDETERMINED further evidence [1]: need instruction wording, feedback messages and SPACE-only gates in the build
  Q4 UNDETERMINED further evidence [1]: need fixation glyph and contents of blank screens in the build
  Q5 UNDETERMINED further evidence [1]: need frame scheduling rule across refresh rates in the build
  Q6 UNDETERMINED further evidence [1]: need key mapping in instructions, ignored inputs and Escape handling in the build or a pilot
  Q7 UNDETERMINED further evidence [1]: need first-key selection, event clearing and clock-reset implementation
  Q8 UNDETERMINED further evidence [1]: need build code reading from stimulus objects
  Q9 UNDETERMINED further evidence [1]: need independent light sensor aligned to flip time for physical display onset
provided/output_files/file_C.csv
  Q1 FAIL trials_p07.csv: 104 unmatched trial records; line 3: ('practice', '1', 'PW4') does not match all input fields
  Q2 FAIL trials_p07.csv: 104 recorded, 104 expected; 104 missing, 104 excess. First difference at trial 1: expected ('practice', '1', 'PW3'), observed ('practice', '1', 'PW4').
  I1 UNDETERMINED interval log [1]: need matching file_C_frameIntervals.log
  I2 UNDETERMINED per-trial counts [1]: need dropped_frames
  Q3 PASS phase counts and order [1]: {'practice': 8, 'experimental': 96}
  Q3 PASS instructions SPACE response [1]: line 2: 'space' vs 'space'
  Q3 PASS break SPACE response [1]: line 11: 'space' vs 'space'
  Q3 PASS end screen duration [1]: line 108: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q3 PASS screen order [1]: row sequence compared with specification
  Q3 PASS practice feedback [8]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q5 PASS practice feedback frame count [8]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q4 PASS fixation [104]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q5 PASS fixation frame count [104]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q4 PASS prime [104]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q5 PASS prime frame count [104]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q4 PASS SOA [104]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q5 PASS SOA frames [104]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q4 PASS ITI [104]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q5 PASS ITI frame count [104]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q4 PASS fixation to prime transition [104]: line 3: 1.366667s vs 1.366667s
  Q4 PASS prime recorded content [104]: line 3: 'metal' vs 'metal'
  Q8 PASS prime shown vs list [104]: line 3: 'metal' vs 'metal'
  Q4 PASS target recorded content [104]: line 3: 'COPPER' vs 'COPPER'
  Q8 PASS target shown vs list [104]: line 3: 'COPPER' vs 'COPPER'
  Q6 PASS accepted recorded key [104]: line 3: 'f'
  Q10 PASS accuracy under participant mapping [104]: line 3: 1 vs 1
  Q7 PASS keyboard starts on target flip [104]: line 3: 2.366667s vs 2.366667s
  Q9 PASS prime onset vs component flip [104]: line 3: 1.366667s vs 1.366667s
  Q9 PASS target onset vs component flip [104]: line 3: 2.366667s vs 2.366667s
  Q10 PASS response fields and two-second limit [104]: line 3: key='f', rt='0.5843092762578408', timeout=0
  Q7 PASS saved response vs automatic key and RT [104]: line 3: 0.584309s vs 0.584309s, key 'f' vs 'f'
  Q4 PASS target removed on response or deadline [104]: line 3: target off 0.61667s after onset, RT 0.58431s
  Q3 PASS no main feedback [96]: line 12: '' vs ''
  Q10 PASS timeout referenced to target onset [2]: line 29: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q10 FAIL ten unmodified trial-list fields [1]: trials_p07.csv: 104 unmatched trial records; line 3: ('practice', '1', 'PW4') does not match all input fields
  Q1 UNDETERMINED further evidence [1]: need dialog and relative filename in the build
  Q3 UNDETERMINED further evidence [1]: need instruction wording, feedback messages and SPACE-only gates in the build
  Q4 UNDETERMINED further evidence [1]: need fixation glyph and contents of blank screens in the build
  Q5 UNDETERMINED further evidence [1]: need frame scheduling rule across refresh rates in the build
  Q6 UNDETERMINED further evidence [1]: need key mapping in instructions, ignored inputs and Escape handling in the build or a pilot
  Q7 UNDETERMINED further evidence [1]: need first-key selection, event clearing and clock-reset implementation
  Q8 UNDETERMINED further evidence [1]: need build code reading from stimulus objects
  Q9 UNDETERMINED further evidence [1]: need independent light sensor aligned to flip time for physical display onset
provided/output_files/file_D.csv
  Q1 PASS All 104 recorded trials match rows of trials_p02.csv on all ten input fields.
  Q2 PASS 104/104 trial identities from trials_p02.csv in exact file order (phase, trial_index, item_id).
  I1 UNDETERMINED interval log [1]: need matching file_D_frameIntervals.log
  I2 UNDETERMINED per-trial counts [1]: need dropped_frames
  Q3 PASS phase counts and order [1]: {'practice': 8, 'experimental': 96}
  Q3 PASS instructions SPACE response [1]: line 2: 'space' vs 'space'
  Q3 PASS break SPACE response [1]: line 11: 'space' vs 'space'
  Q3 PASS end screen duration [1]: line 108: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q3 PASS screen order [1]: row sequence compared with specification
  Q3 PASS practice feedback [8]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q5 PASS practice feedback frame count [8]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q4 PASS fixation [104]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q5 PASS fixation frame count [104]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q4 PASS prime [104]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q5 PASS prime frame count [104]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q4 PASS SOA [104]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q5 PASS SOA frames [104]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q4 PASS ITI [104]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q5 PASS ITI frame count [104]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q4 PASS fixation to prime transition [104]: line 3: 1.366667s vs 1.366667s
  Q4 FAIL prime recorded content [104]: line 3: 'prime' vs 'gravel'
  Q8 FAIL prime shown vs list [104]: line 3: 'prime' vs 'gravel'
  Q4 PASS target recorded content [104]: line 3: 'BLODGE' vs 'BLODGE'
  Q8 PASS target shown vs list [104]: line 3: 'BLODGE' vs 'BLODGE'
  Q6 PASS accepted recorded key [104]: line 3: 'f'
  Q10 PASS accuracy under participant mapping [104]: line 3: 1 vs 1
  Q7 PASS keyboard starts on target flip [104]: line 3: 1.516667s vs 1.516667s
  Q9 PASS prime onset vs component flip [104]: line 3: 1.366667s vs 1.366667s
  Q9 PASS target onset vs component flip [104]: line 3: 1.516667s vs 1.516667s
  Q10 PASS response fields and two-second limit [104]: line 3: key='f', rt='0.6164674831760522', timeout=0
  Q7 PASS saved response vs automatic key and RT [104]: line 3: 0.616467s vs 0.616467s, key 'f' vs 'f'
  Q4 PASS target removed on response or deadline [104]: line 3: target off 0.63333s after onset, RT 0.61647s
  Q3 PASS no main feedback [96]: line 12: '' vs ''
  Q10 PASS timeout referenced to target onset [4]: line 31: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q10 PASS ten unmodified trial-list fields [1]: All 104 recorded trials match rows of trials_p02.csv on all ten input fields.
  Q1 UNDETERMINED further evidence [1]: need dialog and relative filename in the build
  Q3 UNDETERMINED further evidence [1]: need instruction wording, feedback messages and SPACE-only gates in the build
  Q4 UNDETERMINED further evidence [1]: need fixation glyph and contents of blank screens in the build
  Q5 UNDETERMINED further evidence [1]: need frame scheduling rule across refresh rates in the build
  Q6 UNDETERMINED further evidence [1]: need key mapping in instructions, ignored inputs and Escape handling in the build or a pilot
  Q7 UNDETERMINED further evidence [1]: need first-key selection, event clearing and clock-reset implementation
  Q8 UNDETERMINED further evidence [1]: need build code reading from stimulus objects
  Q9 UNDETERMINED further evidence [1]: need independent light sensor aligned to flip time for physical display onset
provided/output_files/file_E.csv
  Q1 PASS All 104 recorded trials match rows of trials_p05.csv on all ten input fields.
  Q2 FAIL trials_p05.csv: 104 recorded, 104 expected; 0 missing, 0 excess. First difference at trial 1: expected ('practice', '1', 'PN2'), observed ('practice', '2', 'PW2').
  I1 UNDETERMINED interval log [1]: need matching file_E_frameIntervals.log
  I2 UNDETERMINED per-trial counts [1]: need dropped_frames
  Q3 PASS phase counts and order [1]: {'practice': 8, 'experimental': 96}
  Q3 PASS instructions SPACE response [1]: line 2: 'space' vs 'space'
  Q3 PASS break SPACE response [1]: line 11: 'space' vs 'space'
  Q3 PASS end screen duration [1]: line 108: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q3 PASS screen order [1]: row sequence compared with specification
  Q3 PASS practice feedback [8]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q5 PASS practice feedback frame count [8]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q4 PASS fixation [104]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q5 PASS fixation frame count [104]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q4 PASS prime [104]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q5 PASS prime frame count [104]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q4 PASS SOA [104]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q5 PASS SOA frames [104]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q4 PASS ITI [104]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q5 PASS ITI frame count [104]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q4 PASS fixation to prime transition [104]: line 3: 1.366667s vs 1.366667s
  Q4 PASS prime recorded content [104]: line 3: 'onion' vs 'onion'
  Q8 PASS prime shown vs list [104]: line 3: 'onion' vs 'onion'
  Q4 PASS target recorded content [104]: line 3: 'GARLIC' vs 'GARLIC'
  Q8 PASS target shown vs list [104]: line 3: 'GARLIC' vs 'GARLIC'
  Q6 PASS accepted recorded key [104]: line 3: 'f'
  Q10 PASS accuracy under participant mapping [104]: line 3: 1 vs 1
  Q7 PASS keyboard starts on target flip [104]: line 3: 1.516667s vs 1.516667s
  Q9 PASS prime onset vs component flip [104]: line 3: 1.366667s vs 1.366667s
  Q9 PASS target onset vs component flip [104]: line 3: 1.516667s vs 1.516667s
  Q10 PASS response fields and two-second limit [104]: line 3: key='f', rt='0.6260179830846937', timeout=0
  Q7 PASS saved response vs automatic key and RT [104]: line 3: 0.626018s vs 0.626018s, key 'f' vs 'f'
  Q4 PASS target removed on response or deadline [104]: line 3: target off 0.65000s after onset, RT 0.62602s
  Q3 PASS no main feedback [96]: line 12: '' vs ''
  Q10 PASS timeout referenced to target onset [1]: line 105: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q10 PASS ten unmodified trial-list fields [1]: All 104 recorded trials match rows of trials_p05.csv on all ten input fields.
  Q1 UNDETERMINED further evidence [1]: need dialog and relative filename in the build
  Q3 UNDETERMINED further evidence [1]: need instruction wording, feedback messages and SPACE-only gates in the build
  Q4 UNDETERMINED further evidence [1]: need fixation glyph and contents of blank screens in the build
  Q5 UNDETERMINED further evidence [1]: need frame scheduling rule across refresh rates in the build
  Q6 UNDETERMINED further evidence [1]: need key mapping in instructions, ignored inputs and Escape handling in the build or a pilot
  Q7 UNDETERMINED further evidence [1]: need first-key selection, event clearing and clock-reset implementation
  Q8 UNDETERMINED further evidence [1]: need build code reading from stimulus objects
  Q9 UNDETERMINED further evidence [1]: need independent light sensor aligned to flip time for physical display onset
provided/output_files/file_F.csv
  Q1 PASS All 104 recorded trials match rows of trials_p08.csv on all ten input fields.
  Q2 PASS 104/104 trial identities from trials_p08.csv in exact file order (phase, trial_index, item_id).
  I1 UNDETERMINED interval log [1]: need matching file_F_frameIntervals.log
  I2 UNDETERMINED per-trial counts [1]: need dropped_frames
  Q3 PASS phase counts and order [1]: {'practice': 8, 'experimental': 96}
  Q3 PASS instructions SPACE response [1]: line 2: 'space' vs 'space'
  Q3 PASS break SPACE response [1]: line 11: 'space' vs 'space'
  Q3 PASS end screen duration [1]: line 108: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q3 PASS screen order [1]: row sequence compared with specification
  Q3 PASS practice feedback [8]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q5 PASS practice feedback frame count [8]: line 3: 60.00 elapsed frames, expected 60; elapsed estimate at rounded Hz
  Q4 PASS fixation [104]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q5 PASS fixation frame count [104]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q4 PASS prime [104]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q5 PASS prime frame count [104]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q4 PASS SOA [104]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q5 PASS SOA frames [104]: line 3: 9.00 elapsed frames, expected 9; elapsed estimate at rounded Hz
  Q4 PASS ITI [104]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q5 PASS ITI frame count [104]: line 3: 30.00 elapsed frames, expected 30; elapsed estimate at rounded Hz
  Q4 PASS fixation to prime transition [104]: line 3: 1.366667s vs 1.366667s
  Q4 PASS prime recorded content [104]: line 3: 'cloth' vs 'cloth'
  Q8 PASS prime shown vs list [104]: line 3: 'cloth' vs 'cloth'
  Q4 PASS target recorded content [104]: line 3: 'VELVET' vs 'VELVET'
  Q8 PASS target shown vs list [104]: line 3: 'VELVET' vs 'VELVET'
  Q6 PASS accepted recorded key [104]: line 3: 'j'
  Q10 PASS accuracy under participant mapping [104]: line 3: 1 vs 1
  Q7 FAIL keyboard starts on target flip [104]: line 3: 0.866667s vs 1.516667s
  Q9 PASS prime onset vs component flip [104]: line 3: 1.366667s vs 1.366667s
  Q9 PASS target onset vs component flip [104]: line 3: 1.516667s vs 1.516667s
  Q10 PASS response fields and two-second limit [104]: line 3: key='j', rt='1.2666782862236232', timeout=0
  Q7 PASS saved response vs automatic key and RT [104]: line 3: 1.266678s vs 1.266678s, key 'j' vs 'j'
  Q4 FAIL target removed on response or deadline [54]: line 3: target off 0.65000s after onset, RT 1.26668s
  Q4 PASS target removed on response or deadline [50]: line 5: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q10 PASS timeout referenced to target onset [50]: line 5: 120.00 elapsed frames, expected 120; elapsed estimate at rounded Hz
  Q3 PASS no main feedback [96]: line 12: '' vs ''
  Q10 PASS ten unmodified trial-list fields [1]: All 104 recorded trials match rows of trials_p08.csv on all ten input fields.
  Q1 UNDETERMINED further evidence [1]: need dialog and relative filename in the build
  Q3 UNDETERMINED further evidence [1]: need instruction wording, feedback messages and SPACE-only gates in the build
  Q4 UNDETERMINED further evidence [1]: need fixation glyph and contents of blank screens in the build
  Q5 UNDETERMINED further evidence [1]: need frame scheduling rule across refresh rates in the build
  Q6 UNDETERMINED further evidence [1]: need key mapping in instructions, ignored inputs and Escape handling in the build or a pilot
  Q7 UNDETERMINED further evidence [1]: need first-key selection, event clearing and clock-reset implementation
  Q8 UNDETERMINED further evidence [1]: need build code reading from stimulus objects
  Q9 UNDETERMINED further evidence [1]: need independent light sensor aligned to flip time for physical display onset
```

</details>

## 4. Reconciliation

1. The instruction wording stayed open for all six files as predicted. The
recorded SPACE identifies an accepted key but not the words shown or all
keys the screen would reject. The final checker also needs build evidence
for stimulus-object provenance, clearing early keys, scheduling at other
rates and the contents of blank screens. Actual physical onset still needs
a light sensor.
2. The predicted count was three of the four A5-passing files. The new
checks identify A, D and F. B passes its testable parts.

   **Cell-level differences.** A/Q6 passes the narrow recorded-key test
predicted in the table (all accepted responses are F/J), but the automatic
scoring also contradicts the required mapping on 97 trials. C/Q10 was
predicted to pass. Its recorded inputs came from the wrong participant's
list, so they fail the unchanged-input requirement against list 7. F/Q4
was predicted to fail the response window. Its visible target duration
passes when measured against the actual keyboard event; the shortened
listening window fails Q7/Q10. D's prime field fails Q4/Q8 as predicted.
The other checkable cell parts agree under these definitions. The shared
UNDETERMINED implementation details in section 3 qualify every relevant
cell, even when its observable parts passed.
3. I predicted 120 Hz. The measured rates were 120.250 Hz in run 7 and 120.069 Hz in run 8. Both round to 120, giving the predicted 60-frame fixation and ITI, 18-frame prime and short SOA, 120-frame feedback and long SOA, and 240-frame end screen. Run 7 met all the elapsed targets. Run 8 used the same frame settings, with the longer intervals detailed in section 2.
4. The expected all-pass verdict missed the final-poll bug described in
section 1. A frame-counted loop can finish preparing the next display before
the current target frame has finished. The final check must still collect
queued key events through the deadline.
5. I predicted zero drops in run 7 and two in run 8, mainly at target onset. Run 7 had zero. Run 8 had 133, with just one interval ending on target onset. I underestimated both how often a refresh could run long and how widely that could occur throughout a trial. A late flip extends whichever image is currently displayed. The logs locate it in time, but cannot identify which application or system operation delayed each flip.
6. The predicted longer prime and SOA follow from how this build counts
frame iterations. A late refresh inside the prime leaves its image up for
longer and pushes later scheduled flips back. In the human video run, practice trial 6 provided a direct example. Both the prime and its short SOA lasted approximately 175 ms (21 periods at 120 Hz), even though each covered the planned 18 recorded flip intervals.
7. Fixation duration, prime duration and SOA can be compared on the flip
clock. Nearest-frame rounding bounds the *scheduled* error under the
assumptions in section 2. Photodiode data would be needed to verify actual
screen onset.
