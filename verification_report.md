# Verification report (Part C)

## Your own runs

Paste your checker's output for participants 3 and 6. 

```
(paste here)
```

For each property marked PILOT, say how you established it: what you watched
for, and what would have counted as a failure.

For any FAIL: what was wrong, what you changed, and the commit that fixed it.
If you fixed it, rerun and paste the new output too.

## The six provided files

Each of `provided/output_files/file_A.csv` … `file_F.csv` came from a
different build of this task, run by a different participant (the number is
in the file). They were generated from the lists in
`provided/canonical_trial_lists/`. Some builds may be broken and some may
not; do not assume a count in either direction.

For each file, answer three things. Two or three sentences each.

### file_A

- Verdicts (paste your checker's output, or summarize it):
- What the person who built it most likely did in Builder:
- What a researcher analyzing this file, without your checker, would have
  concluded:

### file_B

- Verdicts:
- What the person who built it most likely did in Builder:
- What a researcher analyzing this file would have concluded:

### file_C

- Verdicts:
- What the person who built it most likely did in Builder:
- What a researcher analyzing this file would have concluded:

### file_D

- Verdicts:
- What the person who built it most likely did in Builder:
- What a researcher analyzing this file would have concluded:

### file_E

- Verdicts:
- What the person who built it most likely did in Builder:
- What a researcher analyzing this file would have concluded:

### file_F

- Verdicts:
- What the person who built it most likely did in Builder:
- What a researcher analyzing this file would have concluded:

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
