from loggable import Loggable
from uuid import uuid4

class Foo(Loggable):

    def __init__(self):
        pass


def test_basic(capsys):
    foo = Foo()
    foo.set_verbose(True)
    foo._info("This is some information")


def test_log_info(capsys):
    msg = str(uuid4())
    foo = Foo()
    foo.set_verbose(True)
    foo._info(msg)
    _, log = capsys.readouterr()
    assert "INFO" in log
    assert "Foo" in log
    assert msg in log

    foo.set_verbose(False)
    foo._info(msg)
    _, log = capsys.readouterr()
    assert not log