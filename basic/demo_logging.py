import sys

CRITICAL = 50
ERROR    = 40
WARNING  = 30
INFO     = 20
DEBUG    = 10
NOTSET   = 0

_level_dict = {
    CRITICAL: "CRIT",
    ERROR: "ERROR",
    WARNING: "WARN",
    INFO: "INFO",
    DEBUG: "DEBUG",
}

_stream = sys.stderr

class LogRecord:
    def __init__(self):
        self.__dict__ = {}

    def __getattr__(self, key):
        return self.__dict__[key]

class Handler:
    def __init__(self):
        pass

    def setFormatter(self, fmtr):
        pass

class Logger:

    level = NOTSET
    handlers = []
    record = LogRecord()

    def __init__(self, name):
        self.name = name

    def _level_str(self, level):
        l = _level_dict.get(level)
        if l is not None:
            return l
        return "LVL%s" % level

    def setLevel(self, level):
        self.level = level

    def isEnabledFor(self, level):
        return level >= (self.level or _level)

    def log(self, level, msg, *args):
        if self.isEnabledFor(level):
            levelname = self._level_str(level)
            if args:
                msg = msg % args
            if self.handlers:
                d = self.record.__dict__
                d["levelname"] = levelname
                d["levelno"] = level
                d["message"] = msg
                d["name"] = self.name
                for h in self.handlers:
                    h.emit(self.record)
            else:
                print(levelname, ":", self.name, ":", msg, sep="", file=_stream)

    def debug(self, msg, *args):
        self.log(DEBUG, msg, *args)

    def info(self, msg, *args):
        self.log(INFO, msg, *args)

    def warning(self, msg, *args):
        self.log(WARNING, msg, *args)

    def error(self, msg, *args):
        self.log(ERROR, msg, *args)

    def critical(self, msg, *args):
        self.log(CRITICAL, msg, *args)

    def exc(self, e, msg, *args):
        self.log(ERROR, msg, *args)
        sys.print_exception(e, _stream)

    def addHandler(self, hndlr):
        self.handlers.append(hndlr)

_level = INFO
_loggers = {}

def getLogger(name="root"):
    if name in _loggers:
        return _loggers[name]
    l = Logger(name)
    _loggers[name] = l
    return l

def info(msg, *args):
    getLogger().info(msg, *args)

def debug(msg, *args):
    getLogger().debug(msg, *args)

def basicConfig(level=INFO, filename=None, stream=None, format=None):
    global _level, _stream
    _level = level
    if stream:
        _stream = stream
    if filename is not None:
        print("basicConfig: filename arg is not supported")
    if format is not None:
        print("basicConfig: format arg is not supported")

if __name__ == "__main__":

    basicConfig(level=INFO)
    log = getLogger("test")
    log.debug("Test message: %d(%s)", 100, "foobar")
    log.info("Test message2: %d(%s)", 100, "foobar")
    log.warning("Test message3: %d(%s)")
    log.error("Test message4")
    log.critical("Test message5")
    info("Test message6")

    try:
        1/0
    except Exception as e:
        log.exc(e, "Some trouble (%s)", "expected")

    class MyHandler(Handler):
        def emit(self, record):
            print("levelname=%(levelname)s name=%(name)s message=%(message)s" % record.__dict__)

    getLogger().addHandler(MyHandler())
    info("Test message7")
