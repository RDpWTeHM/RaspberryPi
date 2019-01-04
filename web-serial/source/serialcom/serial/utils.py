"""utils.py

Author: Joseph Lin
E-mail: joseph.lin@aliyun.com

"""
import os
import sys
from contextlib import contextmanager
from collections import defaultdict
from abc import abstractmethod, ABC


class WebSerialError(Exception):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)


class SerialDoseNotConnectionError(WebSerialError):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)


class SerialUnpluggingError(WebSerialError):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)


class SerialConnectionRefuseError(WebSerialError):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)


class Exchange:
    def __init__(self):
        self._subscribers = set()

    def attach(self, task):
        self._subscribers.add(task)

    def detach(self, task):
        self._subscribers.remove(task)

    @contextmanager
    def subscribe(self, *tasks):
        for task in tasks:
            self.attach(task)
        try:
            yield
        finally:
            for task in tasks:
                self.detach(task)

    def send(self, msg):
        for subscribe in self._subscribers:
            subscribe.send(msg)


# -[o] take care about _exchanges and get_exchange as globle variables
_exchanges = defaultdict(Exchange)


def get_exchange(name):
    return _exchanges[name]