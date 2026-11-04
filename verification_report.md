# Verification report

## Own runs

Both submitted final CSVs contain 107 data rows. There are 8 practice and 96 experimental trials, plus the instructions, break and end-screen rows. The `piloting` flag is false for both runs. Participant 1's Pilot-mode output is preserved separately in the pre-handoff commit.

**Q1 PILOT.** Both runs used the desktop startup dialog. The root Builder file was reopened, and the compiled script was checked for the relative filename expression that pads the number to two digits. An earlier run labeled 6 illustrates why this check matters: the older draft loaded participant 1's file, and all 104 trials matched participant 1 when the dialog ID was excluded from the comparison. That run was set aside. The replacement script uses the participant-dependent path in both loops. The accepted CSVs agree with participants 3 and 6 on every input field and row position.

```text
data/3_ldt_2026-11-04_12h44.45.576.csv
  Q1 PASS  All 104 recorded trials match rows of trials_p03.csv on all ten input fields.
  Q1 PILOT Observe the startup entry and confirm the root ldt.psyexp loads the relative two-digit filename. A CSV cannot prove the typed value, file location, or loader implementation.
  Q2 PASS  104/104 trial identities from trials_p03.csv in exact file order (phase, trial_index, item_id).
data/6_ldt_2026-11-04_12h59.17.668.csv
  Q1 PASS  All 104 recorded trials match rows of trials_p06.csv on all ten input fields.
  Q1 PILOT Observe the startup entry and confirm the root ldt.psyexp loads the relative two-digit filename. A CSV cannot prove the typed value, file location, or loader implementation.
  Q2 PASS  104/104 trial identities from trials_p06.csv in exact file order (phase, trial_index, item_id).
```

**Timing and scoring observations.** The full-screen runs measured 120.042 Hz (participant 3) and 119.657 Hz (participant 6). Both round to 120 Hz. In each run the timestamps show 52 short prime-to-target intervals of 18 frames and 52 long intervals of 120 frames, rounded to the nearest frame. The prime lasted 18 frames, practice feedback lasted 120, and the blank between trials lasted 60. The saved target onset matched the keyboard start time on every trial. Scoring the recorded keys independently with the assigned mapping reproduced every accuracy flag.

| Participant | Word / nonword keys | Correct | Incorrect key | Timeout | Median RT for responses |
| --- | --- | ---: | ---: | ---: | ---: |
| 3 | F / J | 48 | 55 | 1 | 267 ms |
| 6 | J / F | 16 | 88 | 0 | 632 ms |

## Six supplied runs

Q1 compares the recorded participant and ten input fields with the expected
canonical list. Q2 compares the ordered sequence of (phase, trial_index,
item_id), including missing or repeated trials. For all six files, the literal
startup entry, experiment path, and file-loading method remain PILOT. None of
those actions can be established from the CSV alone.

The first checker results appear at the end of this report and in commit
`7bdb1c6`. After that commit, the trial records were compared with all eight
canonical lists, both by row position and without regard to order. The extra
checks on scoring, displayed text and timestamps below are observations about
the six builds. They are separate from the Q1 and Q2 verdicts.

### File A, participant 3

**Q1 PASS, Q2 PASS.** All 104 input rows match participant 3 in order. Scoring
is the problem: both `accuracy` and `key_resp.corr` are zero on every trial,
although 97 responses match the required odd-participant key mapping. The
correct-answer setting may have compared physical keys with the category names
`word` and `nonword`. Reading the stored accuracy would give 0/104 correct
instead of 97/104 and could lead a researcher to exclude the run.

### File B, participant 4

**Q1 PASS, Q2 PASS.** All 104 rows match participant 4 in order. The recorded
primes and uppercase targets agree with the list, the two measured SOAs match
their labels, the keyboard starts with the target, and recalculating the
even-participant key mapping reproduces the 100 correct trials. A sequential
loop and target-triggered keyboard are consistent with these records. A
researcher would get the same trial assignments and accuracy when analyzing
the recorded fields; the file does not establish what the instructions said.

### File C, participant 7

**Q1 FAIL, Q2 FAIL against the required participant-7 list.** Both participant
columns say 7. Dropping that ID for comparison, all 104 rows match participant
1's canonical list in its original order. The first practice item is PW4
instead of the expected PW3. A loop fixed to the participant-1 conditions file
would explain the evidence. There is no evidence of a separate shuffle. An
analyst using the participant ID to join the planned design would assign the
wrong item or condition and count participant 7's counterbalancing list as
delivered.

### File D, participant 2

