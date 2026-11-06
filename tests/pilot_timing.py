"""Desktop diagnostic. Use Studio's Python. Writes only to the requested diagnostic directory.

Uses a small real display window with the compiled Builder experiment. Selects three
trials per block from list 2, injects software key events and a single 60 ms stall,
and saves the CSV and interval log. This is simulated test data, not a human run.
"""
import argparse
import csv
import importlib.util
import shutil
import tempfile
import time
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="new or empty diagnostic directory")
    dest = parser.parse_args().output.resolve()
    dest.mkdir(parents=True, exist_ok=True)
    if any(dest.glob("*.csv")):
        parser.error("Choose an empty destination to preserve earlier evidence.")
    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location("ldt_pilot", root / "ldt.py")
    ex = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ex)
    import_conditions = ex.data.importConditions
    trial = 0
    delivered = set()
    in_trial = False
    injected = False

    def select_trials(*args, **kwargs):
        return import_conditions(*args, **kwargs)[:3]

    def scripted_keys(keyboard, keyList=None, **kwargs):
        elapsed = float(keyboard.clock.getTime())
        if keyList == ["space"] and elapsed >= 0.12:
            name = "space"
        elif keyList == ["f", "j"] and elapsed >= 0.20 and trial % 3 and trial not in delivered:
            name = "f" if trial % 3 == 1 else "j"
            delivered.add(trial)
        else:
            return []
        return [SimpleNamespace(name=name, rt=elapsed, duration=None)]

    with tempfile.TemporaryDirectory() as scratch:
        info = dict(ex.expInfo, participant="2", session="scripted_diagnostic")
        ex.PILOTING, ex._fullScr, ex._winSize = True, False, [640, 480]
        data = ex.setupData(info, dataDir=scratch)
        win = ex.setupWindow(info)
        original_flip = win.flip

        def flip(*args, **kwargs):
            nonlocal trial, in_trial, injected
            if win.recordFrameIntervals and not in_trial:
                trial += 1
            in_trial = bool(win.recordFrameIntervals)
            if in_trial and trial == 2 and not injected and win.recordFrameIntervalsJustTurnedOn is False:
                time.sleep(0.060)
                injected = True
            return original_flip(*args, **kwargs)

        try:
            ex.setupDevices(info, data, win)
            with patch.object(ex.data, "importConditions", select_trials), \
                 patch.object(ex.keyboard.Keyboard, "getKeys", scripted_keys), \
                 patch.object(win, "flip", flip):
                ex.run(info, data, win, globalClock="float")
            assert trial == 6 and injected, (trial, injected)
            ex.saveData(data)
            for suffix in (".csv", "_frameIntervals.log"):
                shutil.copyfile(data.dataFileName + suffix, dest / ("scripted_pilot" + suffix))
        finally:
            data.abort()
            win.close()
    with (dest / "scripted_pilot.csv").open(encoding="utf-8-sig", newline="") as f:
        rows = [r for r in csv.DictReader(f) if r["phase"]]
    assert len(rows) == 6
    hz = round(float(rows[0]["frameRate"]))
    intervals = [float(x) for x in (dest / "scripted_pilot_frameIntervals.log").read_text().split(",")]
    offset = 0
    for r in rows:
        n = int(r["recorded_intervals"])
        segment = intervals[offset:offset+n]
        drops = sum(t > 1.5 / hz for t in segment)
        error = sum(segment) - (float(r["trial_last_flip"]) - float(r["fixation.started"]))
        assert len(segment) == n and abs(error) < 1e-6
        assert drops == int(r["dropped_frames"])
        print(r["phase"], r["trial_index"], "intervals", n, "drops", drops,
              "span error (s)", round(error, 9))
        offset += n
    assert offset == len(intervals) and int(rows[1]["dropped_frames"]) >= 1
    print("PASS six real trial windows, including the deliberately delayed second trial")


if __name__ == "__main__":
    main()
