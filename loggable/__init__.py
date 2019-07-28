import logging
import math
import pprint
import traceback


def new_logger(name, level=logging.ERROR):
    """Instantiate a new logger with the given name. If channel handler exists, do not create a new one."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # make stream handler
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.tb_limit = 0
        formatter = logging.Formatter(
            "%(levelname)s - %(name)s - %(asctime)s - %(message)s"
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    else:
        ch = logger.handlers[0]
    return logger, ch


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

    @property
    def _logger_name(self):
        name = "{}(id={})".format(self.__class__, id(self))
        return name

    @property
    def _logger(self):
        return new_logger(self._logger_name)[0]


    def set_log_level(self, level, tb_limit=0):
        for h in self._logger.handlers:
            h.setLevel(level)
            h.tb_limit = tb_limit

    def set_verbose(self, verbose, tb_limit=0):
        if verbose:
            self.set_log_level(logging.INFO, tb_limit)
        else:
            self.set_log_level(logging.ERROR, tb_limit)

    def _pprint_data(
        self, data, width=80, depth=10, max_list_len=20, compact=True, indent=1
    ):
        return pprint.pformat(
            condense_long_lists(data, max_list_len=max_list_len),
            indent=indent,
            width=width,
            depth=depth,
            compact=compact,
        )

    def _info(self, msg):
        self._logger.info(msg)
        if self._logger.isEnabledFor(logging.INFO):
            tb_limit = self._logger.handlers[0].tb_limit
            if tb_limit:
                traceback.print_stack(limit=tb_limit)

    def _error(self, msg):
        self._logger.error(msg)
        if self._logger.isEnabledFor(logging.ERROR):
            tb_limit = self._logger.handlers[0].tb_limit
            if tb_limit:
                traceback.print_stack(limit=tb_limit)
