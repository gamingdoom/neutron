#ifdef _WIN32
#include <filesystem>

#include "platform_specific.hpp"
#include "placeholders.hpp"

void platform_specific::move_open_in_default_browser_script(std::filesystem::path appDir){
    return;
}

void platform_specific::clean_open_in_default_browser_script(){
    return;
}

#endif