# Copyright 2-19 by Jim Straus. All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of Vinay Sajip
# not be used in advertising or publicity pertaining to distribution
# of the software without specific, written prior permission.
# JIM STRAUS DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
# ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# JIM STRAUS BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
# ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

'''
Extension to the Logging package for Python.

Copyright (C) 2019 Jim Straus. All Rights Reserved.

This module lets you log all your debugging and info information, but only
if a warning or error is logged are they emitted to the log.  The normal level
controls what is stored and the threshold controls what causes the stored messages
to be emitted.

The defaults if you don't set them are to log everything (level=DEBUG) and emit
when greater or equal to WARNING.

You can also reset the saved log information, which might be useful when a handler
starts, for example.  You can also set the maximum number of stored log items, to
keep a long running program from using up all of memory.

Pretty much all the documentation for the standard Python logging applies.  Beyond
the addition of:
  setThreshold(level)
  setMax(max)
  reset()
the only change in meaning is setLevel(level) affects what is stored, not what
emitted.  If you want to change what is immediately emitted, use setThreshold().

setMax() takes the maximum number of entries to store.  If the number is -1, all
entries are stored (no maximum).

To use, simply 'import pastlogging as logging' and log away!
'''

import logging, sys, warnings

__all__ = []
__all__ += logging.__all__

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

class PastLogger(logging.Logger):

    def __init__(self, name, level=logging.NOTSET, threshold=logging.NOTSET):
        logging.Logger.__init__(self, name, level)
        self._past = []
        self._threshold = threshold
        self._pastmax = -1

    def _log(self, level, msg, args, exc_info=None, extra=None):
        """
        Low-level logging routine which creates a LogRecord and then calls
        all the handlers of this logger to handle the record.
        """
        if logging._srcfile:
            #IronPython doesn't track Python frames, so findCaller raises an
            #exception on some versions of IronPython. We trap it here so that
            #IronPython can use logging.
            try:
                fn, lno, func = self.findCaller()
            except ValueError:
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
        else:
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        if exc_info:
            if not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
        record = self.makeRecord(self.name, level, fn, lno, msg, args, exc_info, func, extra)
        if level < self._threshold:
            self._past.append(record)
            if self._pastmax >= 0 and self._pastmax < len(self._past):
              del self._past[0:len(self._past) - self._pastmax]
        else:
            for rec in self._past:
                self.handle(rec)
            self._past = []
            self.handle(record)

    def setThreshold(self, level):
        """
        Set the logging threshold of this handler.
        """
        self._threshold = logging._checkLevel(level)
        if self._threshold < self.level:
            self.level = _checkLevel(level)

    def setMax(self, max):
        if isinstance(max, (int, long)):
            self._pastmax = max

    def reset(self):
        """
        Reset the past.  Useful at the start of a new sequence.
        """
        self._past = []


class PastRootLogger(PastLogger):
    """
    A root logger is not that different to any other logger, except that
    it must have a logging level and there is only one instance of it in
    the hierarchy.
    """
    def __init__(self, level, threshold):
        """
        Initialize the logger with the name "root".
        """
        PastLogger.__init__(self, "root", level, threshold)

_loggerClass = PastLogger

logging.root = PastRootLogger(logging.DEBUG, logging.WARNING)
logging.Logger.root = logging.root
logging.Logger.manager = logging.Manager(logging.Logger.root)

def getLogger(name=None):
    """
    Return a logger with the specified name, creating it if necessary.

    If no name is specified, return the root logger.
    """
    logging.setLoggerClass(PastLogger)
    if name:
        return PastLogger.manager.getLogger(name)
    else:
        return logging.root

def critical(msg, *args, **kwargs):
    """
    Log a message with severity 'CRITICAL' on the root logger.
    """
    if len(logging.root.handlers) == 0:
        basicConfig()
    logging.root.critical(msg, *args, **kwargs)

fatal = critical

def error(msg, *args, **kwargs):
    """
    Log a message with severity 'ERROR' on the root logger.
    """
    if len(logging.root.handlers) == 0:
        basicConfig()
    logging.root.error(msg, *args, **kwargs)

def exception(msg, *args, **kwargs):
    """
    Log a message with severity 'ERROR' on the root logger,
    with exception information.
    """
    kwargs['exc_info'] = 1
    error(msg, *args, **kwargs)

def warning(msg, *args, **kwargs):
    """
    Log a message with severity 'WARNING' on the root logger.
    """
    if len(logging.root.handlers) == 0:
        basicConfig()
    logging.root.warning(msg, *args, **kwargs)

warn = warning

def info(msg, *args, **kwargs):
    """
    Log a message with severity 'INFO' on the root logger.
    """
    if len(logging.root.handlers) == 0:
        basicConfig()
    logging.root.info(msg, *args, **kwargs)

def debug(msg, *args, **kwargs):
    """
    Log a message with severity 'DEBUG' on the root logger.
    """
    if len(logging.root.handlers) == 0:
        basicConfig()
    logging.root.debug(msg, *args, **kwargs)

def log(level, msg, *args, **kwargs):
    """
    Log 'msg % args' with the integer severity 'level' on the root logger.
    """
    if len(logging.root.handlers) == 0:
        basicConfig()
    logging.root.log(level, msg, *args, **kwargs)

def disable(level):
    """
    Disable all logging calls of severity 'level' and below.
    """
    logging.root.manager.disable = level

def basicConfig(**kwargs):
  logging.root.setThreshold(kwargs.get("threshold", logging.WARNING))
  logging.root.setMax(kwargs.get("max", -1))
  logging.basicConfig(**kwargs)


# Warnings integration

def _showwarning(message, category, filename, lineno, file=None, line=None):
    """
    Implementation of showwarnings which redirects to logging, which will first
    check to see if the file parameter is None. If a file is specified, it will
    delegate to the original warnings implementation of showwarning. Otherwise,
    it will call warnings.formatwarning and will log the resulting string to a
    warnings logger named "py.warnings" with level logging.WARNING.
    """
    if file is not None:
        if logging._warnings_showwarning is not None:
            logging._warnings_showwarning(message, category, filename, lineno, file, line)
    else:
        s = warnings.formatwarning(message, category, filename, lineno, line)
        logger = getLogger("py.warnings")
        if not logger.handlers:
            logger.addHandler(logging.NullHandler())
        logger.warning("%s", s)

def captureWarnings(capture):
    """
    If capture is true, redirect all warnings to the logging package.
    If capture is False, ensure that warnings are not redirected to logging
    but to their original destinations.
    """
    global _warnings_showwarning
    if capture:
        if logging._warnings_showwarning is None:
            logging._warnings_showwarning = warnings.showwarning
            warnings.showwarning = _showwarning
    else:
        if logging._warnings_showwarning is not None:
            warnings.showwarning = logging._warnings_showwarning
            _warnings_showwarning = None
