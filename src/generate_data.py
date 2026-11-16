"""Generate deterministic, entirely synthetic HR CSVs for portfolio learning.

Run: python src/generate_data.py
Requires only the Python standard library.
"""
from pathlib import Path
from datetime import date, timedelta
import csv

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"
DATA.mkdir(exist_ok=True)
_state = 287285

def next_random():
    global _state
    _state = (1664525 * _state + 1013904223) & 0xFFFFFFFF
    return _state

def randint(lo, hi):
    return lo + next_random() % (hi - lo + 1)

def random_date(lo, hi):
    return lo + timedelta(days=randint(0, (hi - lo).days))

def write_csv(name, header, rows):
    with (DATA / name).open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
        writer.writerows(rows)

departments = [
    (1, "Manufacturing"), (2, "Logistics"), (3, "Quality"),
    (4, "Engineering"), (5, "Human Resources"), (6, "Maintenance"),
    (7, "Supply Chain"),
]
shifts = ("Day", "Night", "Rotating")
courses = ("Safety", "Systems", "Operations", "Data Literacy")
weights = (30, 14, 12, 15, 7, 12, 10)
period_start, period_end = date(2024, 1, 1), date(2026, 10, 31)

def choose_department():
    ticket = randint(1, 100)
    total = 0
    for (dept, _), weight in zip(departments, weights):
        total += weight
        if ticket <= total:
            return dept
    raise ValueError("Department weights do not sum to 100")

employees = []
for index in range(1, 601):
    hired = random_date(date(2021, 1, 1), date(2026, 9, 30))
    dept = choose_department()
    employment_type = "Part-time" if randint(0, 4) == 4 else "Full-time"
    shift = shifts[randint(0, 2)]
    termination = None
    if randint(0, 9999) < 2600 and hired <= date(2026, 5, 31):
        earliest = max(hired + timedelta(days=90), period_start)
        if earliest <= period_end:
            termination = random_date(earliest, period_end)
    employees.append((f"EMP{index:04}", dept, hired, termination,
                      employment_type, shift))

write_csv("departments.csv", ("department_id", "department_name"), departments)
write_csv("employees.csv",
          ("employee_id", "department_id", "hire_date", "termination_date",
           "employment_type", "shift"),
          ((eid, dep, hired.isoformat(), term.isoformat() if term else "",
            et, shift) for eid, dep, hired, term, et, shift in employees))

months = []
for y in range(2024, 2027):
    for m in range(1, 13):
        if y == 2026 and m > 10:
            break
        ms = date(y, m, 1)
        me = date(y + (m == 12), (m % 12) + 1, 1) - timedelta(days=1)
        months.append((ms, me))

attendance = []
for eid, dep, hired, term, et, shift in employees:
    for ms, me in months:
        if hired <= me and (term is None or term >= ms):
            ticket = randint(1, 100)
            boundaries = (50, 70, 82, 90, 95, 98, 100)
            absent = next(i for i, bound in enumerate(boundaries) if ticket <= bound)
            scheduled = 20 if et == "Full-time" else 12
            attendance.append((eid, ms.isoformat(), scheduled, absent))

write_csv("attendance_monthly.csv",
          ("employee_id", "month_start", "scheduled_days", "absence_days"),
          attendance)

training = []
for eid, dep, hired, term, et, shift in employees:
    if randint(0, 9999) < 5000:
        earliest = max(hired, period_start)
        latest = min(term or period_end, period_end)
        if earliest <= latest:
            trained = random_date(earliest, latest)
            pre = randint(40, 80)
            post = max(0, min(100, pre + randint(-5, 28)))
            course = courses[randint(0, 3)]
            training.append((f"TRN{len(training)+1:05}", eid,
                             trained.isoformat(), course, pre, post))

write_csv("training_records.csv",
          ("training_id", "employee_id", "training_date",
           "training_type", "pre_score", "post_score"), training)

print(f"Generated: {len(employees)} employees, {len(attendance)} attendance rows, "
      f"{len(training)} training rows; files saved to {DATA}")
