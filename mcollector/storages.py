# -*- coding: utf-8 -*-
from tinydb import TinyDB, Query


class BaseStorage(object):

    def store(self, data_dict):
        raise NotImplementedError()

    def all(self):
        raise NotImplementedError()

    def all_sorted(self):
        raise NotImplementedError()

    def for_timestamp_range(self, start_timestamp=None, end_timestamp=None):
        raise NotImplementedError()


class TinyDBStorage(object):

    def __init__(self, db_path):
        self.tinydb = TinyDB(db_path)
        self.table = self.tinydb.table('metrics')

    def store(self, data_dict):
        self.table.insert(data_dict)
        return True

    def all(self):
        return self.table.all()

    def all_sorted(self):
        return sorted(self.all(), key=lambda x: x['timestamp'])

    def clear(self):
        return self.tinydb.purge()

    def for_timestamp_range(self, start_timestamp=None, end_timestamp=None):
        Metrics = Query()
        timestamp_query = (Metrics.timestamp >= 0)
        if start_timestamp:
            timestamp_query = timestamp_query & (Metrics.timestamp >= start_timestamp)
        if end_timestamp:
            timestamp_query = timestamp_query & (Metrics.timestamp <= end_timestamp)
        return self.table.search(timestamp_query)
