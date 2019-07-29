# Loggable

## Installation

## Usage

Basic logger:

```python
>>> from loggable import Loggable
>>> logger = Loggable("MyLogger")
>>> logger.set_level("INFO")
>>> logger.info("Informative message")
INFO - MyLogger - 2019-07-29 13:07:59,715 - Informative message
<loggable.Loggable object at 0x1108a1cc0>
```

Logging other types of messages:

```python
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

Logging a timed message:

```python
>>> with logger.timeit("INFO") as timeit:
>>>     timeit.log("this is an informative message at default INFO level")
>>>     timeit.error("this is a error message that will get displayed")
>>>     timeit.debug("this is a debug message that will not get displayed")
```


Logging a manually timed message:

```python
>>> timeit = logger.timeit("INFO")
>>> timeit.enter()
>>> timeit.log("long process")
>>> timeit.exit()
INFO - MyLogger - 2019-07-29 13:19:12,301 - Finished in 0:00:00.000528.
<loggable.TimedLoggable object at 0x10f1bc208>
```

Logging with a progress bar:

```python
>>> for x in logger.tqdm(range(10), "INFO"):
>>>     logger.info(x)
```

Manually updating a progress bar:

```python
>>> pbar = logger.track("INFO", desc="my progress bar", total=100).enter()
>>> pbar.update(10, "10% done!")
>>> pbar.update(35, "35% done!")
>>> pbar.exit()
INFO - MyLogger - 2019-07-29 13:19:12,320 - 10% done!
INFO - MyLogger - 2019-07-29 13:19:12,320 - 35% done!
 35%|████████████████▌| 10/100 [00:00<00:00, 13971.70it/s]
```