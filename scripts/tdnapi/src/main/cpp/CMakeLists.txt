# the minimum version of CMake.
cmake_minimum_required(VERSION 3.5.0 FATAL_ERROR)
project(aigram VERSION 1.8 LANGUAGES CXX C)

set(NATIVERENDER_ROOT_PATH ${CMAKE_CURRENT_SOURCE_DIR})
set(TD_DIR ${CMAKE_CURRENT_SOURCE_DIR}/td)
set(OPENSSL_INSTALL_DIR ${CMAKE_CURRENT_SOURCE_DIR}/thirdparty/openssl)
set(OPENSSL_ROOT_DIR ${OPENSSL_INSTALL_DIR}/${OHOS_ARCH})
message(STATUS "openssl root dir is ${OPENSSL_ROOT_DIR}")

if(DEFINED PACKAGE_FIND_FILE)
    include(${PACKAGE_FIND_FILE})
endif()

include_directories(${NATIVERENDER_ROOT_PATH}
                    ${NATIVERENDER_ROOT_PATH}/include
                    ${TD_DIR})

set(CMAKE_MODULE_PATH "${TD_DIR}/CMake")
include(TdSetUpCompiler)
td_set_up_compiler()
string(APPEND CMAKE_CXX_FLAGS_RELWITHDEBINFO " -flto=thin -Oz")
list(APPEND CMAKE_FIND_ROOT_PATH "${OPENSSL_ROOT_DIR}")
add_subdirectory(${TD_DIR} td)

set(NATIVE_LIB "tdnapi")
add_library(${NATIVE_LIB} SHARED td_napi.cpp)

target_link_libraries(${NATIVE_LIB} PUBLIC libace_napi.z.so libhilog_ndk.z.so)
target_link_libraries(${NATIVE_LIB} PRIVATE Td::TdJsonStatic)
target_include_directories(${NATIVE_LIB} PUBLIC $<BUILD_INTERFACE:${TD_DIR}>)
target_compile_definitions(${NATIVE_LIB} PRIVATE TD_JSON_NAPI=1)

set(COMPONENT ${NATIVE_LIB})
install(TARGETS ${NATIVE_LIB} COMPONENT ${NATIVE_LIB}
  LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}"
)
