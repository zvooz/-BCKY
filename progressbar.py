# -*- coding: utf-8 -*- 

import datetime
import sys
from terminalcontroller.terminalcontroller import normal, green, error, warn, TerminalController


class ProgressBar:
    current_height = 0
    current_err_height = 0
    progress_report_count = 0
    progress_record = []


    def __init__(self,
                 current_height=0,
                 current_err_height=0,
                 progress_report_count=0,
                 progress_record=[]
                 ):
        self.current_height = current_height
        self.current_err_height = current_err_height
        self.progress_report_count = progress_report_count
        self.progress_record = progress_record


    def mv_line_by(self, delta_height=0):
        """not thread-safe"""
        term = TerminalController()
        mvmt = term.UP if delta_height < 0 else term.DOWN
        for i in range(0, abs(delta_height)):
            sys.stdout.write(mvmt)
            sys.stdout.flush()
        self.current_height += delta_height


    def mv2line(self, new_height):
        self.mv_line_by(new_height - self.current_height)


    def rm_line(self, line_height=current_height):
        self.mv2line(line_height)
        term = TerminalController()
        sys.stdout.write(term.CLEAR_EOL)
        sys.stdout.flush()
        sys.stdout.write(term.CLEAR_BOL)
        sys.stdout.flush()


    def rm_progress_lines(self, line_count=progress_report_count):
        for i in range(0, line_count):
            self.rm_line(line_height=self.current_err_height + line_count)
        self.mv2line(self.current_err_height)


    def restore_progress_report(self, ):
        i = 0
        for progress in self.progress_record:
            if progress:
                self.mv2line(self.current_err_height + i)
                sys.stdout.write(progress)
                sys.stdout.flush()
                i += 1
    
    
    def report(self, msg):
        """not thread-safe"""

        old_height = self.current_height

        msg = str(msg)

        try:
            newline_count = msg.count("\n") + 1
        except:
            newline_count = 1

        self.rm_progress_lines(line_count=self.progress_report_count)
        normal(msg)
        self.mv_line_by(1)

        self.current_err_height += newline_count

        self.rm_progress_lines(line_count=self.progress_report_count)
        self.restore_progress_report()

        self.mv2line(old_height + newline_count)
    
    
    def err_report(self, err_msg):
        """not thread-safe"""

        old_height = self.current_height

        err_msg = str(err_msg)

        try:
            newline_count = err_msg.count("\n") + 1
        except:
            newline_count = 1

        self.rm_progress_lines(line_count=self.progress_report_count)
        error(err_msg)
        self.mv_line_by(1)

        self.current_err_height += newline_count

        self.rm_progress_lines(line_count=self.progress_report_count)
        self.restore_progress_report()

        self.mv2line(old_height + newline_count)


    def wrn_report(self, wrn_msg):
        """not thread-safe"""

        old_height = self.current_height

        wrn_msg = str(wrn_msg)

        try:
            newline_count = wrn_msg.count("\n") + 1
        except:
            newline_count = 1

        self.rm_progress_lines(line_count=self.progress_report_count)
        warn(wrn_msg)
        self.mv_line_by(1)

        self.current_err_height += newline_count

        self.rm_progress_lines(line_count=self.progress_report_count)
        self.restore_progress_report()

        self.mv2line(old_height + newline_count)


    def out(self,
            iteration	= 0,
            total		= 0,
            start_time	= datetime.datetime.now(),
            prefix		= u"",
            suffix		= u"done",
            decimals	= 1,
            length		= 100,
            fills		= [u'', u'▏', u'▎', u'▍', u'▌', u'▋', u'▊', u'▉', u'█'],
            waves		= ['', u'▁', u'▂', u'▃', u'▄', u'▅', u'▆', u'▇', u'█'],
            position	= 0
            ):
        u"""
		printProgressBar() - Print iterations progress. Call in a loop to create terminal progress bar.
		@params:
			iteration	- Required: current iteration									Int
			total		- Required: total iterations									Int
			prefix		- Optional: prefix string										Str
			suffix		- Optional: suffix string										Str
			decimals	- Optional: positive number of decimals in percent complete		Int
			length		- Optional: character length of bar								Int
			fills		- Optional: horizontal bar fill characters						[Str]
			waves		- Optional: vertical bar fill characters						[Str]
			position	- Optional: on which line is this progress bar printed			Int
		"""

        for i in range(len(self.progress_record), self.progress_report_count):
            self.progress_record.append(None)

        current_time = datetime.datetime.now()
        secs_in_time = ((current_time - start_time) * (total - iteration) // (iteration if iteration != 0 else 1)).total_seconds()
        minutes_left = secs_in_time / 60
        seconds_left = secs_in_time % 60

        percent = (u"{0:." + str(decimals) + u"f}").format(100 * ((iteration / float(total)) if total != 0 else 1))

        if total == 0:
            big_length = length
            smo_length = 0
        else:
            ratio_done = length * iteration / float(total)
            big_length = int(ratio_done)
            smo_length = int((ratio_done % 1) * (len(fills) - 1))

        bar = fills[-1] * big_length + fills[smo_length] + u'-' * (length - big_length - (1 if smo_length > 0 else 0))

        progress = u"\r%-16s |%s| %6s%% %s (%4d/%-4d)\ttime remaining: %3d:%02d\r" % (prefix, green(bar), percent, suffix, iteration, total, minutes_left, seconds_left)
        self.progress_record[position] = progress
        self.mv2line(self.current_err_height + position)
        sys.stdout.write(progress)
        sys.stdout.flush()
        self.mv2line(self.current_err_height + self.progress_report_count)


def test():
    from random import randint

    start_time = datetime.datetime.now()
    progress_bar = ProgressBar(progress_report_count=3)

    l1 = range(randint(5, 10))
    l2 = range(randint(25, 50))
    l3 = range(randint(125, 250))

    progress_bar.out(iteration=0, total=len(l1), start_time=start_time, position=0)
    progress_bar.out(iteration=0, total=len(l2), start_time=start_time, position=1)
    progress_bar.out(iteration=0, total=len(l3), start_time=start_time, position=2)

    for i in l1:
        progress_bar.out(iteration=i + 1, total=len(l1), start_time=start_time, position=0)
        for j in l2:
            progress_bar.out(iteration=j + 1, total=len(l2), start_time=start_time, position=1)
            for k in l3:
                progress_bar.out(iteration=k + 1, total=len(l3), start_time=start_time, position=2)

    progress_bar.mv_line_by(1)
    sys.stdout.flush()


if __name__ == "__main__":
    test()
