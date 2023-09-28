#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""

import os
from models.engine import db_storage, file_storage

storage_type = os.getenv('HBNB_TYPE_STORAGE')

if storage_type == 'db':
    storage = db_storage.DBStorage()
else:
    storage = file_storage.FileStorage()

storage.reload()
