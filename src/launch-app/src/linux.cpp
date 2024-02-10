#ifdef __linux__
#include <filesystem>

#include "platform_specific.hpp"
#include "placeholders.hpp"

#define OPEN_IN_DEFAULT_BROWSER_PATH "/tmp/open-in-default-browser"

void platform_specific::move_open_in_default_browser_script(std::filesystem::path appDir){
    try {
        std::filesystem::copy_file(appDir/"open-in-default-browser", OPEN_IN_DEFAULT_BROWSER_PATH);
    } catch (const std::filesystem::filesystem_error &e){
        // File exists, its ok
    }
    return;
}

void platform_specific::clean_open_in_default_browser_script(){
    std::filesystem::remove(OPEN_IN_DEFAULT_BROWSER_PATH);
    return;
}

#endif