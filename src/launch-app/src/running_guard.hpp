#pragma once
#include <string>
#include <memory>

#include <boost/interprocess/sync/named_semaphore.hpp>
#include <boost/interprocess/creation_tags.hpp>


namespace running_guard
{
    class guard
    {
      public:
        std::string name;
        bool otherProgramExists;
      
      private:
        boost::interprocess::named_semaphore *semaphore;

      public:
        ~guard();
        explicit guard(std::string name);

      public:
        void waitForOtherProgram();
    };
}