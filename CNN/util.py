from enum import Enum
from parse import parse
from datetime import datetime
import json


class CDFLogType(Enum):
    NEW_COREHDF_INSTANCE = 1
    PERSON_DETECTED = 2
    NOTHING_DETECTED = 3
    CANNOT_BE_INFERRED = 4


class CDFLog:
    def __init__(self, logfile: str = 'log.txt'):
        self.file_handler = open(logfile, 'r')
        self.preprocess_cache = []

    def get_last_logs(self, n: int, force_reload=False, reverse=False):
        temp = []
        if not len(self.preprocess_cache) or force_reload:
            while line := self.file_handler.readline():
                self.preprocess_cache.append(line)

        for line in self.preprocess_cache[-n:]:
            temp.append(CDFContext(line))

        return temp if not reverse else list(reversed(temp))

    def get_detected(self, limit: int = -1, force_reload=False):
        temp = []
        logs = self.get_last_logs(0, force_reload=force_reload, reverse=True)

        for log in logs:
            if log.infer_type() == CDFLogType.PERSON_DETECTED:
                print('A')
                # intentional bypass for limit = -1
                if limit == 0 :
                    break
                else :
                    limit -= 1

                temp.append(log)

        return temp

    def clear_logs(self, limit: int = -1):
        temp = []

class CDFContext:
    def __init__(self, report: str):
        parse_result = parse('[{level}/{time}] {message}', report)
        self.level = parse_result['level']
        self.datetime = datetime.strptime(parse_result['time'].split(',')[0], '%Y-%m-%d %H:%M:%S')
        self.datetime_raw = parse_result['time']
        self.message = parse_result['message']

    def infer_type(self):
        if self.message.startswith('Created'):
            return CDFLogType.NEW_COREHDF_INSTANCE
        if self.message.startswith('Detected'):
            return CDFLogType.PERSON_DETECTED
        if self.message.startswith('No person'):
            return CDFLogType.NOTHING_DETECTED
        return CDFLogType.CANNOT_BE_INFERRED

    def json(self):
        return json.dumps({'level': self.level,
                           'datetime': self.datetime_raw,
                           'message': self.message})