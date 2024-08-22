# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_nbt_bot_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED nbt_bot_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(nbt_bot_FOUND FALSE)
  elseif(NOT nbt_bot_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(nbt_bot_FOUND FALSE)
  endif()
  return()
endif()
set(_nbt_bot_CONFIG_INCLUDED TRUE)

# output package information
if(NOT nbt_bot_FIND_QUIETLY)
  message(STATUS "Found nbt_bot: 0.0.0 (${nbt_bot_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'nbt_bot' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${nbt_bot_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(nbt_bot_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${nbt_bot_DIR}/${_extra}")
endforeach()
