"""
Unittests for the logger module.

"""

import os
import tempfile
import logging

import pytest

from pyxmaxlibs.logger import Logger


class TestLogger(object):

    temp_log_file = None

    def test_logger(self):
        logger = Logger()
        logger = Logger(name="MyLogger")
        logger.debug("debugmsg")
        logger.warn("warnmsg")
        logger.error("errormsg")
        logger.critical("criticalmsg")
        logger.fatal("fatalmsg")
        assert logger.name == "MyLogger"
        logger.close()
   

    def test_logger_level(self, capsys):
        logger = Logger(level=logging.ERROR)
        logger.debug("donotappear")
        out, err = capsys.readouterr()
        assert out == ''
        logger.warn("donotappear")
        out, err = capsys.readouterr()
        assert out == ''
        logger.error("doappear")
        out, err = capsys.readouterr()
        assert str(out).endswith("doappear\n")
        logger.close()


    def test_logger_file_logging(self):
        fd, self.temp_log_file = tempfile.mkstemp()
        logger = Logger(log_file=self.temp_log_file)
        assert logger.level == logging.DEBUG
        msg = "my logging message"
        logger.debug(msg)
        logger.close()
        read_msg = open(self.temp_log_file, 'r').read()
        assert read_msg.find(msg) > 0


    def teardown_method(self, method):
        if self.temp_log_file:
            os.unlink(self.temp_log_file)


    def test_logger_exception_traceback(self):
        logger = Logger()
        try:
            1/0
        except:
            tb = logger.get_traceback_simple()
            #print tb
        try:
            1/0
        except:
            tb = logger.get_traceback_full()
            #print tb
