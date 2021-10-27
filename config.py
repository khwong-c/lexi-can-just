from datetime import datetime, timedelta, timezone
# Config
URL_JUST = "https://humanum.arts.cuhk.edu.hk/Lexis/lexi-can/just.php"
SIZE_LOG = 1024 * 1024 * 10
TZ_HK = timezone(timedelta(hours=8))
POLL_INTERVAL = 10 # In Seconds
MERGE_INTERVAL = 10 # In minutes
MERGE_INTERVAL_SEC = MERGE_INTERVAL * 60

# Files
FILE_LOG_CRAWL = "log/crawl.log"
DIR_DB  = "lexican.db"
DIR_DB_MERGED  = "lexican.merged.db"