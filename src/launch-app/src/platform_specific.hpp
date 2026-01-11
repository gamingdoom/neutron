#pragma once

#include "instance_restrictor.hpp"
#if defined(__APPLE__)
#include "tray_mac.hpp"
#else
#include "tray.hpp"
#endif

#include <filesystem>

namespace platform_specific {
    void move_open_in_default_browser_script(std::filesystem::path appDir);
    void clean_open_in_default_browser_script();
    Tray::Tray *setup_tray(std::filesystem::path appDir, InstanceRestrictorImpl &instance_guard, bool &window_state, bool &should_exit);
}
