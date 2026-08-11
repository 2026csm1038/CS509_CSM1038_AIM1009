CXX = g++
CXXFLAGS = -O2 -std=c++17

COMMON = assignment_01/src/csr.cpp
A1_SRC = assignment_01/src
A1_DRIVER = assignment_01/driver

A2_SRC = assignment_02/src
A2_DRIVER = assignment_02/driver

.PHONY: all assignment1 assignment2 wrapper clean

all: assignment1 assignment2 wrapper

assignment1: bfs_driver dfs_driver sssp_driver

assignment2: bc_driver connected_components_driver triangle_counting_driver

bfs_driver:
	$(CXX) $(CXXFLAGS) \
		$(A1_DRIVER)/bfs_driver.cpp \
		$(A1_SRC)/bfs.cpp \
		$(COMMON) \
		-o bfs_driver

dfs_driver:
	$(CXX) $(CXXFLAGS) \
		$(A1_DRIVER)/dfs_driver.cpp \
		$(A1_SRC)/dfs.cpp \
		$(COMMON) \
		-o dfs_driver

sssp_driver:
	$(CXX) $(CXXFLAGS) \
		$(A1_DRIVER)/sssp_driver.cpp \
		$(A1_SRC)/sssp.cpp \
		$(COMMON) \
		-o sssp_driver

bc_driver:
	$(CXX) $(CXXFLAGS) \
		$(A2_DRIVER)/bc_driver.cpp \
		$(A2_SRC)/betweenness_centrality.cpp \
		$(COMMON) \
		-I$(A2_SRC) \
		-o bc_driver

connected_components_driver:
	$(CXX) $(CXXFLAGS) \
		$(A2_DRIVER)/connected_components_driver.cpp \
		$(A2_SRC)/connected_components.cpp \
		$(A1_SRC)/bfs.cpp \
		$(COMMON) \
		-I$(A2_SRC) \
		-o connected_components_driver

triangle_counting_driver:
	$(CXX) $(CXXFLAGS) \
		$(A2_DRIVER)/triangle_counting_driver.cpp \
		$(A2_SRC)/triangle_counting.cpp \
		$(COMMON) \
		-I$(A2_SRC) \
		-o triangle_counting_driver

wrapper:
	$(CXX) $(CXXFLAGS) \
		common_wrapper/wrapper.cpp \
		-o wrapper

clean:
	rm -f bfs_driver
	rm -f dfs_driver
	rm -f sssp_driver
	rm -f bc_driver
	rm -f connected_components_driver
	rm -f triangle_counting_driver
	rm -f wrapper
