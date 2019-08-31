# Files to compile that do have a main() function
TARGETS = ckdirs

# Let the programmer choose 32 or 64 bits
BITS ?= 64

# Directory names
ODIR := ./bin$(BITS)
output_folder := $(shell mkdir -p $(ODIR))

# Names of files that the compiler generates
EXEFILES  = $(patsubst %, $(ODIR)/%, $(TARGETS))

# Compilers (clang++ normally has faster runtime)
GCC = g++
CLANG = clang++
CXX = $(GCC)

# General flags
CXXFLAGS = -march=native -Ofast -D_GLIBCXX_PARALLEL

# Compiler-specific flags
GCCFLAGS = -frename-registers
AOCCFLAGS = -fstruct-layout=5 -enable-partial-unswitch -enable-redundant-movs

# PGO flags
PGOGEN = -fprofile-generate
PGOUSE = -fprofile-use -fprofile-correction

# Clang PGO instrumented profiler flags http://clang.llvm.org/docs/UsersManual.html#profile-guided-optimization
PGOGEN_ISTR = -fprofile-instr-generate
PGOUSE_ISTR = -fprofile-instr-use

# Clang PGO sampling profiler flags http://clang.llvm.org/docs/UsersManual.html#profile-guided-optimization
PGOGEN_SMPL = -g
PGOUSE_SMPL = -fprofile-sample-use

# OpenMP flags
OMP = -fopenmp

# Best to be safe...
.DEFAULT_GOAL = all
.PRECIOUS: $(EXEOFILES)
.PHONY: all clean

# Goal is to build all executables
all: $(EXEFILES)

# Rules for building executables
$(ODIR)/%: %.cpp
	echo "[CXX] $< --> $@"
	$(CXX) $^ -o $@ $(CXXFLAGS) $(GCCFLAGS)

# clean by clobbering the build folder
clean:
	@echo Cleaning up...
	rm -rf $(ODIR)
