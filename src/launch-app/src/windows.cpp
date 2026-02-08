#ifdef _WIN32

#define WINVER 0x0600
#define _WIN32_WINNT 0x0600
#define NTDDI_VERSION 0x06000000
#include <windows.h>
#include <shlobj.h>

#include <filesystem>
#include <string>
#include <fstream>
#include <iostream>

#include "platform_specific.hpp"
#include "placeholders.hpp"

void platform_specific::move_open_in_default_browser_script(std::filesystem::path appDir){
    return;
}

void platform_specific::clean_open_in_default_browser_script(){
    return;
}

std::string platform_specific::get_icon_path(std::filesystem::path appDir) {
    return (appDir / (std::string(APPLICATION_NAME) + ".ico")).string();
}

Config platform_specific::get_config(){
    // Get config path at appdata/roaming/APPLICATION_NAME/config.txt
    PWSTR path = nullptr;
    SHGetKnownFolderPath(FOLDERID_RoamingAppData, 0, nullptr, &path);
    std::filesystem::path configPath = std::filesystem::path(path) / APPLICATION_NAME / "config.txt";
    CoTaskMemFree(path);
    
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
    // Get config path at appdata/roaming/APPLICATION_NAME/config.txt
    PWSTR path = nullptr;
    SHGetKnownFolderPath(FOLDERID_RoamingAppData, 0, nullptr, &path);
    std::filesystem::path configPath = std::filesystem::path(path) / APPLICATION_NAME / "config.txt";
    CoTaskMemFree(path);
    
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