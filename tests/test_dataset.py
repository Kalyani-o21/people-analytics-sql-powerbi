"""Read-only dataset checks, runnable with python -m unittest discover -s tests -v."""
import csv
import unittest
from datetime import date
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"

def read_csv(filename):
    with (DATA / filename).open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))

class SyntheticDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.depts = read_csv("departments.csv")
        cls.employees = read_csv("employees.csv")
        cls.attendance = read_csv("attendance_monthly.csv")
        cls.training = read_csv("training_records.csv")

    def test_employee_ids_unique_and_count(self):
        ids = [e["employee_id"] for e in self.employees]
        self.assertEqual(len(ids), 600)
        self.assertEqual(len(ids), len(set(ids)))

    def test_department_references(self):
        ids = {d["department_id"] for d in self.depts}
        self.assertTrue(all(e["department_id"] in ids for e in self.employees))

    def test_employee_lifecycle_dates(self):
        for e in self.employees:
            if e["termination_date"]:
                self.assertGreaterEqual(
                    date.fromisoformat(e["termination_date"]),
                    date.fromisoformat(e["hire_date"])
                )

    def test_attendance_ranges_and_employee_refs(self):
        ids = {e["employee_id"] for e in self.employees}
        keys = set()
        for a in self.attendance:
            key = (a["employee_id"], a["month_start"])
            self.assertNotIn(key, keys)
            keys.add(key)
            self.assertIn(a["employee_id"], ids)
            self.assertLessEqual(0, int(a["absence_days"]))
            self.assertLessEqual(int(a["absence_days"]), int(a["scheduled_days"]))

    def test_training_scores_and_employee_refs(self):
        ids = {e["employee_id"] for e in self.employees}
        for t in self.training:
            self.assertIn(t["employee_id"], ids)
            self.assertTrue(0 <= int(t["pre_score"]) <= 100)
            self.assertTrue(0 <= int(t["post_score"]) <= 100)

if __name__ == "__main__":
    unittest.main()
