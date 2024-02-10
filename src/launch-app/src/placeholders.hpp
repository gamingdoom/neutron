#pragma once

// This file fixes the placeholders that should be defined when compiling so the IDE shuts up

#ifndef SHOULD_RUN_IN_BACKGROUND
    #define SHOULD_RUN_IN_BACKGROUND true
#endif

#ifndef APPLICATION_NAME
    #define APPLICATION_NAME "neutronapp"
#endif

#ifndef SHOULD_OPEN_IN_DEFAULT_BROWSER
    #define SHOULD_OPEN_IN_DEFAULT_BROWSER true
#endif