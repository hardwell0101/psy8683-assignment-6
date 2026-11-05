# Verification report and timing audit (Part C)

## 1. Your Assignment 5 build against Q3–Q10

Paste your checker's output for participants 3 and 6.

```
(paste here)
```

For each property that is not PASS:

- **PILOT:** how you established it. What you watched for or read in the
  build, and what would have counted as a failure.
- **UNDETERMINED:** why the file cannot settle it, and what you did to
  settle it. If it is still open, say what would settle it.
- **FAIL:** what was wrong, the commit that fixed it (`fix:`), and the
  verdict on runs 7 and 8, which are made with the fixed build. Do not rerun
  participants 3 or 6.

## 2. Timing audit

### The machine

| | Run 7 | Run 8 |
| --- | --- | --- |
| Computer and OS | | |
| Display, and its refresh rate in the OS settings | | |
| Full screen? | | |
| PsychoPy version | | |
| `frameRate` in the file | | |
| Other load | nothing | muted video in a browser |

### Achieved timing

For runs 7 and 8: for each event in Q3 and Q4 that runs for a fixed number
of frames, the frame count Q5 asks for and the distribution you got. Then
the dropped-frame totals from I2, and the longest interval in the I1 log.

| Event | Q5 frames | Run 7 | Run 8 |
| --- | --- | --- | --- |
| fixation | | | |
| prime | | | |
| prime to target, SOA 150 | | | |
| prime to target, SOA 1000 | | | |
| ITI | | | |
| feedback | | | |
| end screen | | | |
| `dropped_frames` total | | | |
| longest logged interval (ms) | | | |

For every trial whose count differs from Q5: was a dropped frame recorded on
that trial? If not, what else explains it? Some events happen outside the
I1 recording window. Say which, and what that means for explaining their
deviations.

Does your I2 total equal the number of intervals over 1.5 frames in your I1
log? If not, find out why before you go on.

### Three bins

Sort every timing claim in Q4, Q5, Q7, Q9, and Q10 into one of three bins.
Two or three sentences each.

- **Verified from software time stamps.** What the stamps show, and what
  they assume.
- **Bounded, not verified.** What you can say, the bound, and what it
  depends on. Include what your build would do at 60, 75, 120, and 144 Hz,
  and how you know.
- **Not reachable without hardware.** What would reach it.

## 3. The six provided files

Paste your checker's output on all six.

```
(paste here)
```

For each file:

### file_A

- Verdicts on Q3–Q10:
- What the person who built it most likely did in Builder:
- What a researcher analyzing this file, without your checker, would have
  concluded:
- Which properties stay UNDETERMINED, and what would settle each:

### file_B

- Verdicts on Q3–Q10:
- What the person who built it most likely did in Builder:
- What a researcher would have concluded:
- Which properties stay UNDETERMINED, and what would settle each:

### file_C

- Verdicts on Q3–Q10:
- What the person who built it most likely did in Builder:
- What a researcher would have concluded:
- Which properties stay UNDETERMINED, and what would settle each:

### file_D

- Verdicts on Q3–Q10:
- What the person who built it most likely did in Builder:
- What a researcher would have concluded:
- Which properties stay UNDETERMINED, and what would settle each:

### file_E

- Verdicts on Q3–Q10:
- What the person who built it most likely did in Builder:
- What a researcher would have concluded:
- Which properties stay UNDETERMINED, and what would settle each:

### file_F

- Verdicts on Q3–Q10:
- What the person who built it most likely did in Builder:
- What a researcher would have concluded:
- Which properties stay UNDETERMINED, and what would settle each:

### Your first checker on the six files

Run your first working Q3–Q10 checker on the six files before you look at
them by hand, and commit that output with a message that starts
`first-run:` (paste it here too). Then, as in A5:
for any wrong verdict, in either direction, what your check was actually
testing and what you changed, with the fix in its own commit. If all six
came out right, say for each file which of your checks could have failed on
it, and whether it did.

### What A5 could and could not see

Some of these files passed everything you checked in A5. For each one that
fails now, name the A5 check that came closest to catching it and say why
it didn't.

## 4. Reconciliation

For each numbered prediction in `a6_predictions.md`, and for each cell in
the provided-files table you got wrong: what you got, and the mechanism
behind any difference. "I was wrong" is not a mechanism. Name what
PsychoPy, the build, or the machine did that you did not expect.
