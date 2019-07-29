import logging
import math
import pprint
import traceback
from logging import DEBUG, INFO, CRITICAL, ERROR, WARNING, WARN
from colorlog import ColoredFormatter
from tqdm import tqdm


class TqdmLoggingHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET, tqdm=tqdm):
        super().__init__(level)
        self._tqdm = tqdm

    def emit(self, record):
        try:
            msg = self.format(record)
            self._tqdm.write(msg)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


def condense_long_lists(d, max_list_len=20):
    """
    Condense the long lists in a dictionary

    :param d: dictionary to condense
    :type d: dict
    :param max_len: max length of lists to display
    :type max_len: int
    :return:
    :rtype:
    """
    if isinstance(d, dict):
        return_dict = {}
        for k in d:
            return_dict[k] = condense_long_lists(dict(d).pop(k))
        return dict(return_dict)
    elif isinstance(d, list):
        if len(d) > max_list_len:
            g = max_list_len / 2
            return d[: math.floor(g)] + ["..."] + d[-math.ceil(g) :]
        else:
            return d[:]
    return str(d)


class Loggable(object):

    DEFAULT_FORMAT = "%(log_color)s%(levelname)s - %(name)s - %(asctime)s - %(message)s"
    DEFAULT_COLORS = {
                        'DEBUG': 'cyan',
                        'INFO': 'white',
                        'SUCCESS:': 'green',
                        'WARNING': 'yellow',
                        'ERROR': 'red',
                        'CRITICAL': 'red,bg_white'
                    }

    def __init__(self, object_or_name, format=None, log_colors=None, tqdm=tqdm):
        if isinstance(object_or_name, str):
            self.name = object_or_name
        else:
            self.name = "{}(id={})".format(object_or_name.__class__, id(object_or_name))

        self.format = format or self.DEFAULT_FORMAT
        self.log_colors = log_colors or self.DEFAULT_COLORS
        self._tqdm = tqdm

    def new_logger(self, name, level=logging.ERROR):
        """Instantiate a new logger with the given name. If channel handler exists, do not create a new one."""
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # make stream handler
        if not logger.handlers:
            handler = TqdmLoggingHandler(level, tqdm=self._tqdm)
            handler.tb_limit = 0
            formatter = ColoredFormatter(
                self.format,
                log_colors=self.log_colors
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        else:
            handler = logger.handlers[0]
        return logger, handler

    @property
    def logger(self):
        return self.new_logger(self.name)[0]

    def set_tb_limit(self, limit):
        for h in self.logger.handlers:
            h.tb_limit = limit

    def _get_level(self, level):
        if isinstance(level, str):
            try:
                level = {
                    "INFO": INFO,
                    "ERROR": ERROR,
                    "DEBUG": DEBUG,
                    "CRITICAL": CRITICAL,
                    "WARNING": WARNING,
                    "WARN": WARN
                }[level.upper()]
            except KeyError as e:
                raise KeyError("Level {} not recognized.".format(level)) from e
        return level

    def set_level(self, level, tb_limit=None):
        level = self._get_level(level)
        for h in self.logger.handlers:
            h.setLevel(level)
        if tb_limit is not None:
            self.set_tb_limit(tb_limit)

    def set_verbose(self, verbose, tb_limit=0):
        if verbose:
            self.set_level(logging.INFO, tb_limit)
        else:
            self.set_level(logging.ERROR, tb_limit)

    def pprint_data(
        self, data, width=80, depth=10, max_list_len=20, compact=True, indent=1
    ):
        return pprint.pformat(
            condense_long_lists(data, max_list_len=max_list_len),
            indent=indent,
            width=width,
            depth=depth,
            compact=compact,
        )

    pprint = pprint_data

    def tqdm(self, iterable, level, *args, **kwargs):
        """Logging """
        level = self._get_level(level)
        if self.logger.isEnabledFor(level):
            progress_bar = self._tqdm(iterable, *args, **kwargs)
            progress_bar.set_description("{:8} {}".format(logging._levelToName[level], progress_bar.desc))
            return progress_bar
        else:
            return iterable

    progress = tqdm

    def log(self, msg, level):
        level = self._get_level(level)
        self.logger.log(level, msg)
        if self.logger.isEnabledFor(level):
            tb_limit = self.logger.handlers[0].tb_limit
            if tb_limit:
                traceback.print_stack(limit=tb_limit)

    def critical(self, msg):
        self.log(msg, CRITICAL)

    def error(self, msg):
        self.log(msg, ERROR)

    def warn(self, msg):
        self.log(msg, WARNING)

    def info(self, msg):
        self.log(msg, INFO)

    def debug(self, msg):
        self.log(msg, DEBUG)


class LoggableFactory(object):

    def __init__(self, format=None, log_colors=None, tqdm=tqdm):
        self.format = format
        self.log_colors = log_colors
        self._tqdm = tqdm

    def __call__(self, name):
        return Loggable(name, format=self.format, log_colors=self.log_colors, tqdm=self._tqdm)