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

1. The CSV has 107 data rows. The predicted 104 trials were present. Builder also wrote one row each for the instructions, break, and end screen. Practice feedback and the blank interval stayed on the trial row inside each loop iteration.

2. Only `participant` appears twice. Both cells read `3` on every trial. Builder includes the trial-parameter name and then appends the experiment-info names to the header. PsychoPy merges the dialog values into each row and writes both cells by looking up the same key. The two cells therefore cannot independently establish which list ran. Matching all ten fields against the source list provides that check.

3. Full-screen Run mode measured 120.042 Hz, rounded to 120 Hz. Across 52 trials in each condition, the median onset differences were 150.13 ms and 1000.00 ms. All short gaps rounded to 18 frames and all long gaps to 120. The millisecond predictions held. The frame counts doubled because the prediction assumed 60 Hz.

4. The median across 103 recorded responses was 267 ms, 383 ms faster than the predicted 650 ms. The timeout rate was 1/104 (0.96%), close to the predicted 1%. The target disappeared on the first valid keypress. The session felt fast and involved frequent guesses. On 34 trials the key arrived within 150 ms of target onset, consistent with that account.

5. Participant 3's list contains no `smoke` and `pepper` pair, so this run cannot verify that exact pair. On main trial 61 the list paired `salt` with `pepper`; the recorded stimulus values were `salt` and `PEPPER`. On all 104 trials, the saved prime matched the lowercase list entry and the saved target matched the uppercase text drawn by the target component.
