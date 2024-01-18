cmake_minimum_required(VERSION 3.0)
project(launch-app)

file(GLOB_RECURSE sources      src/*.cpp src/*.hpp)

add_executable(launch-app ${sources} ${data})

# just for example add some compiler flags
target_compile_options(launch-app PUBLIC -std=c++17 -Wall -Wextra -Wpedantic -Wno-deprecated-declarations -Wno-unused-parameter -Werror -g)

target_compile_definitions(launch-app PUBLIC APPLICATION_NAME=${APPLICATION_NAME} SHOULD_OPEN_IN_DEFAULT_BROWSER=${SHOULD_OPEN_IN_DEFAULT_BROWSER} SHOULD_RUN_IN_BACKGROUND=${SHOULD_RUN_IN_BACKGROUND})

find_package(Boost COMPONENTS filesystem system REQUIRED)

target_link_libraries(launch-app PUBLIC
  ${Boost_LIBRARIES}
)