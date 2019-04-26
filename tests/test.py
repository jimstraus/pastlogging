import sys
import pytest
import io

sys.path.append('..')     # to find pastlogging for import

PY3 = sys.version_info[0] == 3

output = None
plogging = None
def setup():
    global output, plogging
    if output:
        output.close()
    if sys.modules.get("pastlogging"):
        del sys.modules["pastlogging"]
        del plogging
    import pastlogging
    plogging = pastlogging
    plogging.basicConfig()

def addHandler(logger):
    global plogging, output
    if PY3:
        output = io.StringIO()
    else:
        output = io.BytesIO()
    handler = plogging.StreamHandler(output)
    formatter = plogging.Formatter(plogging.BASIC_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

###################################

def test_basic_error():
    """Logging an error outputs an error"""
    setup()
    logger = plogging.getLogger()
    addHandler(logger)
    logger.error("an error")
    result = output.getvalue()
    assert output.getvalue() == "ERROR:root:an error\n"
    del logger

def test_basic_error_root():
    """Logging an error outputs an error"""
    setup()
    logger = plogging.getLogger()
    addHandler(logger)
    plogging.error("an error")
    result = output.getvalue()
    assert output.getvalue() == "ERROR:root:an error\n"
    del logger

def test_basic_error_named():
    """Logging an error outputs an error"""
    setup()
    logger = plogging.getLogger("abc")
    addHandler(logger)
    logger.error("an error")
    result = output.getvalue()
    assert output.getvalue() == "ERROR:abc:an error\n"
    del logger

def test_info_does_not_log():
    """Logging an info doesn't display'"""
    setup()
    logger = plogging.getLogger()
    addHandler(logger)
    logger.info("an info")
    result = output.getvalue()
    assert result == ""
    del logger

def test_info_and_error_log():
    setup()
    logger = plogging.getLogger()
    addHandler(logger)
    logger.info("an info")
    logger.error("an error")
    result = output.getvalue()
    assert result == "INFO:root:an info\nERROR:root:an error\n"
    del logger

def test_reset():
    setup()
    logger = plogging.getLogger()
    addHandler(logger)
    logger.info("an info")
    logger.reset()
    logger.debug("a debug")
    logger.error("an error")
    result = output.getvalue()
    assert result == "DEBUG:root:a debug\nERROR:root:an error\n"
    del logger

def test_setlevel():
    setup()
    logger = plogging.getLogger()
    addHandler(logger)
    logger.setLevel(plogging.INFO)
    logger.info("an info")
    result = output.getvalue()
    assert result == "INFO:root:an info\n"
    del logger

def test_setmax():
    setup()
    logger = plogging.getLogger()
    addHandler(logger)
    logger.setMax(2)
    logger.info("info 1")
    logger.info("info 2")
    logger.info("info 3")
    logger.info("info 4")
    logger.error("an error")
    result = output.getvalue()
    assert result == "INFO:root:info 3\nINFO:root:info 4\nERROR:root:an error\n"
    del logger

def test_setminlevel():
    setup()
    logger = plogging.getLogger()
    addHandler(logger)
    logger.setMinLevel(plogging.INFO)
    logger.debug("a debug")
    logger.info("an info")
    logger.error("an error")
    result = output.getvalue()
    assert result == "INFO:root:an info\nERROR:root:an error\n"
    del logger

def test_multiple_names():
    setup()
    logger = plogging.getLogger()
    addHandler(logger)
    loggera = plogging.getLogger("a")
    loggerab = plogging.getLogger("a.b")
    loggera.setLevel(plogging.WARNING)
    loggerab.setLevel(plogging.WARNING)
    logger.debug("root debug")
    loggera.debug("a debug")
    loggerab.debug("ab debug")
    loggerab.error("ab error")
    result = output.getvalue()
    assert result == "DEBUG:root:root debug\nDEBUG:a:a debug\nDEBUG:a.b:ab debug\nERROR:a.b:ab error\n"
    del logger
    del loggera
    del loggerab

def test_multiple_names():
    setup()
    logger = plogging.getLogger()
    addHandler(logger)
    loggera = plogging.getLogger("a")
    loggerab = plogging.getLogger("a.b")
    loggera.setLevel(plogging.WARNING)
    loggerab.setLevel(plogging.WARNING)
    logger.debug("root debug")
    loggera.debug("a debug")
    loggerab.debug("ab debug")
    loggerab.error("ab error")
    result = output.getvalue()
    assert result == "DEBUG:root:root debug\nDEBUG:a:a debug\nDEBUG:a.b:ab debug\nERROR:a.b:ab error\n"
    del logger
    del loggera
    del loggerab

def test_using_logging_directly():
    setup()
    import logging
    logger = plogging.getLogger()
    addHandler(logger)
    logger.error("an error")
    logging.error("logging error")
    result = output.getvalue()
    assert output.getvalue() == "ERROR:root:an error\nERROR:root:logging error\n"
    del logger
