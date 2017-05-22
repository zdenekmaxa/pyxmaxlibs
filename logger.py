"""
Python wrapper class for logging module.

Author: Zdenek Maxa

"""

import sys
import traceback
import linecache
import logging


class Logger(logging.getLoggerClass()):
    """
    Customised Logger.

    Should any customisation on logging calls be necessary, then:
    def fatal(self, msg):
        # custom actions
        logging.Logger.fatal(self, msg)

    """
    # handler for logging into a file
    log_file_handler = None
    log_file_name = None


    def __init__(self, name="Logger", log_file=None, level=logging.DEBUG):
        # initialise logger, necessary
        logging.Logger.__init__(self, name)

        self.setLevel(level)  # should be set for further created handlers

        # %(name)-12s gives name as given here: name = "Logger"
        fs = "%(asctime)s %(levelname)-8s %(message)s"
        formatter = logging.Formatter(fs)

        # logging to console, sys.stdout
        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(formatter)
        self.addHandler(console)

        if log_file:
            self.log_file_name = log_file
            self.log_file_handler = logging.FileHandler(log_file)
            self.log_file_handler.setLevel(level)
            self.log_file_handler.setFormatter(formatter)
            self.addHandler(self.log_file_handler)

        self.debug("Logger instance initialised.")


    def close(self):
        """
        Closing the logger.
        This can't be put into __del__() - gives error (file already closed).

        """
        self.debug("Logger closing.")
        if self.log_file_handler:
            self.log_file_handler.flush()
            self.log_file_handler.close()


    def get_traceback_simple(self):
        """
        Returns formatted traceback of the most recent exception.
        
        """
        # sys.exc_info() most recent exception
        trace = traceback.format_exception(*sys.exc_info())
        tb_simple = "".join(trace)  # may want to add '\n'
        return tb_simple


    def get_traceback_full(self, local_levels = 5):
        """
        Returns formatted traceback of the most recent exception.
        Could write into a file-like object (argument would be
        output = sys.stdout), now returns result in formatted string.
        
        """
        tb_full = "".join([78 * '-', '\n'])
        tb_full = "".join([tb_full, "Problem: %s\n" % sys.exc_info()[1]])
        
        trace = sys.exc_info()[2]
        stack_str = []
        while trace is not None:
            frame = trace.tb_frame
            lineno = trace.tb_lineno
            code = frame.f_code
            filename = code.co_filename
            function = code.co_name
            if filename.endswith(".py"):
                line = linecache.getline(filename, lineno)
            else:
                line = None
            stack_str.append((filename, lineno, function, line, frame))
            trace = trace.tb_next

        tb_full = "".join([tb_full, "Traceback:\n"])
        local_level = max(len(stack_str) - local_levels, 0)
        for i in range(len(stack_str)):
            (filename, lineno, name, line, frame) = stack_str[i]
            output_line = (" File '%s', line %d, in %s (level %i):\n" %
                          (filename, lineno, name, i))
            tb_full = "".join([tb_full, output_line])
            if line:
                tb_full = "".join([tb_full, "  %s\n" % line])
            if i >= local_level:
                # want to see complete stack if exception came from a template
                pass
        
        tb_full = "".join([tb_full, 78 * '-', '\n'])

        del stack_str[:]
        frame, trace = None, None
        return tb_full
