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

The table expands my prediction that A fails scoring, D fails prime text and
F fails response timing. I expect the rest to pass wherever the CSV can
settle the question. P = PASS, F = FAIL, U = UNDETERMINED. The letters in a
split cell refer to the named parts of that row in order.

| Property and parts | A | B | C | D | E | F |
| --- | --- | --- | --- | --- | --- | --- |
| Q3 recorded sequence and durations / instruction wording | P/U | P/U | P/U | P/U | P/U | P/U |
| Q4 recorded prime text / target response window / other checkable trial events | P/P/P | P/P/P | P/P/P | F/P/P | P/P/P | P/F/P |
| Q5 recorded fixed frame counts | P | P | P | P | P | P |
| Q6 recorded response keys | P | P | P | P | P | P |
| Q7 response timing relative to target onset | P | P | P | P | P | F |
| Q8 recorded prime / recorded target | P/P | P/P | P/P | F/P | P/P | P/P |
| Q9 saved software flip times / actual screen onset | P/U | P/U | P/U | P/U | P/U | P/U |
| Q10 accuracy / timeout deadline / other checkable fields | F/P/P | P/P/P | P/P/P | P/P/P | P/P/P | P/F/P |

Codex mapped the three faults I named to the overlapping requirements above.
For C and E my prediction concerns the new checks, even though their list or
order already failed in A5. The P entries apply to evidence in the file.

Before making these A6 file predictions, I asked Codex to summarize the A5
findings for files A through F from `verification_report.md`. Codex used that
written report without reopening the six CSVs.

1. Which properties, or parts of properties, do you expect to be
   UNDETERMINED for every file, and why can't a data file settle them?

   I would need the build to see what the instructions actually said. The
   file can record an instructions event without recording the words. A
   light sensor would be needed for the physical onset in Q9.

2. Of the files that passed Q1 and Q2 in A5, how many do you expect to fail
   something in Q3–Q10?

   Three of four: A, D and F. I expect B to pass its checkable parts.

## Your own build

Answer for your A5 build at the tag, run on the computer you will use for
runs 7 and 8.

3. What will `frameRate` say on that computer? What frame counts does Q5
   then require for the fixation, the prime, the SOA 150 and SOA 1000
   intervals, the ITI, the feedback, and the end screen?

   I expect about 120 Hz in fullscreen on the built-in MacBook Pro display.

   Using 120 Hz, the Q5 calculation is `round(duration_ms * 120 / 1000)`:

   | Event or interval | Duration (ms) | Frames |
   | --- | ---: | ---: |
   | Fixation | 500 | 60 |
   | Prime | 150 | 18 |
   | Prime-to-target SOA 150 | 150 | 18 |
   | Prime-to-target SOA 1000 | 1000 | 120 |
   | Inter-trial interval | 500 | 60 |
   | Practice feedback | 1000 | 120 |
   | End screen | 2000 | 240 |

   Prediction provenance: Ibra selected "About 120 Hz" in this chat on
   November 5, 2026. Before this answer, Codex had read the A5 documentation
   reporting approximately 120 Hz and checked macOS display information,
   which reported 120.00 Hz. Codex calculated the table from that prediction
   and the specification. No new experiment run or output-file check had
   been performed for A6 at this point.

4. Which of Q3–Q10 do you expect your A5 build to fail, if any? Name the
   part of the build you are least sure of.

   I expect it to pass everything, but I'm least sure about the timing.

5. In the instrumented run with nothing else open (participant 7), how many
   dropped frames will `dropped_frames` add up to? With a video playing
   (participant 8)? Where in a trial will they happen?

   I'd guess 0 dropped frames in run 7 and 2 in run 8, probably when the target appears.

6. When a frame is dropped during the prime, what happens to the prime's
   duration in your build: longer, shorter, or unchanged? What happens to
   the SOA on that trial?

   I'd guess the prime stays on longer and the target appears later, so I expect a longer SOA.

7. Name three timing properties in Q4–Q10 that software time stamps can
   verify, one they can only bound, and one they cannot reach at all.

   I think the timestamps can verify fixation duration, prime duration and SOA.
   Frame rounding gives a range. Actual screen onset needs a light sensor.
