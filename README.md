# pastlogging — Logging extension for Python

**Source code:** https://github.com/jimstraus/pastlogging

This module extends the built in logging module in Python.  It supports both Python 2.3 and greater and Python 3.X.

The key benefit is to provide a mechanism where your logs are not cluttered with _info_ and _debug_ messages, but when an _warning_ or _error_ occurs, you get all the previous _info_ and _debug_ messages.  Because it is based on the standard logging module, all the usual flexibility in terms of handlers, filters, name spaces, etc. are available.

Please read the Python Standard Library documentation for logging to understand all the normal options and mechanisms for logging.

# PastLogger Objects
PastLoggers are extended with the following methods.  _Not that PastLoggers are generated and retrieved using the same mechanism as the normal logger._

```
logging.getLogger()
```

PastLogger.**setLevel**_(level)_

Sets the threshold for this logger to _level_. Logging messages which are less severe than level will be held (up to a maximum number, see below).  If a message equals or is greater than the threshold, then all held messages and the current message are sent to the log(s).

PastLogger.**setMinLevel**_(level)_

Sets the minimum _level_ of messages to be held.  No messages below the minimum level will be held.

PastLogger.**setMax**_(number)_

Sets the _number_ of messages to be held.  The default is 1000 and if set to -1 there is no limit.

PastLogger.**reset**_()_

Resets the buffer holding messages.  This can be used when entering code where the previous operations completed either successfully or unsuccessfully.

# PastLogger Usage

To minimize the changes to your code, you may

```
import pastlogging as logging
```

At that point, all your code using logging should work as expected.

Since the previous log messages are sent to the logs at the same time, the timestamp stored in the LogRecords themselves.  This can be configured using

```
logging.basicConfig(format='%(asctime)s %(message)s')
```

Or see the builtin logging documentation for further formatting optinos.
