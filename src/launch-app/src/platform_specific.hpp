#pragma once

#include "running_guard.hpp"
#include "tray.hpp"

#include <filesystem>

namespace platform_specific {
    void move_open_in_default_browser_script(std::filesystem::path appDir);
    void clean_open_in_default_browser_script();
    Tray::Tray *setup_tray(std::filesystem::path appDir, running_guard::guard &instance_guard, bool &window_state, bool &should_exit);
}
