-- Run in an empty PostgreSQL database named people_analytics.
-- Import CSV files AFTER creating these tables.
CREATE TABLE departments (
  department_id INTEGER PRIMARY KEY,
  department_name VARCHAR(80) NOT NULL
);

CREATE TABLE employees (
  employee_id VARCHAR(12) PRIMARY KEY,
  department_id INTEGER NOT NULL REFERENCES departments(department_id),
  hire_date DATE NOT NULL,
  termination_date DATE,
  employment_type VARCHAR(20) NOT NULL CHECK (employment_type IN ('Full-time','Part-time')),
  shift VARCHAR(20) NOT NULL CHECK (shift IN ('Day','Night','Rotating')),
  CONSTRAINT valid_employee_dates CHECK (termination_date IS NULL OR termination_date >= hire_date)
);

CREATE TABLE attendance_monthly (
  employee_id VARCHAR(12) NOT NULL REFERENCES employees(employee_id),
  month_start DATE NOT NULL,
  scheduled_days INTEGER NOT NULL CHECK (scheduled_days > 0),
  absence_days INTEGER NOT NULL CHECK (absence_days >= 0),
  PRIMARY KEY (employee_id, month_start),
  CONSTRAINT valid_absences CHECK (absence_days <= scheduled_days)
);

CREATE TABLE training_records (
  training_id VARCHAR(12) PRIMARY KEY,
  employee_id VARCHAR(12) NOT NULL REFERENCES employees(employee_id),
  training_date DATE NOT NULL,
  training_type VARCHAR(40) NOT NULL,
  pre_score INTEGER NOT NULL CHECK (pre_score BETWEEN 0 AND 100),
  post_score INTEGER NOT NULL CHECK (post_score BETWEEN 0 AND 100)
);
