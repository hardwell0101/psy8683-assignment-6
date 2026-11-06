"""Mutate a preserved reference file or diagnostic, then run the ordinary CLI."""
import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MutationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.directory = Path(self.tmp.name)

    def fixture(self, source="provided/output_files/file_B.csv"):
        with (ROOT/source).open(encoding="utf-8-sig", newline="") as f:
            self.header, *self.rows = csv.reader(f)

    def change(self, field, val, index=1):
        self.rows[index][self.header.index(field)] = str(val)

    def check(self, *flags):
        path = self.directory/"run.csv"
        with path.open("w",newline="") as f:
            writer = csv.writer(f)
            writer.writerow(self.header)
            writer.writerows(self.rows)
        p = subprocess.run([sys.executable,"check_output.py",str(path),"--lists",
                            "provided/canonical_trial_lists",*flags], cwd=ROOT,
                           capture_output=True,text=True, check=False)
        self.assertIn(p.returncode,(0,1),p.stderr)
        self.assertEqual(p.stderr,"")
        return p.stdout

    def test_correct_control_and_reference_aliases(self):
        self.fixture()
        text = self.check()
        self.assertNotIn(" FAIL ",text)
        self.assertNotIn(" PILOT ",text)
        self.assertIn("Q3 PASS screen order",text)
        self.assertIn("Q5 PASS ITI frame count",text)

    def test_wrong_phase_order(self):
        self.fixture()
        self.change("phase","experimental")
        self.assertIn("Q3 FAIL phase counts and order",self.check())

    def test_duplicate_participant_conflict(self):
        self.fixture()
        self.change("participant",7)
        self.assertIn("Q1 FAIL",self.check("--participant","4"))

    def test_duration_off_one_frame_without_drops(self):
        self.fixture()
        i = self.header.index("prime_text.stopped")
        self.change("prime_text.stopped",float(self.rows[1][i])+1/60)
        self.assertIn("Q5 FAIL prime frame count",self.check())

    def test_unknown_component_is_open(self):
        self.fixture()
        self.header[self.header.index("key_resp.started")] = "unknown_device.started"
        self.assertIn("Q7 UNDETERMINED keyboard starts",self.check())

    def test_wrong_onset_and_unknown_key(self):
        self.fixture()
        self.change("prime_onset",0)
        self.change("key","k")
        text=self.check()
        self.assertIn("Q9 FAIL prime onset",text)
        self.assertIn("Q6 FAIL accepted recorded key",text)
        self.assertIn("Q10 FAIL response fields",text)

    def test_missing_required_column_and_bad_numeric(self):
        self.fixture()
        self.header[self.header.index("target_shown")] = "absent"
        self.change("prime_onset","nan")
        text=self.check()
        self.assertIn("Q8 FAIL required output columns",text)
        self.assertIn("Q9 FAIL prime onset",text)

    def test_timeout_keyboard_disappears_before_target_deadline(self):
        self.fixture("provided/output_files/file_F.csv")
        self.assertIn("Q10 FAIL keyboard available through target deadline",self.check())

    def test_instruction_key_and_different_feedback_duration(self):
        self.fixture()
        self.change("instr_key.keys","j",0)
        self.change("feedback_text.stopped",.2)
        text=self.check()
        self.assertIn("Q3 FAIL instructions SPACE response",text)
        self.assertIn("Q5 FAIL practice feedback frame count",text)

    def pilot(self):
        self.fixture("evidence/diagnostic/scripted_pilot.csv")
        return ROOT/"evidence/diagnostic/scripted_pilot_frameIntervals.log"

    def test_long_interval_and_redistributed_drops(self):
        log=self.pilot()
        (self.directory/"run_frameIntervals.log").write_bytes(log.read_bytes())
        text=self.check("--require-log")
        for s in ("I1 PASS trial slice endpoints","I2 PASS trial slice count",
                  "Q5 PASS fixation frame count"):
            self.assertIn(s,text)
        # Keep the global total right while moving a drop to the wrong trial.
        i=self.header.index("dropped_frames")
        before=count1=int(self.rows[2][i])
        self.assertGreaterEqual(before,1)
        self.change("dropped_frames",count1-1,2)
        self.change("dropped_frames",int(self.rows[1][i])+1,1)
        text=self.check("--require-log")
        self.assertIn("I2 PASS whole-run agreement",text)
        self.assertIn("I2 FAIL trial slice count",text)

    def test_extra_interval_and_missing_log(self):
        log=self.pilot()
        self.assertIn("I1 FAIL interval log",self.check("--require-log"))
        (self.directory/"run_frameIntervals.log").write_text(log.read_text()+",0.25")
        text=self.check("--require-log")
        self.assertIn("I1 FAIL all intervals allocated",text)
        self.assertIn("I2 FAIL whole-run agreement",text)

    def test_malformed_counter(self):
        log=self.pilot()
        (self.directory/"run_frameIntervals.log").write_bytes(log.read_bytes())
        self.change("dropped_frames","-1")
        self.assertIn("I2 FAIL per-trial counts",self.check("--require-log"))


if __name__=="__main__":
    unittest.main(verbosity=2)
