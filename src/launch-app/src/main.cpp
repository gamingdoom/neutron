#include <chrono>
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
#include "running_guard.hpp"
#include "placeholders.hpp"

std::filesystem::path executablePath(){
    return std::filesystem::path(boost::dll::program_location().string());
}

void runApp(int argc, char *argv[], std::filesystem::path appDir, running_guard::guard &instance_guard, bool &window_state, Tray::Tray *tray, bool &should_exit){
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

    if (SHOULD_RUN_IN_BACKGROUND){
        while (true){
            if (should_exit)
                return;

            boost::process::child app((appDir/APPLICATION_NAME).string(), args);
            window_state = true;
            if (tray)
                tray->update();
            while (true){

                if (should_exit){
                    app.terminate();
                    return;
                }

                if (window_state){
                    if (app.wait_for(std::chrono::milliseconds(100))){
                        window_state = false;
                        if (tray)
                            tray->update();
                        printf("App Closed!\n");
                        break;
                    }
                } else {
                    printf("Stopping App\n");
                    app.terminate();
                    break;
                }
            }

            // On close, launch headless.
            window_state = false;
            if (tray)
                tray->update();

            boost::process::child appHeadless((appDir/APPLICATION_NAME).string(), headlessArgs);
            
            printf("Started headless\n");

            bool waiter_exited = false;

            auto waiter = new boost::thread([&]{
                instance_guard.waitForOtherProgram();
                waiter_exited = true;
            });

            while (true){
                if (should_exit){
                    appHeadless.terminate();
                    return;
                }
                if (waiter_exited){
                    break;
                }
                if (window_state){
                    break;
                }
                std::this_thread::sleep_for(std::chrono::milliseconds(50));
            }
            
            try {
                delete waiter;
            } catch (std::exception &e){
                std::cout << e.what();
            }

            appHeadless.terminate();
        }
    } else {
        boost::process::child app((appDir/APPLICATION_NAME).string(), args);
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

    auto instance_guard = running_guard::guard(APPLICATION_NAME);

    if (instance_guard.otherProgramExists){
        sleep(1);
        return 0;
    }

    std::filesystem::path appDir = executablePath().parent_path();

    bool window_state = true;
    bool should_exit = false;

    // Tray
    Tray::Tray *tray = nullptr;
    std::thread *tray_runner;
    if (SHOULD_RUN_IN_BACKGROUND){
        tray = platform_specific::setup_tray(appDir, instance_guard, window_state, should_exit);
        tray_runner = new std::thread([&]{tray->run();});
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