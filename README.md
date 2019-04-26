Python logging where your full debugging messages only appear if an problem occurs

This module lets you log all your debugging and info information, but only
if a warning or error is logged are they emitted to the log.  setLevel() controls
what messages are actually logged, as normal, but also all previous lower levels are
also logged.  To prevent some of the lower levels from being logged, setMinLevel() to
cutoff desired.

The defaults if you don't set them are to log everything (level=NOTSET) and emit
when greater or equal to WARNING.

You can also reset() the saved log information, which might be useful when a handler
starts, for example.  You can also setMax() the maximum number of stored log items, to
keep a long running program from using up all of memory.  The default is 1000 items, and
if the max is set to -1, there is no limit to the number of messages kept.

Pretty much all the documentation for the standard Python logging applies.  Beyond
the addition of:
* *setMinLevel(level)
* setMax(max)
* reset()
the only change in meaning is setMinLevel(level) affects what is stored, not what
emitted.

setMax() takes the maximum number of entries to store.  If the number is -1, all
entries are stored (no maximum).

To use, simply 'import pastlogging as logging' and log away!

If you used to use 'import logging' and then 'logging.warning()' change to:
'import pastlogging' and 'logging = getLogger()'.

If you used 'import logging' and 'logger = logging.getLogger()' and 'logger.warning()'
just change the import to 'import pastlogging as logging'.
