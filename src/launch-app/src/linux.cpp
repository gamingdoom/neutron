#if defined(__linux__)
#include <filesystem>
#include <thread>
#include <cstddef>
#include <exception>

#include "platform_specific.hpp"
#include "placeholders.hpp"
#include "running_guard.hpp"
#include "tray.hpp"

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

Tray::Tray *platform_specific::setup_tray(std::filesystem::path appDir, running_guard::guard &instance_guard, bool& window_state, bool &should_exit){
    Tray::Tray *tray = new Tray::Tray(APPLICATION_NAME, std::string(appDir/"browser/chrome/icons/default/default128.png"));
    tray->addEntry(Tray::SyncedToggle("Show Window", window_state, [&](bool){}));
    tray->addEntry(Tray::Button("Exit", [&]{should_exit = true;}));

    return tray;
}

#endif