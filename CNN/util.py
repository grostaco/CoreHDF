from parse import parse
from datetime import datetime
import json


class CDFLog:
    def __init__(self, logfile: str = 'log.txt'):
        self.file_handler = open(logfile, 'r')
        self.preprocess_cache = []

    def get_last_logs(self, n: int, force_reload=False):
        temp = []
        if not len(self.preprocess_cache) or force_reload:
            while line := self.file_handler.readline():
                self.preprocess_cache.append(line)

        for line in self.preprocess_cache[-n:]:
            temp.append(CDFContext(line))

        return temp


class CDFContext:
    def __init__(self, report: str):
        parse_result = parse('[{level}/{time}] {message}', report)
        self.level = parse_result['level']
        self.datetime = datetime.strptime(parse_result['time'].split(',')[0], '%Y-%m-%d %H:%M:%S')
        self.datetime_raw = parse_result['time']
        self.message = parse_result['message']

    def json(self):
        return json.dumps({'level': self.level,
                           'datetime': self.datetime_raw,
                           'message': self.message})