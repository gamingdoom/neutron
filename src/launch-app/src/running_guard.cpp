#include <boost/interprocess/creation_tags.hpp>
#include <boost/interprocess/exceptions.hpp>
#include <string>

#include <boost/interprocess/sync/named_semaphore.hpp>

#include "running_guard.hpp"

namespace running_guard {
    guard::guard(std::string name) : name(name){
        try {
            guard::semaphore = new boost::interprocess::named_semaphore(boost::interprocess::create_only_t(), name.c_str(), 0);
            guard::otherProgramExists = false;
        } catch (boost::interprocess::interprocess_exception &e){
            guard::semaphore = new boost::interprocess::named_semaphore(boost::interprocess::open_only_t(), name.c_str());
            guard::otherProgramExists = true;
        }
        //mutex.try_lock();
        if (otherProgramExists){
            guard::semaphore->post();
        }
    }

    guard::~guard() {
        if (!otherProgramExists || guard::semaphore->try_wait())
            boost::interprocess::named_semaphore::remove(guard::name.c_str());
    }

    void guard::waitForOtherProgram(){
        guard::semaphore->wait();
        return;
    }
}