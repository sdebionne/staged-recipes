cmake_minimum_required(VERSION 3.10)
project(zstd_hdf5)

find_path(ZSTD_INCLUDE_DIR "zstd.h")
find_library(ZSTD_LIBRARY NAMES zstd)

message("ZSTD lib: ${ZSTD_LIBRARY}")
message("ZSTD include: ${ZSTD_INCLUDE_DIRS}")

set(PLUGIN_INSTALL_PATH "${CMAKE_INSTALL_PREFIX}/lib/hdf5/plugin" CACHE PATH
      "Where to install the dynamic HDF5-plugin")

# sources
set(SOURCES zstd_h5plugin.c)
set(PLUGIN_SOURCES zstd_h5plugin.c)

# dependencies
if(MSVC)
    # FindHDF5.cmake does not find Windows installations. Try to
    # use an environment variable instead until the official "find"
    # file can be updated for Windows.
    #
    # Note that you have to set this environment variable by hand.
    file(TO_CMAKE_PATH "$ENV{HDF5_DIR}" HDF5_HINT)
    set(HDF5_DIR ${HDF5_HINT} CACHE STRING "Path to HDF5 CMake config directory.")
    find_package(HDF5 REQUIRED HINTS ${HDF5_DIR})
else(MSVC)
    find_package(HDF5 REQUIRED)
endif(MSVC)
include_directories(${HDF5_INCLUDE_DIRS})

# add ZSTD libraries
add_library(zstd SHARED IMPORTED)
set_target_properties(zstd PROPERTIES
    IMPORTED_LINK_INTERFACE_LANGUAGES "C"
    IMPORTED_LOCATION "${ZSTD_LIBRARY}")

add_library(zstd_h5_plugin_shared SHARED ${PLUGIN_SOURCES})
set_target_properties(zstd_h5_plugin_shared PROPERTIES OUTPUT_NAME H5Zzstd)
target_link_libraries(zstd_h5_plugin_shared zstd hdf5::hdf5)

#install
install(TARGETS zstd_h5_plugin_shared DESTINATION ${PLUGIN_INSTALL_PATH} COMPONENT HDF5_FILTER_DEV)
