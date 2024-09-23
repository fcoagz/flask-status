import os
import re
from sqlalchemy import create_engine
from ..utils.cache import cache

if re.findall('tmp', cache['SQLALCHEMY_DATABASE_URI']):
    os.makedirs('tmp', exist_ok=True)

engine = create_engine(cache['SQLALCHEMY_DATABASE_URI'])