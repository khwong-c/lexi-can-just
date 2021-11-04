SQL_CREATE_TABLE = """CREATE TABLE IF NOT EXISTS lexican_history(
    timestamp INTEGER UNIQUE
                      NOT NULL
                      PRIMARY KEY DESC,
    interval  INTEGER NOT NULL,
    chars     TEXT
);
"""
SQL_INSERT_RECORD = """
INSERT INTO lexican_history(timestamp, interval, chars) VALUES(?,?,?);
"""
SQL_SELECT_ALL_RECORD = """
    SELECT timestamp, interval, chars FROM lexican_history;
"""
SQL_SELECT_RANGED_RECORD = """
    SELECT timestamp, interval, chars 
    FROM lexican_history
    WHERE timestamp >= ? AND timestamp < ?;
"""
SQL_GET_LATEST_TIMESTAMP = """
    SELECT timestamp FROM lexican_history ORDER BY timestamp DESC LIMIT 1;
"""

RECORD_TITLE = [('ts','interval','chars')]