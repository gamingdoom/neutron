#include <chrono>
#include <cstdio>
#include <cstring>
#include <exception>
#include <fstream>
#include <filesystem>
#include <future>
#include <memory>
#include <ratio>
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
#include "placeholders.hpp"

std::filesystem::path executablePath(){
    return std::filesystem::path(boost::dll::program_location().string());
}

void runApp(int argc, char *argv[], std::filesystem::path appDir, InstanceRestrictorImpl &instance_guard, bool &is_windowed, Tray::Tray *tray, bool &should_exit){
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
        
        is_windowed = true;
        bool prev_is_windowed = is_windowed;
        while (!should_exit) {
            // Headless -> Window
            if ((instance_guard.hasAnotherInstanceBeenLaunched() && !is_windowed) || (!prev_is_windowed && is_windowed)) {
                printf("Going to window!\n");
                is_windowed = true;
                app.terminate();
                app.wait();
                app = boost::process::child(application_executable, args);
                if (tray)
                    tray->update();
            }

            // Window -> Headless
            if ((!app.running() && is_windowed) || (prev_is_windowed && !is_windowed)) {
                printf("Going to headless!\n");
                is_windowed = false;
                app.terminate();
                app.wait();
                app = boost::process::child(application_executable, headlessArgs);

                if (tray)
                    tray->update();
            }

            prev_is_windowed = is_windowed;

            std::this_thread::sleep_for(std::chrono::milliseconds(100));            
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
        return 0;
    }

    std::filesystem::path appDir = executablePath().parent_path();

    bool window_state = true;
    bool should_exit = false;

    Tray::Tray *tray = nullptr;
    if (SHOULD_RUN_IN_BACKGROUND){
        tray = platform_specific::setup_tray(appDir, instance_guard, window_state, should_exit);
    }

    // Open in default browser stuff
    if (SHOULD_OPEN_IN_DEFAULT_BROWSER){
        platform_specific::move_open_in_default_browser_script(appDir);
    }

    // Run application
    runApp(argc, argv, appDir, instance_guard, window_state, tray, should_exit);

    if (tray){
        tray->exit();
    }

    return 0;
}

#if defined(WIN32)
int WinMain(HINSTANCE hInstance,
            HINSTANCE hPrevInstance, 
            LPTSTR    lpCmdLine, 
            int       cmdShow)
    {
        return main(__argc, __argv);
    }
#endif