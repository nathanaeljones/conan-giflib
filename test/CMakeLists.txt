PROJECT(MyHello)
cmake_minimum_required(VERSION 2.8)

include(conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

ADD_EXECUTABLE(gifcolor gifcolor.c qprintf.c)
include_directories(${CONAN_INCLUDE_DIRS})
TARGET_LINK_LIBRARIES(gifcolor ${CONAN_LIBS})