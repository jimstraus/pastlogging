# MIT License
#
# Copyright (c) 2019 Jim Straus
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
  setMinLevel(level)
  setMax(max)
  reset()
the only change in meaning is setMinLevel(level) affects what is stored, not what
emitted.

setMax() takes the maximum number of entries to store.  If the number is -1, all
entries are stored (no maximum).

To use, simply 'import pastlogging as logging' and log away!

If you used to use 'import logging' and then 'logging.warning()' change to:
'import pastlogging' and 'logging = getLogger()'.

If you used 'import logging' and 'logger = logging.getLogger()' and 'logger.warning()'
just change the import to 'import pastlogging as logging'.
'''

import os, sys, warnings
from logging import *
import logging

class PastManager(logging.Manager):
    def __init__(self, rootnode):
        logging.Manager.__init__(self, rootnode)
        self._past = []
        self.pastmax = 1000

    def setMax(self, max):
        if isinstance(max, (int, long)):
            self.pastmax = max

    def addLogRecord(self, record):
        self._past.append(record)
        if self.pastmax >= 0 and self.pastmax < len(self._past):
          del self._past[0:len(self._past) - self.pastmax]

    def getLogRecords(self):
        return self._past

    def resetLogRecords(self):
        self._past = []

class PastLogger(Logger):
    def __init__(self, name, threshold=NOTSET, minlevel=NOTSET):
        Logger.__init__(self, name, minlevel)
        self.threshold = threshold

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
        if level < self.threshold:
            self.manager.addLogRecord(record)
        else:
            for rec in self.manager.getLogRecords():
                self.handle(rec)
            self.manager.resetLogRecords()
            self.handle(record)

    def setLevel(self, level):
        """
        Set the logging level of this logger.
        """
        self.threshold = logging._checkLevel(level)

    def setMinLevel(self, level):
        """
        Set the logging threshold of this handler.
        """
        self.level = logging._checkLevel(level)

    def setMax(self, max):
        self.manager.setMax(max)

    def reset(self):
        """
        Reset the past.  Useful at the start of a new sequence.
        """
        self.manager.resetLogRecords()

class PastRootLogger(PastLogger):
    """
    A root logger is not that different to any other logger, except that
    it must have a logging level and there is only one instance of it in
    the hierarchy.
    """
    def __init__(self, threshold, minlevel):
        """
        Initialize the logger with the name "root".
        """
        PastLogger.__init__(self, "root", threshold, minlevel)

logging._loggerClass = PastLogger

logging.root = PastRootLogger(WARNING, DEBUG)
Logger.root = logging.root
Logger.manager = PastManager(Logger.root)

def getLogger(name=None):
    """
    Return a logger with the specified name, creating it if necessary.

    If no name is specified, return the root logger.
    """
    setLoggerClass(PastLogger)
    if name:
        return Logger.manager.getLogger(name)
    else:
        return logging.root

def basicConfig(**kwargs):
    """
    Do basic configuration for the logging system.

    This function does nothing if the root logger already has handlers
    configured. It is a convenience method intended for use by simple scripts
    to do one-shot configuration of the logging package.

    The default behaviour is to create a StreamHandler which writes to
    sys.stderr, set a formatter using the BASIC_FORMAT format string, and
    add the handler to the root logger.

    A number of optional keyword arguments may be specified, which can alter
    the default behaviour.

    filename  Specifies that a FileHandler be created, using the specified
              filename, rather than a StreamHandler.
    filemode  Specifies the mode to open the file, if filename is specified
              (if filemode is unspecified, it defaults to 'a').
    format    Use the specified format string for the handler.
    datefmt   Use the specified date/time format.
    level     Set the root logger level to the specified level.
    stream    Use the specified stream to initialize the StreamHandler. Note
              that this argument is incompatible with 'filename' - if both
              are present, 'stream' is ignored.

    Note that you could specify a stream created using open(filename, mode)
    rather than passing the filename and mode in. However, it should be
    remembered that StreamHandler does not close its stream (since it may be
    using sys.stdout or sys.stderr), whereas FileHandler closes its stream
    when the handler is closed.
    """
    # Add thread safety in case someone mistakenly calls
    # basicConfig() from multiple threads
    logging._acquireLock()
    try:
        if len(logging.root.handlers) == 0:
            filename = kwargs.get("filename")
            if filename:
                mode = kwargs.get("filemode", 'a')
                hdlr = FileHandler(filename, mode)
            else:
                stream = kwargs.get("stream")
                hdlr = StreamHandler(stream)
            fs = kwargs.get("format", BASIC_FORMAT)
            dfs = kwargs.get("datefmt", None)
            fmt = Formatter(fs, dfs)
            hdlr.setFormatter(fmt)
            logging.root.addHandler(hdlr)
            level = kwargs.get("level")
            if level is not None:
                logging.root.setLevel(level)
            logging.root.setMinLevel(kwargs.get("minlevel", NOTSET))
            logging.root.setMax(kwargs.get("max", 1000))
    finally:
        logging._releaseLock()
