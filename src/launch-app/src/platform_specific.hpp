#pragma once

#include <filesystem>

typedef struct Config {
    bool run_in_background;
} Config;

namespace platform_specific {
    void move_open_in_default_browser_script(std::filesystem::path appDir);
    void clean_open_in_default_browser_script();
    std::string get_icon_path(std::filesystem::path appDir);
    Config get_config();
    void write_config(Config config);
}
