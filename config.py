import os
from datetime import timedelta, timezone
# Logs
LOG_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
# Config
URL_JUST = "https://humanum.arts.cuhk.edu.hk/Lexis/lexi-can/just.php"
SIZE_LOG = 1024 * 1024 * 10
TZ_HK = timezone(timedelta(hours=8))
TZ_GMT = timezone(timedelta(hours=0))
POLL_INTERVAL = 10 # In Seconds
MERGE_INTERVAL = 30 # In minutes
MERGE_INTERVAL_SEC = MERGE_INTERVAL * 60
TS_CACHE_TTL = 60
POSSIBLE_MOST_COUNT = [0,10,50,100,500,1000]
DEFAULT_MOST_COUNT = 50

# Files
FILE_LOG_CRAWL = "log/crawl.log"
DIR_DB  = "lexican.db"
SQLITE_DB_MERGED  = "lexican.merged.sqlite.db"
SQLITE_DB_LOG  = "lexican.log.sqlite.db"

DEBUG = os.environ.get('DEBUG', '')