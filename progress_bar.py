from loggable import Loggable
from uuid import uuid4
from tqdm import tqdm
import time

class Foo(object):

    def __init__(self):
        self.log = Loggable(self)

    def bar(self):
        self.log.info("bar")


if __name__ == '__main__':
    foo = Foo()
    foo.log.set_verbose(True)
    foo.log.info("This is some information")
    for x in tqdm(range(100)):
        foo.log.info(x)
        time.sleep(0.01)
    foo.log.info("This is more information")