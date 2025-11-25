-- Create table for storing logs and alerts
CREATE TABLE IF NOT EXISTS Logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    level TEXT NOT NULL,         -- INFO, WARNING, ERROR
    message TEXT NOT NULL,
    details TEXT,                -- optional detailed info (stack trace, etc.)
    execution_time REAL          -- seconds, measured via @timeit
);
SELECT * FROM Logs;

