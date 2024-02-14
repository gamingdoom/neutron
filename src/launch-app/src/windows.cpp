#ifdef _WIN32
#include <filesystem>

#include "platform_specific.hpp"
#include "placeholders.hpp"
#include "running_guard.hpp"
#include "tray.hpp"


void platform_specific::move_open_in_default_browser_script(std::filesystem::path appDir){
    return;
}

void platform_specific::clean_open_in_default_browser_script(){
    return;
}

Tray::Tray *platform_specific::setup_tray(std::filesystem::path appDir, running_guard::guard &instance_guard, bool& window_state, bool &should_exit){
    Tray::Tray *tray = new Tray::Tray(APPLICATION_NAME, std::string(appDir/APPLICATION_NAME ".ico"));
    tray->addEntry(Tray::SyncedToggle("Show Window", window_state, NULL));
    tray->addEntry(Tray::Button("Exit", [&]{should_exit = true;}));

    return tray;
}

#endif