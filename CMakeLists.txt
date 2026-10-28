cmake_minimum_required(VERSION 3.10)
project(RobborCP_Firmware)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Firmware target (host-side simulation / unit-test build)
add_executable(robbor_cp firmware/src/main.cpp)

# Optional: install target
install(TARGETS robbor_cp DESTINATION bin)
