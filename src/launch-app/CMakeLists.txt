cmake_minimum_required(VERSION 3.27.4)
project(launch-app)

file(GLOB_RECURSE sources      src/*.cpp src/*.hpp)

set( BOOST_INCLUDE_LIBRARIES dll interprocess process algorithm )
add_subdirectory( extern/boost/ EXCLUDE_FROM_ALL )

add_executable(launch-app ${sources} ${Boost_INCLUDE_DIRS})

# just for example add some compiler flags
target_compile_options(launch-app PRIVATE -std=c++17 -Wall -Wextra -Wpedantic -Wno-deprecated-declarations -Wno-unused-parameter -Werror -g)

target_compile_definitions(launch-app PRIVATE APPLICATION_NAME=${APPLICATION_NAME} SHOULD_OPEN_IN_DEFAULT_BROWSER=${SHOULD_OPEN_IN_DEFAULT_BROWSER} SHOULD_RUN_IN_BACKGROUND=${SHOULD_RUN_IN_BACKGROUND})

target_link_libraries(launch-app PRIVATE
  $<$<BOOL:${WIN32}>:ws2_32>
  Boost::headers Boost::interprocess Boost::dll Boost::process Boost::algorithm
)