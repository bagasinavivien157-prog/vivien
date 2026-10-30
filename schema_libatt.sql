-- PROBLEMA:
-- Hindi na-track ng library kung sino ang regular na pumupunta, kung ano libro ang hihiramin,
-- kung anong PC ang ginagamit ng mga estudyante, at hindi rin nila alam kung sino ang
-- pinaka-active na bumibisita sa library para sa rewards.
--
-- SOLUSYON:
-- Library Attendance & Usage System na nagre-record ng pagpasok/paglabas ng estudyante,
-- nagtatanong kung gagamit ba ng PC o may hihiramin bang libro, nag-a-assign ng available na PC,
-- nagtatala kung sino ang gumagamit ng aling PC, nagbibigay ng points kada bisita,
-- at may leaderboard para makita ang pinaka-marami ang punta sa library para sa reward.

CREATE DATABASE IF NOT EXISTS library_attendance_db;
USE library_attendance_db;

CREATE TABLE IF NOT EXISTS students (
  student_id VARCHAR(20) PRIMARY KEY,
  full_name VARCHAR(150) NOT NULL,
  grade_level VARCHAR(20) NOT NULL,
  section VARCHAR(50) NOT NULL,
  total_visits INT DEFAULT 0,
  total_points INT DEFAULT 0,
  date_added DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS books (
  book_id VARCHAR(20) PRIMARY KEY,
  title VARCHAR(150) NOT NULL,
  author VARCHAR(100) NOT NULL,
  available TINYINT(1) DEFAULT 1,
  date_added DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pc_units (
  pc_id INT AUTO_INCREMENT PRIMARY KEY,
  pc_name VARCHAR(10) NOT NULL UNIQUE,
  status ENUM('AVAILABLE','IN-USE') DEFAULT 'AVAILABLE',
  date_added DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS library_visits (
  visit_id INT AUTO_INCREMENT PRIMARY KEY,
  student_id VARCHAR(20) NOT NULL,
  visit_date DATE NOT NULL,
  time_in TIME NOT NULL,
  time_out TIME NULL,
  book_id VARCHAR(20) NULL,
  using_pc TINYINT(1) DEFAULT 0,
  pc_name VARCHAR(10) NULL,
  points_earned INT DEFAULT 0,
  status ENUM('INSIDE','OUT') DEFAULT 'INSIDE',
  FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS pc_usage (
  usage_id INT AUTO_INCREMENT PRIMARY KEY,
  visit_id INT NOT NULL,
  student_id VARCHAR(20) NOT NULL,
  pc_name VARCHAR(10) NOT NULL,
  time_start TIME NOT NULL,
  time_end TIME NULL,
  status ENUM('USING','DONE') DEFAULT 'USING',
  FOREIGN KEY (visit_id) REFERENCES library_visits(visit_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE RESTRICT ON UPDATE CASCADE
);
