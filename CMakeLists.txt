cmake_minimum_required(VERSION 3.10)
project(RobborCP Firmware)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(robbor_cp firmware/src/main.cpp)
