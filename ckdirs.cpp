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
//string [] dirs;

/*
 *	forward declarations
 */
void help(char*);
void error(const char *, const char *);
void dir_check(string);

/*
 *	main() - parse command line
 */
int main(int argc, char **argv) {
	long opt;
	while((opt = getopt(argc, argv, "-h")) != -1) {
		switch(opt) {
			case 'h': help(argv[0]); break;
			default: cerr << "Warning: ignore undefined argument: " << (char)opt << " " << optarg << endl; cout << "check -h for help\n"; break;
		}
	}
	
	for (int i = optind; i < argc; i++) {
		dir_check(argv[i]);
	}
}

/*
 *	help() - print out help message
 */
void help(char * progname) {
	printf("Usage: %s [OPTIONS]\n", progname);
	printf("Check and create (if not already there) the directories for output and its record.\n");
	printf("Available options:\n");
	printf("\t-h\t\tHelp (aka what you're seeing right now).\n");
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
 *	dir_check() - check if a directory exists, and create it if not
 */
void dir_check(string dirpath) {
	struct stat stat_dirpath;
	if (stat(dirpath.c_str(), &stat_dirpath) != 0 || !(stat_dirpath.st_mode & S_IFDIR)) {
		cout << "creating directory " << dirpath << endl;
		if ((system(("mkdir -p \'" + dirpath + "\'").c_str()) != 0)) {
			error(("directory \"" + dirpath + "\" does not exist; unable to create the the directory: ").c_str(), strerror(errno));
		}
	}
	system(("chmod 755 \"" + dirpath + "\" && chown -R " + getlogin() + " \"" + dirpath + "\"").c_str());
}
