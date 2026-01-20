#include <chrono>
#include <filesystem>
#include <iostream>
#include <fstream>
#include <thread>

#include "instance_restrictor.hpp"

#include <boost/dll/runtime_symbol_info.hpp>

#define TIMEOUT_SECONDS 3

// Implementation.
// We will have a file stored next to the executable.
// It will have 2 64-bit numbers of unix timestamps.
// If the first timestamp is more than 2 seconds out of date, we assume we are the first instance.
// If it isn't, we update the second timestamp. 
// The first instance will then use this updated timestamp to know if another instance has been launched.

InstanceRestrictorImpl::InstanceRestrictorImpl()
{
    mPath = std::filesystem::temp_directory_path()/(APPLICATION_NAME"_instance_lock.bin");

    // Create and initialize file if it doesn't exist
    if (!std::filesystem::exists(mPath)){
        std::ofstream file(mPath, std::ios::out | std::ios::binary);
        LockData zero = {0, 0};
        file.write(reinterpret_cast<char *>(&zero),  sizeof(LockData));
        file.close();
    }

    mIsFirstInstance = checkIfFirstInstance();

    mUpdateThread = std::thread(&InstanceRestrictorImpl::updateTimestamp, this);
}

InstanceRestrictorImpl::~InstanceRestrictorImpl() {
    mIsExiting = true;
    mUpdateThread.join();

    std::ofstream file(mPath, std::ios::out | std::ios::binary);
    LockData zero = {0, 0};
    file.write(reinterpret_cast<char *>(&zero),  sizeof(LockData));
    file.close();
}

bool InstanceRestrictorImpl::hasAnotherInstanceBeenLaunched() {
    assert(mIsFirstInstance);
    
    if (mOtherInstanceLaunched) {
        mOtherInstanceLaunched = false;
        return true;
    }

    return false;
}

void InstanceRestrictorImpl::updateTimestamp() {
    do {
        if (mIsFirstInstance) {
            LockData lockData{};

            std::ifstream ifile(mPath, std::ios::in | std::ios::binary);
            ifile.read(reinterpret_cast<char *>(&lockData), sizeof(LockData));
            ifile.close();

            lockData.t1 = std::chrono::system_clock::now().time_since_epoch().count() / 1e9;

            if (lockData.t1 - lockData.t2 < 2) {
                mOtherInstanceLaunched = true;
            }

            std::ofstream ofile(mPath, std::ios::out | std::ios::binary);
            ofile.write(reinterpret_cast<char *>(&lockData), sizeof(LockData));
            ofile.close();
        } else {
            LockData lockData{};

            std::ifstream ifile(mPath, std::ios::in | std::ios::binary);
            ifile.read(reinterpret_cast<char *>(&lockData), sizeof(LockData));
            ifile.close();

            lockData.t2 = std::chrono::system_clock::now().time_since_epoch().count() / 1e9;

            std::ofstream ofile(mPath, std::ios::out | std::ios::binary);
            ofile.write(reinterpret_cast<char *>(&lockData), sizeof(LockData));
            ofile.close();

            break;
        }

        std::this_thread::sleep_for(std::chrono::seconds(1));
    } while (!mIsExiting);
}

bool InstanceRestrictorImpl::checkIfFirstInstance() {
    LockData lockData{};

    std::ifstream ifile(mPath, std::ios::in | std::ios::binary);
    ifile.read(reinterpret_cast<char *>(&lockData), sizeof(LockData));
    ifile.close();

    if ((std::chrono::system_clock::now().time_since_epoch().count() / 1e9) - lockData.t1 > TIMEOUT_SECONDS){
        lockData.t2 = 0;

        std::ofstream ofile(mPath, std::ios::out | std::ios::binary);
        ofile.write(reinterpret_cast<char *>(&lockData), sizeof(LockData));
        ofile.close();

        return true;
    }

    return false;
}