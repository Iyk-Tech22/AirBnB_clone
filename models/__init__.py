#!/usr/bin/python3
"""
import file_storage, initializes the FileStorage 
as well as call reload() method  
"""
from models.engine.file_storage import FileStorage
storage = FileStorage()
storage.reload()