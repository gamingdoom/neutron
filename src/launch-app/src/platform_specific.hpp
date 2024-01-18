#pragma once

#include <filesystem>

namespace platform_specific {
    void move_open_in_default_browser_script(std::filesystem::path appDir);
    void clean_open_in_default_browser_script();
}
