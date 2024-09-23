import re
from typing import Tuple
from datetime import datetime

PATTERN_GET_LOG = r'(\d{2}/\w{3}/\d{4} \d{2}:\d{2}:\d{2})\] "(GET \/.*) HTTP\/1\.1" (\d{3}) -' # Run into ()

def parse_log_entry(log_entry: str) -> Tuple[datetime, str, int]:
    date, url, status = re.findall(PATTERN_GET_LOG, log_entry)[0]
    url = url.split(' ')[-1]
    url = url.split('?')[0] if '?' in url else url
    date = datetime.strptime(date, '%d/%b/%Y %H:%M:%S')
    return date, url, int(status)