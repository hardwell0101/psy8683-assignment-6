# Run 7 data dictionary

The CSV has 107 data rows. In order, these are the opening instructions, eight practice trials, the break, 96 experimental trials and the end screen. Trial timestamps in seconds use PsychoPy’s run clock. Keyboard RTs use a clock reset for the corresponding screen. A display flip records when the software presented a frame. Physical light onset requires an independent measurement.

Positions below follow the exported header, including both participant fields. “Trials” means all 104 trials. “Empty” means no row had a value in this run. The literal string `None` in a key-duration column counts as a recorded value.

| Position | Column | Source | Meaning | Units or values | Populated rows in run 7 |
| ---: | --- | --- | --- | --- | --- |
| 1 | `participant` | Trial list | Participant field among the ten list columns. At export the startup ID occupies the same dictionary key. | integer ID, 7 | Every row |
| 2 | `phase` | Trial list | Block to which the planned item belongs. | practice / experimental | Trials |
| 3 | `trial_index` | Trial list | Position within its block, starting at one. | 1–8 / 1–96 | Trials |
| 4 | `item_id` | Trial list | Item identifier in the canonical list. | text, e.g. PW1 | Trials |
| 5 | `target` | Trial list | Planned lexical-decision string, before the build capitalizes it. | lowercase text | Trials |
| 6 | `prime` | Trial list | Planned cue shown before the target. | lowercase text | Trials |
| 7 | `relatedness` | Trial list | Relationship condition assigned to the pair. | related / unrelated / none | Trials |
| 8 | `soa` | Trial list | Planned interval from prime onset to target onset. | 150 or 1000 ms | Trials |
| 9 | `correct_response` | Trial list | Correct lexical category of the target. | word / nonword | Trials |
| 10 | `seed` | Trial list | Seed recorded by the list generator. The loops replay the resulting order. | integer, 8683 here | Trials |
| 11 | `thisN` | PsychoPy automatic | Trial count across repetitions of this loop. | zero-based index | Trials |
| 12 | `thisTrialN` | PsychoPy automatic | Trial position in the current repetition. | zero-based index | Trials |
| 13 | `thisRepN` | PsychoPy automatic | Current repetition of this loop. | zero-based, 0 here | Trials |
| 14 | `decision.keys` | PsychoPy automatic | Key accepted for the target response. | f / j | Trials |
| 15 | `decision.rt` | PsychoPy automatic | Key-down time relative to the target-onset flip. Keyboard event time. | seconds | Trials |
| 16 | `decision.duration` | PsychoPy automatic | Time from key-down to release when available. Run 7 stored the literal None because responses were collected on press. | seconds or None | Trials |
| 17 | `practice_loop.thisRepN` | PsychoPy automatic | Current repetition of this loop. | zero-based, 0 here | Practice |
| 18 | `practice_loop.thisTrialN` | PsychoPy automatic | Trial position in the current repetition. | zero-based index | Practice |
| 19 | `practice_loop.thisN` | PsychoPy automatic | Trial count across repetitions of this loop. | zero-based index | Practice |
| 20 | `practice_loop.thisIndex` | PsychoPy automatic | Index in the subset loaded by this loop. | zero-based index | Practice |
| 21 | `main_loop.thisRepN` | PsychoPy automatic | Current repetition of this loop. | zero-based, 0 here | Experimental |
| 22 | `main_loop.thisTrialN` | PsychoPy automatic | Trial position in the current repetition. | zero-based index | Experimental |
| 23 | `main_loop.thisN` | PsychoPy automatic | Trial count across repetitions of this loop. | zero-based index | Experimental |
| 24 | `main_loop.thisIndex` | PsychoPy automatic | Index in the subset loaded by this loop. | zero-based index | Experimental |
| 25 | `thisRow.t` | PsychoPy automatic | First flip after the loop starts the trial row. It equals fixation onset here. | s, flip | Trials |
| 26 | `notes` | PsychoPy automatic | Reserved experiment notes field. No notes were entered. | free text | Empty |
| 27 | `piloting` | PsychoPy automatic | Whether PsychoPy used Pilot mode for the session. | boolean, False here | Instructions |
| 28 | `instructions.started` | PsychoPy automatic | Time the program enters the instructions routine, read from its global clock. | s, non-flip | Instructions |
| 29 | `instructionText.started` | PsychoPy automatic | Flip on which the opening instructions appears. | s, display flip | Instructions |
| 30 | `beginKey.started` | PsychoPy automatic | Flip on which the keyboard starts accepting responses for the instructions. | s, keyboard-start flip | Instructions |
| 31 | `instructions.stopped` | PsychoPy automatic | Time the program leaves the instructions routine, read from its global clock. | s, non-flip | Instructions |
| 32 | `beginKey.keys` | PsychoPy automatic | Key accepted for the start of practice. | space | Instructions |
| 33 | `beginKey.rt` | PsychoPy automatic | Key-down time relative to the opening flip of this screen. Keyboard event time. | seconds | Instructions |
| 34 | `beginKey.duration` | PsychoPy automatic | Time from key-down to release when available. Run 7 stored the literal None because responses were collected on press. | seconds or None | Instructions |
| 35 | `trial.started` | PsychoPy automatic | Time the program enters the trial routine, read from its global clock. | s, non-flip | Trials |
| 36 | `fixation.started` | PsychoPy automatic | Flip on which the fixation cross appears. | s, display flip | Trials |
| 37 | `fixation.stopped` | PsychoPy automatic | Flip on which the fixation cross disappears. | s, display flip | Trials |
| 38 | `prime_text.started` | PsychoPy automatic | Flip on which the prime appears. | s, display flip | Trials |
| 39 | `prime_text.stopped` | PsychoPy automatic | Flip on which the prime disappears. | s, display flip | Trials |
| 40 | `target_text.started` | PsychoPy automatic | Flip on which the uppercase target appears. | s, display flip | Trials |
| 41 | `decision.started` | PsychoPy automatic | Flip on which the keyboard starts accepting responses for the target. | s, keyboard-start flip | Trials |
| 42 | `trial.stopped` | PsychoPy automatic | Time the program leaves the trial routine, read from its global clock. | s, non-flip | Trials |
| 43 | `dropped_frames` | Code: trialTiming | Trial intervals strictly longer than 1.5 nominal frame periods. | count, 0 here | Trials |
| 44 | `recorded_intervals` | Code: trialTiming | Number of successive flip intervals contributed by this trial to the companion log. | count | Trials |
| 45 | `trial_last_flip` | Code: trialTiming | Global flip time for the last frame drawn in the trial recording window. | s, display flip | Trials |
| 46 | `practice_loop.decision.keys` | PsychoPy automatic | Key accepted for the practice target response. | f / j | Practice |
| 47 | `practice_loop.decision.rt` | PsychoPy automatic | Key-down time relative to the target-onset flip. Keyboard event time. | seconds | Practice |
| 48 | `practice_loop.decision.duration` | PsychoPy automatic | Time from key-down to release when available. Run 7 stored the literal None because responses were collected on press. | seconds or None | Practice |
| 49 | `key` | Code: scoreTrial | First valid key for this target. Empty for a timeout. | f / j | Trials |
| 50 | `rt` | Code: scoreTrial | Event time relative to the target-onset flip for that key. Empty for a timeout. | seconds | Trials |
| 51 | `accuracy` | Code: scoreTrial | Whether the key matches the category under the participant’s assigned mapping. Timeouts count as errors. | 1 correct / 0 incorrect | Trials |
| 52 | `timeout` | Code: scoreTrial | Whether the two-second window ended without a valid response. | 1 yes / 0 no | Trials |
| 53 | `prime_shown` | Code: scoreTrial | Text read from the prime stimulus object at trial end. | lowercase text | Trials |
| 54 | `target_shown` | Code: scoreTrial | Text read from the target stimulus object at trial end. | uppercase text | Trials |
| 55 | `prime_onset` | Code: scoreTrial | Copy of the prime text’s automatic start-flip timestamp. | s, display flip | Trials |
| 56 | `target_onset` | Code: scoreTrial | Copy of the target text’s automatic start-flip timestamp. | s, display flip | Trials |
| 57 | `feedback.started` | PsychoPy automatic | Time the program enters the feedback routine, read from its global clock. | s, non-flip | Practice |
| 58 | `feedbackText.started` | PsychoPy automatic | Flip on which the practice feedback appears. | s, display flip | Practice |
| 59 | `feedbackText.stopped` | PsychoPy automatic | Flip on which the practice feedback disappears. | s, display flip | Practice |
| 60 | `feedback.stopped` | PsychoPy automatic | Time the program leaves the feedback routine, read from its global clock. | s, non-flip | Practice |
| 61 | `interval.started` | PsychoPy automatic | Time the program enters the interval routine, read from its global clock. | s, non-flip | Trials |
| 62 | `blankScreen.started` | PsychoPy automatic | Flip on which the blank ITI display appears. | s, display flip | Trials |
| 63 | `blankScreen.stopped` | PsychoPy automatic | Flip on which the blank ITI display disappears. | s, display flip | Trials |
| 64 | `interval.stopped` | PsychoPy automatic | Time the program leaves the interval routine, read from its global clock. | s, non-flip | Trials |
| 65 | `rest.started` | PsychoPy automatic | Time the program enters the rest routine, read from its global clock. | s, non-flip | Break |
| 66 | `breakText.started` | PsychoPy automatic | Flip on which the break message appears. | s, display flip | Break |
| 67 | `resumeKey.started` | PsychoPy automatic | Flip on which the keyboard starts accepting responses for the break message. | s, keyboard-start flip | Break |
| 68 | `rest.stopped` | PsychoPy automatic | Time the program leaves the rest routine, read from its global clock. | s, non-flip | Break |
| 69 | `resumeKey.keys` | PsychoPy automatic | Key accepted for the end of the break. | space | Break |
| 70 | `resumeKey.rt` | PsychoPy automatic | Key-down time relative to the opening flip of this screen. Keyboard event time. | seconds | Break |
| 71 | `resumeKey.duration` | PsychoPy automatic | Time from key-down to release when available. Run 7 stored the literal None because responses were collected on press. | seconds or None | Break |
| 72 | `main_loop.decision.keys` | PsychoPy automatic | Key accepted for the main target response. | f / j | Experimental |
| 73 | `main_loop.decision.rt` | PsychoPy automatic | Key-down time relative to the target-onset flip. Keyboard event time. | seconds | Experimental |
| 74 | `main_loop.decision.duration` | PsychoPy automatic | Time from key-down to release when available. Run 7 stored the literal None because responses were collected on press. | seconds or None | Experimental |
| 75 | `endScreen.started` | PsychoPy automatic | Time the program enters the endScreen routine, read from its global clock. | s, non-flip | End screen |
| 76 | `endText.started` | PsychoPy automatic | Flip on which the end message appears. | s, display flip | End screen |
| 77 | `endText.stopped` | PsychoPy automatic | Flip on which the end message disappears. | s, display flip | End screen |
| 78 | `endScreen.stopped` | PsychoPy automatic | Time the program leaves the endScreen routine, read from its global clock. | s, non-flip | End screen |
| 79 | `participant` | Startup dialog | Participant number from experiment metadata, repeated on each row. | integer ID, 7 | Every row |
| 80 | `session` | Startup dialog | Session label supplied at startup. Preserve leading zeros. | text, 001 | Every row |
| 81 | `date` | PsychoPy automatic | Local date and time refreshed at the start of the run. The filename uses an earlier setup timestamp. | date-time string, non-flip | Every row |
| 82 | `expName` | PsychoPy automatic | Experiment name from the build. | ldt | Every row |
| 83 | `expVersion` | PsychoPy automatic | Optional experiment version from the build. | blank here | Empty |
| 84 | `psychopyVersion` | PsychoPy automatic | Version written by the running experiment. | 2026.2.2 | Every row |
| 85 | `frameRate` | PsychoPy automatic | Refresh rate estimated during fullscreen window setup. | Hz, 120.04609774509024 | Every row |
| 86 | `expStart` | PsychoPy automatic | Wall-clock date and time of the start synchronization, including UTC offset. PsychoPy reads this string after the synchronization flip. | local date-time string, non-flip sample | Every row |
| 87 | *(unnamed)* | PsychoPy automatic | Empty field produced by the trailing comma on every exported line. | empty | Empty |

