CPLEX_DIR = /opt/ibm/ILOG/CPLEX_Studio1210/cplex
CONCERT_DIR = /opt/ibm/ILOG/CPLEX_Studio1210/concert

CXX = g++
CXXFLAGS += -g -DIL_STD -Wall -I$(CPLEX_DIR)/include -I$(CONCERT_DIR)/include
LDFLAGS += -L$(CPLEX_DIR)/lib/x86-64_linux/static_pic -L$(CONCERT_DIR)/lib/x86-64_linux/static_pic -L/opt/ibm/ILOG/CPLEX_Studio129/lib/x86-64_linux/static_pic -Wl,--no-as-needed
LDLIBS += -ldl -lilocplex -lconcert -lcplex -lm -lpthread


clean:
	$(RM) *~ *.o main

.PHONY: all clean
