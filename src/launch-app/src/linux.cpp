#if defined(__linux__)
#include <filesystem>
#include <iostream>
#include <string>
#include <fstream>

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

std::string platform_specific::get_icon_path(std::filesystem::path appDir) {
    return std::string(appDir/"browser/chrome/icons/default/default128.png");
}

Config platform_specific::get_config(){
    // Get config path ${HOME}/.APPLICATION_NAME/config.txt
    std::filesystem::path configPath = std::filesystem::path(std::getenv("HOME")) / "." APPLICATION_NAME / "config.txt";
    
    // create it if it doesn't exist
    if (!std::filesystem::exists(configPath)) {
        std::filesystem::create_directories(configPath.parent_path());

        std::ofstream configFile(configPath);
        configFile << "run_in_background=";

        if (SHOULD_RUN_IN_BACKGROUND) {
            configFile << "true";
        } else {
            configFile << "false";
        }

        configFile << std::endl;

        configFile.close();
    }

    // Parse it
    try {
        std::ifstream configFile(configPath);
        std::string line;
        while (std::getline(configFile, line)) {
            if (line.find("run_in_background") != std::string::npos) {
                if (line.find("true") != std::string::npos) {
                    return Config{true};
                } else if (line.find("false") != std::string::npos) {
                    return Config{false};
                }
            }
        }
    } catch (std::exception &e) {
        std::cerr << "Failed to parse config file: " << e.what() << std::endl;
        throw e;
    }

    throw std::runtime_error("Failed to parse config file!");
}

void platform_specific::write_config(Config config) {
    // Get config path ${HOME}/.APPLICATION_NAME/config.txt
    std::filesystem::path configPath = std::filesystem::path(std::getenv("HOME")) / "." APPLICATION_NAME / "config.txt";
    
    std::ofstream configFile(configPath, std::ios::out | std::ios::trunc);
    configFile << "run_in_background=";

    if (config.run_in_background) {
        configFile << "true";
    } else {
        configFile << "false";
    }

    configFile << std::endl;

    configFile.close();
}

#endif