# A few variables need to be set with -D... at configure:
# APPLICATION_NAME: string
# SHOULD_OPEN_IN_DEFAULT_BROWSER: true or false
# SHOULD_RUN_IN_BACKGROUND: true or false
# RES_PATH (only if Windows): path/to/app.res

cmake_minimum_required(VERSION 3.27.4)
project(launch-app)

set (CMAKE_CXX_STANDARD 20)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_${lang}_COMPILE_OPTIONS_SYSROOT "--sysroot=")

file(GLOB_RECURSE sources      src/*.cpp src/*.hpp src/*.h)

set( BOOST_INCLUDE_LIBRARIES dll interprocess process algorithm thread )

if (NOT ${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
  add_subdirectory(extern/boost EXCLUDE_FROM_ALL)
endif()

add_executable(launch-app ${sources} ${Boost_INCLUDE_DIRS} ${RES_PATH})

target_compile_options(launch-app PRIVATE -std=c++17 -Wall -Wextra -Wno-deprecated-declarations -Wno-unused-parameter)
target_compile_definitions(launch-app PRIVATE APPLICATION_NAME=${APPLICATION_NAME} SHOULD_OPEN_IN_DEFAULT_BROWSER=${SHOULD_OPEN_IN_DEFAULT_BROWSER} SHOULD_RUN_IN_BACKGROUND=${SHOULD_RUN_IN_BACKGROUND})

if (NOT ${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
  if (${LINUX})
    find_package(PkgConfig REQUIRED)
    pkg_check_modules(APPINDICATOR REQUIRED appindicator3-0.1)
    
    target_include_directories(launch-app PRIVATE ${APPINDICATOR_INCLUDE_DIRS})
  endif()

  target_link_libraries(launch-app PRIVATE
    $<$<BOOL:${WIN32}>:ws2_32>
    Boost::headers Boost::interprocess Boost::dll Boost::process Boost::algorithm
    $<$<BOOL:${LINUX}>:dl ${APPINDICATOR_LIBRARIES}>
  )
else()
  target_link_libraries(launch-app PRIVATE
    ${BOOST_SYSTEM_LIB}
    ${BOOST_THREAD_LIB}
  )
  target_include_directories(launch-app PRIVATE
    ${MY_BOOST_INCLUDE_DIRS}
  )
endif()
