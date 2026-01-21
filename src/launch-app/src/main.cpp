#include <chrono>
#include <cstdio>
#include <filesystem>
#include <thread>
#include <vector>
#include <iostream>

#include <boost/dll/runtime_symbol_info.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/replace.hpp>
#include <boost/thread.hpp>

#ifndef __kernel_entry
    #define __kernel_entry
#endif
#include <boost/process.hpp>

#if defined(WIN32)
    #include <windows.h>
#endif

#include "platform_specific.hpp"
#include "instance_restrictor.hpp"

#if defined(_WIN32)
    #define TRAY_WINAPI 1
#elif defined(__linux__)
    #define TRAY_APPINDICATOR 1
#endif

#include "tray.h"

#if TRAY_APPINDICATOR
#define TRAY_ICON1 "indicator-messages"
#define TRAY_ICON2 "indicator-messages-new"
#elif TRAY_WINAPI
#define TRAY_ICON1 "icon.ico"
#define TRAY_ICON2 "icon.ico"
#endif

typedef struct WindowStateCtx {
    tray *tray;
    bool *window_state;
    bool *should_exit;
    bool *should_run_in_background;

    Config *config;
} WindowStateCtx;

std::filesystem::path executablePath(){
    return std::filesystem::path(boost::dll::program_location().string());
}

void window_state_cb(struct tray_menu *m){
    m->checked = !m->checked;
    *((WindowStateCtx *)m->context)->window_state = m->checked;
    tray_update(((WindowStateCtx *)m->context)->tray);
}

void should_exit_cb(struct tray_menu *m){
    *((WindowStateCtx *)m->context)->should_exit = true;
}

void should_run_in_background_cb(struct tray_menu *m){
    m->checked = !m->checked;
    *((WindowStateCtx *)m->context)->should_run_in_background = m->checked;

    // Write config
    ((WindowStateCtx *)m->context)->config->run_in_background = *((WindowStateCtx *)m->context)->should_run_in_background;
    platform_specific::write_config(*((WindowStateCtx *)m->context)->config);

    tray_update(((WindowStateCtx *)m->context)->tray);
}


void runApp(int argc, char *argv[], std::filesystem::path appDir, InstanceRestrictorImpl &instance_guard, bool *is_windowed, tray *tray, bool *should_exit, Config *config){
    std::vector<std::string> args;
    std::vector<std::string> headlessArgs;

    #if defined(WIN32)
        args.push_back("-wait-for-browser");
        headlessArgs.push_back("-wait-for-browser");
    #endif

    headlessArgs.push_back("--headless");
    
    for (int i = 1; i < argc; i++){
        args.push_back(std::string(argv[i]));
        headlessArgs.push_back(std::string(argv[i]));
    }

    std::string application_executable = (appDir/APPLICATION_NAME).string();

    #if defined(_WIN32)
        application_executable += ".exe";
    #endif

    if (SHOULD_RUN_IN_BACKGROUND){
        boost::process::child app(application_executable, args);
        
        *is_windowed = true;
        bool prev_is_windowed = *is_windowed;
        while (!*should_exit) {
            // Headless -> Window
            if ((instance_guard.hasAnotherInstanceBeenLaunched() && !*is_windowed) || (!prev_is_windowed && *is_windowed)) {
                std::cout << "Headless -> Window" << std::endl;
                *is_windowed = true;
                app.terminate();
                app.wait();
                app = boost::process::child(application_executable, args);
                if (tray)
                    tray_update(tray);
            }

            // Window -> Headless
            if ((!app.running() && *is_windowed) || (prev_is_windowed && !*is_windowed)) {
                std::cout << "Window -> Headless" << std::endl;
                *is_windowed = false;
                app.terminate();
                app.wait();

                if (!config->run_in_background) {
                    break;
                }

                app = boost::process::child(application_executable, headlessArgs);
                if (tray)
                    tray_update(tray);
            }

            prev_is_windowed = *is_windowed;

            std::this_thread::sleep_for(std::chrono::milliseconds(50));
            tray_loop(0);            
		}
    } else {
        boost::process::child app(application_executable, args);
        app.wait();
    }

    return;
}

// Get the destructors to run
[[noreturn]] void signal_handler(int signal){
    exit(-1);
}

int main(int argc, char *argv[]) {
    // We need to cleanup the mutexes
    signal(SIGINT, signal_handler);
    signal(SIGABRT, signal_handler);
    signal(SIGFPE, signal_handler);
    signal(SIGILL, signal_handler);
    signal(SIGSEGV, signal_handler);
    signal(SIGTERM, signal_handler);

    #ifndef _WIN32
        std::signal(SIGKILL, signal_handler);
    #endif

    auto instance_guard = InstanceRestrictorImpl();

    if (!instance_guard.mIsFirstInstance){
        sleep(1);
        //printf("Another instance is already running.\n");
        std::cout << "Another instance is already running." << std::endl;
        return 0;
    }

    std::cout << "This instance is first." << std::endl;

    auto config = platform_specific::get_config();

    std::filesystem::path appDir = executablePath().parent_path();

    bool *window_state = nullptr;
    bool *should_exit = new bool(false);
    bool *should_run_in_background = nullptr;

    static tray tray;
    struct tray *tray_ptr = nullptr;
    std::string icon_path;
    WindowStateCtx window_state_ctx = {nullptr, window_state, should_exit, should_run_in_background, &config};
    if (SHOULD_RUN_IN_BACKGROUND){
        icon_path = platform_specific::get_icon_path(appDir);

        tray.icon = const_cast<char*>(icon_path.c_str());
        static struct tray_menu tray_menu[] = {
            {.text = "Show Window", .disabled = 0, .checked = 1, .cb = window_state_cb, .context = &window_state_ctx, .submenu = NULL},
            {.text = "-", .disabled = 0, .checked = 0, .cb = NULL, .context = NULL, .submenu = NULL},
            {.text = "Run in Background (uses more resources)", .disabled = 0, .checked = 1, .cb = should_run_in_background_cb, .context = &window_state_ctx, .submenu = NULL},
            {.text = "Exit", .disabled = 0, .checked = 0, .cb = should_exit_cb, .context = &window_state_ctx, .submenu = NULL},
            {.text = "-", .disabled = 0, .checked = 0, .cb = NULL, .context = NULL, .submenu = NULL},
            {.text = NULL, .disabled = 0, .checked = 0, .cb = NULL, .context = NULL, .submenu = NULL},
        };
        tray.menu = tray_menu;
        
        tray_ptr = &tray;

        window_state = (bool*)&tray.menu[0].checked;
        should_run_in_background = (bool*)&tray.menu[2].checked;

        window_state_ctx.tray = tray_ptr;
        window_state_ctx.window_state = window_state;
        window_state_ctx.should_run_in_background = should_run_in_background;

        if (tray_init(tray_ptr) < 0){
            std::cout << "Failed to initialize tray" << std::endl;
            return 1;
        }

        *should_run_in_background = config.run_in_background;
        tray_update(tray_ptr);

    } else {
        window_state = new bool(true);
        should_run_in_background = new bool(false);
    }

    // Open in default browser stuff
    if (SHOULD_OPEN_IN_DEFAULT_BROWSER){
        platform_specific::move_open_in_default_browser_script(appDir);
    }

    // Run application
    runApp(argc, argv, appDir, instance_guard, window_state, tray_ptr, should_exit, &config);

    return 0;
}

#if defined(_WIN32)
int WinMain(HINSTANCE hInstance,
            HINSTANCE hPrevInstance, 
            LPTSTR    lpCmdLine, 
            int       cmdShow)
    {
        return main(__argc, __argv);
    }
#endif