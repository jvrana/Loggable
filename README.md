# Loggable

[![PyPI version](https://badge.fury.io/py/loggable-jdv.svg)](https://badge.fury.io/py/loggable-jdv)

Logging library with terminal colors, loggable progress bars, and timed logs built in.

## Installation

## Usage

Basic logger:

```
>>> from loggable import Loggable
>>> logger = Loggable("MyLogger")
>>> logger.set_level("INFO")
>>> logger.info("Informative message")
INFO - MyLogger - 2019-07-29 13:07:59,715 - Informative message
<loggable.Loggable object at 0x1108a1cc0>
```

Logging other types of messages:

```
>>> logger.info("Informative message")
INFO - MyLogger - 2019-07-29 13:07:59,715 - Informative message

>>> logger.warn("Warning message")
WARNING - MyLogger - 2019-07-29 13:10:10,253 - Warning message

>>> logger.debug("Debug message")
DEBUG - MyLogger - 2019-07-29 13:07:59,715 - Debug message

>>> logger.error("Error message")
ERROR - MyLogger - 2019-07-29 13:10:10,253 - Error message

>>> logger.critical("Critical message")
CRITICAL - MyLogger - 2019-07-29 13:10:10,253 - Critical message
```

Logging a custom level:

```
>>> logger.log("my custom message", 15)
```

A log message can be displayed that displays how long a series of command took.

```
>>> with logger.timeit("INFO") as timeit:
>>>     timeit.log("this is an informative message at default INFO level")
>>>     timeit.error("this is a error message that will get displayed")
>>>     timeit.debug("this is a debug message that will not get displayed")
```

A timed message can be displayed manually using `enter` and `exit` methods.

```
>>> timeit = logger.timeit("INFO")
>>> timeit.enter()
>>> timeit.log("long process")
>>> timeit.exit()
INFO - MyLogger - 2019-07-29 13:19:12,301 - Finished in 0:00:00.000528.
<loggable.TimedLoggable object at 0x10f1bc208>
```

A loggable progress bar can be displayed. Progress bar will only be displayed if logging is enabled.

```
>>> for x in logger.tqdm(range(10), "INFO"):
>>>     logger.info(x)
```

Manually updating a progress bar:

```
>>> pbar = logger.track("INFO", desc="my progress bar", total=100).enter()
>>> pbar.update(10, "10% done!")
>>> pbar.update(35, "35% done!")
>>> pbar.exit()
INFO - MyLogger - 2019-07-29 13:19:12,320 - 10% done!
INFO - MyLogger - 2019-07-29 13:19:12,320 - 35% done!
 35%|████████████████▌| 35/100 [00:00<00:00, 13971.70it/s]
```

Making attaching a logger to a model class. Instantiating with model instance will create
a unique logger for that instance.

```python
class Foo(object):

    def __init__(self):
        self.log = Loggable(self)

    def bar(self):
        self.log.info("bar was called")

foo = Foo()
foo.log.set_level("INFO", tb_limit=10)
foo.bar()
```