Both participant columns have the literal header `participant`. PsychoPy updates the row with startup metadata and writes the same row key twice. Matching values cannot independently prove which list was loaded. The checker reads by column position, retains both values, and compares the ten list fields with the canonical list for the expected participant. A plain Python `csv.DictReader` exposes only the last copy under that name.

No run 7 trial timed out. The response normally ended the routine before Builder recorded a separate target or keyboard stop. A timeout can introduce `target_text.stopped` (target-removal flip) and `decision.stopped` (keyboard-stop flip). The first replacement stimulus provides the visible offset when the target-stop field is absent. Key and RT can be empty when a trial times out.

## Frame intervals

The paired file has the CSV basename followed by `_frameIntervals.log`. It contains one comma-separated sequence of positive durations in seconds, in presentation order. Within each trial, the first interval begins at the fixation flip and the last ends at the last flip displaying the target. The interval that crosses into the next routine is excluded. Instructions, feedback, ITIs, the break and the end screen contribute no intervals.

In run 7 there are 21,199 intervals. Take the next `recorded_intervals` values for each trial row. Their sum reproduces `trial_last_flip − fixation.started`. Count entries in each slice greater than `1.5 / round(frameRate)`, or 12.5 ms here. The slice count matches `dropped_frames` on all 104 rows. Both whole-run totals are zero.

## Component names in the six supplied files

The supplied keyboard is `key_resp`, with loop copies under `practice.key_resp` and `experiment.key_resp`. Those files include automatic `.corr` fields. The matching keyboard in run 7 is `decision`; accuracy in this build comes from `scoreTrial`. The supplied files use `instr_text_stim/instr_key` for instructions, `feedback_text` for feedback, `iti/blank` for the interval, `break_screen/break_text/break_key` for the break, and `end_screen/end_text` for the end. Fixation, prime and target retain the same component names. A routine’s start or stop and its stimulus flip describe different events.
