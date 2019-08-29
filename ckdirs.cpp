//
//	ckdirs.cpp
//	check and create the necessary directory structure for storing EOD OHLCV data for ^BCKY portfolios
//
//	Created by zvooz on 19-04-23.
//	Copyleft © 2019 zvooz. All rights forgone.
//

#include <cstring>
#include <errno.h>
#include <iostream>
#include <stdlib.h>
#include <string>
#include <sys/stat.h>
#include <unistd.h>
using namespace std;

/*
 *	global variables
 */
string e_dir;
string A_dir;
string B_dir;
string V_dir;
string R_dir;
string p_dir;

/*
 *	forward declarations
 */
void help(char*);
void error(const char *, const char *);
void arg_check();
void dir_check(string &);

/*
 *	main() - parse command line
 */
int main(int argc, char **argv) {
	long opt;
	while((opt = getopt(argc, argv, "he:A:B:V:R:p:")) != -1) {
		switch(opt) {
			case 'h': help(argv[0]); break;
			case 'e': e_dir = optarg; break;
			case 'A': A_dir = optarg; break;
			case 'B': B_dir = optarg; break;
			case 'V': V_dir = optarg; break;
			case 'R': R_dir = optarg; break;
			case 'p': p_dir = optarg; break;
			default: cerr << "Warning: ignore undefined argument: " << (char)opt << " " << optarg << endl; cout << "check -h for help\n"; break;
		}
	}
	
	arg_check();
	dir_check(e_dir);
	dir_check(A_dir);
	dir_check(B_dir);
	dir_check(V_dir);
	dir_check(R_dir);
	dir_check(p_dir);
	
//	cout << "directory check passed\n";
}

/*
 *	help() - print out help message
 */
void help(char * progname) {
	printf("Usage: %s [OPTIONS]\n", progname);
	printf("Check and create (if not already there) the directories for output and its record.\n");
	printf("Available options:\n");
	printf("\t-h\t\tHelp (aka what you're seeing right now).\n");
	printf("\t-e <aggregated EOD OHLCV data>\n\t\t\tThis is where you tell the program where you want to save the aggregated EOD OHLCV data, MANDATORY.\n");
	printf("\t-A <^BCKY.A EOD OHLCV data>\n\t\t\tThis is where you tell the program where you want to save ^BCKY.A's EOD OHLCV data, MANDATORY.\n");
	printf("\t-B <^BCKY.B EOD OHLCV data>\n\t\t\tThis is where you tell the program where you want to save ^BCKY.B's EOD OHLCV data, MANDATORY.\n");
	printf("\t-V <^BCKY.V EOD OHLCV data>\n\t\t\tThis is where you tell the program where you want to save ^BCKY.V's EOD OHLCV data, MANDATORY.\n");
    printf("\t-R <^RTRD EOD OHLCV data>\n\t\t\tThis is where you tell the program where you want to save ^RTRD's EOD OHLCV data, MANDATORY.\n");
	printf("\t-p <plots and charts>\n\t\t\tThis is where you tell the program where you want to save the plots and charts generated from all the data, MANDATORY.\n");
	exit(0);
}

/*
 *	error() - print out error message and then exit(1)
 */
void error(const char * errmsg1, const char * errmsg2) {
	cerr << "Error: " << errmsg1 << errmsg2 << ".\n";
	exit(1);
}

/*
 *	arg_check() - check if the arguments are properly set
 */
void arg_check() {
	bool bad = false;
	if (e_dir.empty()) {
		bad = true;
		cerr << "OHLCV directory is not set: set -h (help) for instructions\n";
	}
	if (A_dir.empty()) {
		bad = true;
		cerr << "BCKY.A directory is not set: set -h (help) for instructions\n";
	}
	if (B_dir.empty()) {
		bad = true;
		cerr << "BCKY.B directory is not set: set -h (help) for instructions\n";
	}
	if (V_dir.empty()) {
		bad = true;
		cerr << "BCKY.V directory is not set: set -h (help) for instructions\n";
	}
	if (R_dir.empty()) {
		bad = true;
		cerr << "RTRD directory is not set: set -h (help) for instructions\n";
	}
	if (p_dir.empty()) {
		bad = true;
		cerr << "plots directory is not set: set -h (help) for instructions\n";
	}
	if (bad) {
		exit(1);
	}
}

/*
 *	dir_check() - check if a directory exists, and create it if not
 */
void dir_check(string & dirpath) {
	struct stat stat_dirpath;
	if (stat(dirpath.c_str(), &stat_dirpath) != 0 || !(stat_dirpath.st_mode & S_IFDIR)) {
		cout << "creating directory " << dirpath << endl;
		if ((system(("mkdir -p \"" + dirpath + "\"").c_str()) != 0)) {
			error(("directory \"" + dirpath + "\" does not exist; unable to create the the directory: ").c_str(), strerror(errno));
		}
	}

	system(("sudo chmod 775 \"" + dirpath + "\" && sudo chown -R " + getlogin() + " \"" + dirpath + "\"").c_str());
}
