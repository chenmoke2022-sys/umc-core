cmake_minimum_required(VERSION 3.16)
project(system_perf_microbench CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(mem_bw src/mem_bw.cpp)


