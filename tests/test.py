import sys
import StringIO

sys.path.append('..')
import pastlogging as logging

logging.basicConfig()

output = None
handler = None
logger = logging.getLogger()

def setup():
    global handler, output, logger
    output = StringIO.StringIO()
    handler = logging.StreamHandler(output)
    formatter = logging.Formatter(logging.BASIC_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.reset()
    logger.setLevel(logging.WARN)
    logger.setMinLevel(logging.NOTSET)
    logger.setMax(1000)

def cleanup():
    global handler, output
    logger.removeHandler(handler)
    output.close()


def test1():
    setup()
    logger.error("an error")
    result = output.getvalue() == "ERROR:root:an error\n"
    cleanup()
    return result

def test2():
    setup()
    logger.info("an info")
    result = output.getvalue() == ""
    cleanup()
    return result

def test3():
    setup()
    logger.info("an info")
    logger.error("an error")
    result = output.getvalue() == "INFO:root:an info\nERROR:root:an error\n"
    cleanup()
    return result

def test4():
    setup()
    logger.info("an info")
    logger.reset()
    logger.debug("a debug")
    logger.error("an error")
    result = output.getvalue() == "DEBUG:root:a debug\nERROR:root:an error\n"
    cleanup()
    return result

def test5():
    setup()
    logger.setLevel(logging.INFO)
    logger.info("an info")
    result = output.getvalue() == "INFO:root:an info\n"
    cleanup()
    return result

def test6():
    setup()
    logger.setMax(2)
    logger.info("info 1")
    logger.info("info 2")
    logger.info("info 3")
    logger.info("info 4")
    logger.error("an error")
    result = output.getvalue() == "INFO:root:info 3\nINFO:root:info 4\nERROR:root:an error\n"
    cleanup()
    return result


if __name__ == '__main__':
    if not test1():
        print "test1 failed"
    if not test2():
        print "test2 failed"
    if not test3():
        print "test3 failed"
    if not test4():
        print "test4 failed"
    if not test5():
        print "test5 failed"
    if not test6():
        print "test6 failed"
