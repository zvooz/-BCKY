# -*- coding: utf-8 -*- 

import os
import platform
import shlex
import subprocess
from portfolios import Portfolios


class DirectoryElements:
	def __init__(self):
		pass
	
	portfolios = Portfolios()
	
	ckdirs = u"ckdirs"
	
	plots_subdir = os.path.join(u"docs", u"plots")
	portfolios_subdir = u"portfolios"
	EODs_subdir = u"aggregated EODs"
	indices_subdirs = portfolios.indices.keys()

	cur_dir = os.getcwd()
	plots_dir = os.path.join(cur_dir, plots_subdir)
	portfolios_dir = os.path.join(cur_dir, portfolios_subdir)
	EODs_dir = os.path.join(portfolios_dir, EODs_subdir)
	indices_dirs = {}
	for index_subdir in indices_subdirs:
		indices_dirs[index_subdir] = os.path.join(portfolios_dir, index_subdir)
	# indices_dirs = {index_subdir: os.path.join(portfolios_dir, index_subdir) for index_subdir in indices_subdirs}

	ckdirs_args = shlex.split(
		u"\""
		+ os.path.join(cur_dir, u"bin64" if platform.architecture()[0] == u"64bit" else u"bin32", ckdirs)
		+ u"\" \"" + EODs_dir
		+ u"\" \"" + plots_dir
		+ u"\" "
		+ u' '.join([u"\"" + index_dir + u"\"" for index_dir in indices_dirs.values()])
	)
	
	ckdirs_exec = subprocess.Popen(ckdirs_args)
	ckdirs_exec.communicate()