**Q1 PASS, Q2 PASS.** The input columns match all 104 intended trials in order,
but `prime_shown` says `prime` on every trial, including the first trial, whose
input prime is `gravel`. Entering the literal word in the prime Text field
instead of binding it to the list variable would produce that pattern. If the
shown-text field accurately reflects the stimulus object, a researcher relying
on the planned prime or relatedness column would analyze a priming manipulation
the build never presented. The CSV alone cannot rule out an error in the
shown-text logging itself.

### File E, participant 5

**Q1 PASS, Q2 FAIL.** All 104 participant-5 rows occur exactly once, but 103 are
in a different position. The first two practice indices are 2 and 3. A random
loop within each phase would preserve counts while changing order. The longest
experimental run of one response category is five trials. A researcher checking
only cell counts would miss the violation of the planned maximum of three.

### File F, participant 8

**Q1 PASS, Q2 PASS.** All 104 participant-8 rows match in order. On every trial
the keyboard starts at fixation, 650 ms before the short-SOA target and 1500 ms
before the long-SOA target. On all 50 timeouts the keyboard closes 2000 ms after
it opens, and all 50 occur on the long SOA. Starting its clock and response
window at the beginning of the trial explains both the inflated RTs and the
500 ms left to respond after a long-SOA target. The apparent long-SOA slowing
and timeout excess would mix response-window settings with participant behavior.

## Assessment of the first checker

The independent list comparisons reproduced all six first verdict pairs for
Q1 and Q2. For A, B, D and F, a foreign input row would have failed Q1 and a
swapped or repeated trial would have failed Q2. Neither occurred. C failed both
comparisons because the recorded sequence was from another participant's list.
E passed the membership comparison and failed the order comparison. The other
faults observed in A, D and F concern properties outside this assignment's
checker scope. No Q1 or Q2 verdict required correction.

## Your first checker on the six files

Command: `python3 check_output.py provided/output_files/file_*.csv --lists provided/canonical_trial_lists`

First output, recorded before manual inspection of any supplied file:

```text
provided/output_files/file_A.csv
  Q1 PASS  All 104 recorded trials match rows of trials_p03.csv on all ten input fields.
  Q1 PILOT Observe the startup entry and confirm the root ldt.psyexp loads the relative two-digit filename. A CSV cannot prove the typed value, file location, or loader implementation.
  Q2 PASS  104/104 trial identities from trials_p03.csv in exact file order (phase, trial_index, item_id).
provided/output_files/file_B.csv
  Q1 PASS  All 104 recorded trials match rows of trials_p04.csv on all ten input fields.
  Q1 PILOT Observe the startup entry and confirm the root ldt.psyexp loads the relative two-digit filename. A CSV cannot prove the typed value, file location, or loader implementation.
  Q2 PASS  104/104 trial identities from trials_p04.csv in exact file order (phase, trial_index, item_id).
provided/output_files/file_C.csv
  Q1 FAIL  trials_p07.csv: 104 unmatched trial records; line 3: ('practice', '1', 'PW4') does not match all input fields
  Q1 PILOT Observe the startup entry and confirm the root ldt.psyexp loads the relative two-digit filename. A CSV cannot prove the typed value, file location, or loader implementation.
  Q2 FAIL  trials_p07.csv: 104 recorded, 104 expected; 104 missing, 104 excess. First difference at trial 1: expected ('practice', '1', 'PW3'), observed ('practice', '1', 'PW4').
provided/output_files/file_D.csv
  Q1 PASS  All 104 recorded trials match rows of trials_p02.csv on all ten input fields.
  Q1 PILOT Observe the startup entry and confirm the root ldt.psyexp loads the relative two-digit filename. A CSV cannot prove the typed value, file location, or loader implementation.
  Q2 PASS  104/104 trial identities from trials_p02.csv in exact file order (phase, trial_index, item_id).
provided/output_files/file_E.csv
  Q1 PASS  All 104 recorded trials match rows of trials_p05.csv on all ten input fields.
  Q1 PILOT Observe the startup entry and confirm the root ldt.psyexp loads the relative two-digit filename. A CSV cannot prove the typed value, file location, or loader implementation.
  Q2 FAIL  trials_p05.csv: 104 recorded, 104 expected; 0 missing, 0 excess. First difference at trial 1: expected ('practice', '1', 'PN2'), observed ('practice', '2', 'PW2').
provided/output_files/file_F.csv
  Q1 PASS  All 104 recorded trials match rows of trials_p08.csv on all ten input fields.
  Q1 PILOT Observe the startup entry and confirm the root ldt.psyexp loads the relative two-digit filename. A CSV cannot prove the typed value, file location, or loader implementation.
  Q2 PASS  104/104 trial identities from trials_p08.csv in exact file order (phase, trial_index, item_id).
```
