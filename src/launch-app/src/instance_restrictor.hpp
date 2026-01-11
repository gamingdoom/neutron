#pragma once

#include <filesystem>
#include <thread>

class InstanceRestrictor {
    public:
        bool mIsFirstInstance;

        // Must be first instance to call this
        virtual bool hasAnotherInstanceBeenLaunched() = 0;
};

class InstanceRestrictorImpl : public InstanceRestrictor {
    public:
        InstanceRestrictorImpl();
        ~InstanceRestrictorImpl();

        virtual bool hasAnotherInstanceBeenLaunched() override;

        bool mIsFirstInstance = false;
    
    private:
        void updateTimestamp();

        bool checkIfFirstInstance();

        std::filesystem::path mPath;
        std::thread mUpdateThread;

        bool mOtherInstanceLaunched = false;

        bool mIsExiting = false;

        typedef struct LockData{
            uint64_t t1;
            uint64_t t2;
            uint64_t null_terminator = '\0';
        } LockData;
};