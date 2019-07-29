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
    foo.log.info("ok")


class TestLogging:
    def test_basic(self):
        foo = Foo()
        foo.log.set_verbose(True)
        foo.log.info("This is some information")
        foo.log.info("This is more information")

    @pytest.mark.parametrize(
        "level",
        [
            "error",
            "critical",
            "debug",
            "info",
            "warn",
            "ERROR",
            "CRITICAL",
            "DEBUG",
            "INFO",
            "WARN",
        ],
    )
    @pytest.mark.parametrize(
        "level_as_str", [True, False], ids=["LVL_AS_STR", "LVL_AS_INT"]
    )
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
        assert level_str.upper() in log

    @pytest.mark.parametrize("level", ["error", "critical", "debug", "info", "warn"])
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

    @pytest.mark.parametrize("level", ["error", "critical", "debug", "info", "warn"])
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

    @pytest.mark.parametrize("level", ["error", "critical", "debug", "info", "warn"])
    def test_leveled_progress_bar(self, level):
        log = Loggable("Test")
        for x in log.tqdm(range(10), level, desc="this is a description"):
            log.info(x)
        log.info("This is more information")


class TestTimedLoggable(object):
    def test_basic_log(self, capsys):
        logger = Loggable("loggable_test")
        logger.set_level("INFO")

        logger.timeit("INFO").info("log2")
        log, _ = capsys.readouterr()
        assert "INFO" in log

    def test_spawn(self, capsys):
        log = Loggable("loggable_test")
        log.set_level("INFO")
        log2 = log.timeit(logging.INFO)
        log2.enter()
        log2.info("log2")
        log2.exit()
        msg, _ = capsys.readouterr()
        assert "started" in msg.lower()
        assert "log2" in msg
        assert "finished" in msg.lower()

    def test_timeit(self):
        log = Loggable("loggable_test")
        log.set_level("INFO")

        with log.timeit(logging.INFO, "TimeItTest"):
            log.info("ok")

    def test_timeit(self, capsys):
        log = Loggable("loggable_test")
        log.set_level("INFO")

        timeit = log.timeit(logging.INFO)
        timeit.enter()
        timeit.info("ok")
        time.sleep(0.1)
        timeit.exit()
        log, _ = capsys.readouterr()
        print(log)
        assert "started" in log.lower()
        assert "ok" in log
        assert "finished" in log.lower()

    def test_does_not_log(self, capsys):
        log = Loggable("loggable_test")
        log.set_level("ERROR")

        timeit = log.timeit(logging.INFO)
        timeit.enter()
        timeit.info("ok")
        time.sleep(0.1)
        timeit.exit()
        log, _ = capsys.readouterr()
        print(log)
        assert not log

    def test_prefix(self, capsys):
        log = Loggable("loggable_test")
        log.set_level("INFO")

        timeit = log.timeit(logging.INFO, "prefix")
        timeit.enter()
        timeit.info("Some information")
        timeit.exit()
        log, _ = capsys.readouterr()
        print(log)
        assert "prefix" in log


class TestProgressLoggable(object):
    def test_basic_log(self, capsys):
        logger = Loggable("loggable_test")
        logger.set_level("INFO")

        logger.track("INFO").info("log2")
        log, _ = capsys.readouterr()
        assert "INFO" in log

    def test_update(self, capsys):
        logger = Loggable("loggable_test")
        logger.set_level("INFO")

        track = logger.track("INFO", total=100).enter()
        track.update(10, "10% there!")
        track.update(20, "20% there!")
        track.exit()

    def test_not_enabled(self):
        logger = Loggable("loggable_test")
        logger.set_level("CRITICAL")

        track = logger.track("INFO")
        assert not track.is_enabled()

        track = logger.track("CRITICAL")
        assert track.is_enabled()

    def test_track_iterable(self):
        logger = Loggable("loggable_test")
        logger.set_level("INFO")
        track = logger.track("INFO", desc="This is a progress bar")
        for x in track(range(10)):
            track.info(x)

    def test_no_update(self, capsys):
        logger = Loggable("loggable_test")
        logger.set_level("CRITICAL")
        assert not logger.is_enabled("INFO")

        track = logger.track("INFO", total=100).enter()
        track.update(10, "10% there!")
        track.update(20, "20% there!")
        track.exit()


def test_tb_limit(capsys):
    foo = Foo()
    foo.log.set_verbose(True, tb_limit=10)
    foo.bar()
