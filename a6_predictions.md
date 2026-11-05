# Predictions (Part A)

Fill in this file before you run any new check, on your own files or on the
provided ones, and commit it with a message that starts `predictions-a6:`.
Do not edit it after that commit; the history is how it is read. The
reconciliation goes in `a6_report.md`, not here.

You are graded on the reconciliation, not on being right. A prediction you
cannot be wrong about earns nothing, so commit to answers.

## The six provided files

In A5 you checked Q1 and Q2 on these files. Without opening them again,
predict the verdict (PASS, FAIL, or UNDETERMINED) each file will get on each
of Q3–Q10 from a checker that has only the file. Where a property has parts
that could get different verdicts, split the cell and say which part.

| Property | A | B | C | D | E | F |
| --- | --- | --- | --- | --- | --- | --- |
| Q3 | | | | | | |
| Q4 | | | | | | |
| Q5 | | | | | | |
| Q6 | | | | | | |
| Q7 | | | | | | |
| Q8 | | | | | | |
| Q9 | | | | | | |
| Q10 | | | | | | |

1. Which properties, or parts of properties, do you expect to be
   UNDETERMINED for every file, and why can't a data file settle them?

2. Of the files that passed Q1 and Q2 in A5, how many do you expect to fail
   something in Q3–Q10?

## Your own build

Answer for your A5 build at the tag, run on the computer you will use for
runs 7 and 8.

3. What will `frameRate` say on that computer? What frame counts does Q5
   then require for the fixation, the prime, the SOA 150 and SOA 1000
   intervals, the ITI, the feedback, and the end screen?

4. Which of Q3–Q10 do you expect your A5 build to fail, if any? Name the
   part of the build you are least sure of.

5. In the instrumented run with nothing else open (participant 7), how many
   dropped frames will `dropped_frames` add up to? With a video playing
   (participant 8)? Where in a trial will they happen?

6. When a frame is dropped during the prime, what happens to the prime's
   duration in your build: longer, shorter, or unchanged? What happens to
   the SOA on that trial?

7. Name three timing properties in Q4–Q10 that software time stamps can
   verify, one they can only bound, and one they cannot reach at all.
