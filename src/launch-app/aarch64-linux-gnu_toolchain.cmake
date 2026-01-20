set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)

set(CMAKE_SYSROOT $ENV{MOZBUILD}/sysroot-$ENV{TARGET})

# Cross compilers
set(CMAKE_C_COMPILER   /usr/bin/clang)
set(CMAKE_CXX_COMPILER /usr/bin/clang++)
set(CMAKE_ASM_COMPILER /usr/bin/$ENV{TARGET}-gcc)

set(CMAKE_C_FLAGS   "--target=$ENV{TARGET} --gcc-toolchain=${CMAKE_SYSROOT}/usr" CACHE STRING "" FORCE)
set(CMAKE_CXX_FLAGS "-fpermissive --target=$ENV{TARGET} --gcc-toolchain=${CMAKE_SYSROOT}/usr" CACHE STRING "" FORCE)
set(CMAKE_SHARED_LINKER_FLAGS "--target=$ENV{TARGET} --gcc-toolchain=${CMAKE_SYSROOT}/usr" CACHE STRING "" FORCE)
set(CMAKE_LINKER_TYPE LLD CACHE STRING "" FORCE)