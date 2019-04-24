# -*- coding: utf-8 -*- 

import os
import platform
import shlex
import subprocess



class DirectoryElements:
	ckdirs = "bin64/ckdirs" if platform.architecture()[0] == "64bit" else "bin32/ckdirs"

	plots_subdir = "plots"
	portfolios_subdir = "portfolios"
	EODs_subdir = "aggregated EODs"
	BCKY_A_subdir = "^BCKY.A"
	BCKY_B_subdir = "^BCKY.B"
	BCKY_V_subdir = "^BCKY.V"

	cur_dir = os.getcwd()
	plots_dir = os.path.join(cur_dir, plots_subdir)
	portfolios_dir = os.path.join(cur_dir, portfolios_subdir)
	EODs_dir = os.path.join(portfolios_dir, EODs_subdir)
	BCKY_A_dir = os.path.join(portfolios_dir, BCKY_A_subdir)
	BCKY_B_dir = os.path.join(portfolios_dir, BCKY_B_subdir)
	BCKY_V_dir = os.path.join(portfolios_dir, BCKY_V_subdir)

	ckdirs_args = shlex.split("\"" + os.path.join(cur_dir, ckdirs)
		+ "\" -e \"" + EODs_dir
		+ "\" -A \"" + BCKY_A_dir
		+ "\" -B \"" + BCKY_B_dir
		+ "\" -V \"" + BCKY_V_dir
		+ "\" -p \"" + plots_dir
		+ "\"")
	ckdirs_exec = subprocess.Popen(ckdirs_args)
	ckdirs_exec.communicate()
