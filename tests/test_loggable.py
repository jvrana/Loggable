from loggable import Loggable
from uuid import uuid4
from tqdm import tqdm
import time
import pytest
import logging


class Foo(object):

    def __init__(self):
        self.log = Loggable(self)

    def bar(self):
        self.log.info("bar")


def test_init_with_class():
    foo = Foo()
    foo.log.set_level("INFO")
    foo.log.info('ok')


class TestLogging:

    def test_basic(self):
        foo = Foo()
        foo.log.set_verbose(True)
        foo.log.info("This is some information")
        foo.log.info("This is more information")

    @pytest.mark.parametrize('level', ['error', 'critical', 'debug', 'info', 'warn', 'ERROR', 'CRITICAL', 'DEBUG', 'INFO', 'WARN'])
    @pytest.mark.parametrize('level_as_str', [True, False], ids=['LVL_AS_STR', 'LVL_AS_INT'])
    def test_does_log(self, level, level_as_str, capsys):
        logger = Loggable("test")

        fxn = getattr(logger, level.lower())

        level_str = level

        if not level_as_str:
            level = getattr(logging, level.upper())

        # check log
        logger.set_level(level)
        msg = str(uuid4())
        fxn(msg)
        log, _ = capsys.readouterr()

        print(log)
        assert msg in log
        assert level_str.upper() in log    \

    @pytest.mark.parametrize('level', ['error', 'critical', 'debug', 'info', 'warn'])
    def test_does_not_log(self, level, capsys):
        logger = Loggable("test")
        fxn = getattr(logger, level.lower())

        # does log
        logger.set_level(level)
        msg = str(uuid4())
        fxn(msg)
        log, _ = capsys.readouterr()
        # print(log)
        assert msg in log
        assert level.upper() in log

        # does not log
        logger.set_level(logging.CRITICAL + 1)
        msg = str(uuid4())
        fxn(msg)
        log, _ = capsys.readouterr()
        assert not log
        assert not _

    @pytest.mark.parametrize('level', ['error', 'critical', 'debug', 'info', 'warn'])
    def test_log(self, level, capsys):
        logger = Loggable("test")
        msg = str(uuid4())
        logger.set_level(level)
        logger.log(msg, level)
        log, _ = capsys.readouterr()
        print(log)
        assert msg in log

class TestProgressBar(object):

    def test_basic_progress_bar(self):
        log = Loggable("test")
        for x in tqdm(range(10)):
            log.info(x)
            time.sleep(0.01)
        log.info("This is more information")


    @pytest.mark.parametrize('level', ['error', 'critical', 'debug', 'info', 'warn'])
    def test_leveled_progress_bar(self, level):
        log = Loggable("Test")
        for x in log.tqdm(range(10), level, desc='this is a description'):
            log.info(x)
        log.info("This is more information")


def test_tb_limit(capsys):
    msg = str(uuid4())
    foo = Foo()
    foo.log.set_verbose(True, tb_limit=10)
    foo.bar()
