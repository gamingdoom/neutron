#include <chrono>
#include <cstring>
#include <fstream>
#include <filesystem>
#include <memory>
#include <thread>
#include <vector>
#include <iostream>

#include <boost/dll/runtime_symbol_info.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/replace.hpp>

#ifndef __kernel_entry
    #define __kernel_entry
#endif
#include <boost/process.hpp>

#if defined(WIN32)
    #include <windows.h>
#endif

#include "platform_specific.hpp"
#include "running_guard.hpp"

std::filesystem::path executablePath(){
    return std::filesystem::path(boost::dll::program_location().string());
}

void runApp(int argc, char *argv[], std::filesystem::path appDir, running_guard::guard instance_guard){
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
            boost::process::child app((appDir/APPLICATION_NAME).string(), args);
            app.wait();

            // On close, launch headless.
            boost::process::child appHeadless((appDir/APPLICATION_NAME).string(), headlessArgs);

            instance_guard.waitForOtherProgram();
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

    // Open in default browser stuff
    if (SHOULD_OPEN_IN_DEFAULT_BROWSER){
        platform_specific::move_open_in_default_browser_script(appDir);
    }

    // policies.json editing
    std::ifstream ifs(appDir/"distribution/policies.json");
    std::string policies( (std::istreambuf_iterator<char>(ifs) ),
                       (std::istreambuf_iterator<char>()    ) );

    ifs.close();

    boost::replace_all(policies, "NEUTRON_OPEN_IN_DEFAULT_BROWSER_EXTENSION_LOCATION", (appDir/"open_in_default_browser-1.0.zip").string());

    std::ofstream out(appDir/"distribution/policies.json");
    out << policies;
    out.close();

    // Run application
    runApp(argc, argv, appDir, instance_guard);

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