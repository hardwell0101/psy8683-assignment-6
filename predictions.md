# Predictions and reconciliation (Part D)

Fill in **Predictions** before your first complete run, and commit this file
with a message that starts `predictions:`. Do not edit the Predictions
section after that commit; the history is how it is read. Then run the
experiment and fill in **Reconciliation**.

You are graded on the reconciliation, not on being right.

## Predictions

Answer for your own build, as participant 3.

1. How many rows will the output file have? How many of them will be trials?
   What will the other rows be?

   I expect 105 data rows, excluding the header. Of those, 104 will be trials (8 practice and 96 main), and one will record the instructions screen and the SPACE press.

2. Will any column name appear more than once? If so, which, and what will
   each copy hold on a trial row?

   I expect `participant` to appear twice. On a trial row, I’d expect both copies to show `3`, one from the trial list and one from the experiment dialog.

3. On an SOA 150 trial, what will `target_onset - prime_onset` be, in
   milliseconds and in frames, on the machine you are using? On an SOA 1000
   trial?

   Assuming a 60 Hz screen, I expect the target to appear 150 ms (9 frames) after the prime appears in the short condition and 1000 ms (60 frames) after it appears in the long condition.

4. What will the median `rt` be, roughly, and what proportion of trials will
   be timeouts?

   I’d guess a median reaction time of 650 ms from target onset, with about 1% of trials timing out.

5. On a trial whose prime is `smoke` and whose target is `pepper`, what will
   `prime_shown` and `target_shown` hold, exactly?

   `prime_shown` = `smoke` and `target_shown` = `PEPPER`.

## Reconciliation

For each prediction: what you got, and if it differs, why. "I was wrong" is
not a reason. Name the mechanism: what PsychoPy, your build, or your machine
did that you did not expect.

1.

2.

3.

4.

5.
