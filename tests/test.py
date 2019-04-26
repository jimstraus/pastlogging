import sys
import StringIO
import pytest

sys.path.append('..')     # to find pastlogging for import

output = None
logging = None
def setup():
    global output, logging
    if output:
        output.close()
    if sys.modules.get("pastlogging"):
        del sys.modules["pastlogging"]
        del logging
    import pastlogging
    logging = pastlogging
    logging.basicConfig()

def addHandler(logger):
    global output
    output = StringIO.StringIO()
    handler = logging.StreamHandler(output)
    formatter = logging.Formatter(logging.BASIC_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

###################################

def test_basic_error():
    """Logging an error outputs an error"""
    setup()
    logger = logging.getLogger()
    addHandler(logger)
    logger.error("an error")
    result = output.getvalue()
    assert output.getvalue() == "ERROR:root:an error\n"
    del logger

def test_basic_error_root():
    """Logging an error outputs an error"""
    setup()
    logger = logging.getLogger()
    addHandler(logger)
    logging.error("an error")
    result = output.getvalue()
    assert output.getvalue() == "ERROR:root:an error\n"

def test_basic_error_named():
    """Logging an error outputs an error"""
    setup()
    logger = logging.getLogger("abc")
    addHandler(logger)
    logger.error("an error")
    result = output.getvalue()
    assert output.getvalue() == "ERROR:abc:an error\n"
    del logger

def test_info_does_not_log():
    """Logging an info doesn't display'"""
    setup()
    logger = logging.getLogger()
    addHandler(logger)
    logger.info("an info")
    result = output.getvalue()
    assert result == ""
    del logger

def test_info_and_error_log():
    setup()
    logger = logging.getLogger()
    addHandler(logger)
    logger.info("an info")
    logger.error("an error")
    result = output.getvalue()
    assert result == "INFO:root:an info\nERROR:root:an error\n"
    del logger

def test_reset():
    setup()
    logger = logging.getLogger()
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
    logger = logging.getLogger()
    addHandler(logger)
    logger.setLevel(logging.INFO)
    logger.info("an info")
    result = output.getvalue()
    assert result == "INFO:root:an info\n"
    del logger

def test_setmax():
    setup()
    logger = logging.getLogger()
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
    logger = logging.getLogger()
    addHandler(logger)
    logger.setMinLevel(logging.INFO)
    logger.debug("a debug")
    logger.info("an info")
    logger.error("an error")
    result = output.getvalue()
    assert result == "INFO:root:an info\nERROR:root:an error\n"
    del logger

def test_multiple_names():
    setup()
    logger = logging.getLogger()
    addHandler(logger)
    loggera = logging.getLogger("a")
    loggerab = logging.getLogger("a.b")
    loggera.setLevel(logging.WARNING)
    loggerab.setLevel(logging.WARNING)
    logger.debug("root debug")
    loggera.debug("a debug")
    loggerab.debug("ab debug")
    loggerab.error("ab error")
    result = output.getvalue()
    assert result == "DEBUG:root:root debug\nDEBUG:a:a debug\nDEBUG:a.b:ab debug\nERROR:a.b:ab error\n"
    del logger
    del loggera
    del loggerab

