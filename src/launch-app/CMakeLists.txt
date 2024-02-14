# A few variables need to be set with -D... at configure:
# APPLICATION_NAME: string
# SHOULD_OPEN_IN_DEFAULT_BROWSER: true or false
# SHOULD_RUN_IN_BACKGROUND: true or false
# RES_PATH (only if Windows): path/to/app.res

cmake_minimum_required(VERSION 3.27.4)
project(launch-app)

file(GLOB_RECURSE sources      src/*.cpp src/*.hpp)

set( BOOST_INCLUDE_LIBRARIES dll interprocess process algorithm )

if (NOT ${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
  add_subdirectory(extern/boost/ EXCLUDE_FROM_ALL)
  add_subdirectory(extern/traypp EXCLUDE_FROM_ALL)
endif()

add_executable(launch-app ${sources} ${Boost_INCLUDE_DIRS} ${RES_PATH})

target_compile_options(launch-app PRIVATE -std=c++17 -Wall -Wextra -Wno-deprecated-declarations -Wno-unused-parameter -g)

target_compile_definitions(launch-app PRIVATE APPLICATION_NAME=${APPLICATION_NAME} SHOULD_OPEN_IN_DEFAULT_BROWSER=${SHOULD_OPEN_IN_DEFAULT_BROWSER} SHOULD_RUN_IN_BACKGROUND=${SHOULD_RUN_IN_BACKGROUND})

if (NOT ${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
  target_link_libraries(launch-app PRIVATE
    $<$<BOOL:${WIN32}>:ws2_32>
    Boost::headers Boost::interprocess Boost::dll Boost::process Boost::algorithm
    tray
  )
else()
  target_link_libraries(launch-app PRIVATE
    ${MY_BOOST_LIB_PATHS}  
  )
  target_include_directories(launch-app PRIVATE
    ${MY_BOOST_INCLUDE_DIRS}
  )
endif()
