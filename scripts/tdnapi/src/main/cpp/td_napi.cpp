#include <string>
#include <hilog/log.h>  // hilog, need link libhilog_ndk.z.so
#include "napi/native_api.h"
#include "td/telegram/td_json_client.h"

static napi_value TdCreate(napi_env env, napi_callback_info info) {
    int clientId = td_create_client_id();
    napi_value result;
    napi_create_int32(env, clientId, &result);
    return result;
}

static std::string value2string(napi_env env, napi_value value) {
    size_t size = 0;
    napi_get_value_string_utf8(env, value, nullptr, 0, &size);
    std::string result;
    result.resize(size + 1);
    napi_get_value_string_utf8(env, value, &result[0], size + 1, &size);
    return result;
}

static napi_value TdSend(napi_env env, napi_callback_info info) {
    size_t argc = 2;
    napi_value args[2] = {nullptr};

    napi_get_cb_info(env, info, &argc, args , nullptr, nullptr);

    napi_valuetype valuetype0;
    napi_typeof(env, args[0], &valuetype0);

    napi_valuetype valuetype1;
    napi_typeof(env, args[1], &valuetype1);

    int32_t clientId;
    napi_get_value_int32(env, args[0], &clientId);
    std::string request = value2string(env, args[1]);
    td_send(clientId, request.c_str());
    return nullptr;
}

static napi_value TdReceive(napi_env env, napi_callback_info info) {
    size_t argc = 1;
    napi_value args[1] = {nullptr};

    napi_get_cb_info(env, info, &argc, args , nullptr, nullptr);

    napi_valuetype valuetype0;
    napi_typeof(env, args[0], &valuetype0);
    
    double timeout;
    napi_get_value_double(env, args[0], &timeout);
    
    const char* content = td_receive(timeout);
    if (content == nullptr) {
        return nullptr;
    }
    
    napi_value result;
    if (napi_create_string_utf8(env, content, NAPI_AUTO_LENGTH, &result) != napi_ok) {
        return nullptr;
    }
    
    return result;
}

static napi_value TdExecute(napi_env env, napi_callback_info info) {
    size_t argc = 1;
    napi_value args[1] = {nullptr};

    napi_get_cb_info(env, info, &argc, args , nullptr, nullptr);

    napi_valuetype valuetype0;
    napi_typeof(env, args[0], &valuetype0);
    
    std::string request = value2string(env, args[0]);
    const char * content = td_execute(request.c_str());
    if (content == nullptr) {
        return nullptr;
    }
    
    napi_value result;
    if (napi_create_string_utf8(env, content, NAPI_AUTO_LENGTH, &result) != napi_ok) {
        return nullptr;
    }
    
    return result;
}

#undef LOG_TAG
#define LOG_TAG "DLTD"
#define VERBOSITY_NAME(x) verbosity_##x
// constexpr int VERBOSITY_NAME(PLAIN) = -1;
constexpr int VERBOSITY_NAME(FATAL) = 0;
constexpr int VERBOSITY_NAME(ERROR) = 1;
constexpr int VERBOSITY_NAME(WARNING) = 2;
constexpr int VERBOSITY_NAME(INFO) = 3;
// constexpr int VERBOSITY_NAME(DEBUG) = 4;
// constexpr int VERBOSITY_NAME(NEVER) = 1024;

static void on_log_message(int verbosityLevel, const char *logMessage) {
    switch (verbosityLevel) {
      case VERBOSITY_NAME(FATAL):
        OH_LOG_FATAL(LOG_APP, "%s", logMessage);
        break;
      case VERBOSITY_NAME(ERROR):
        OH_LOG_ERROR(LOG_APP, "%s", logMessage);
        break;
      case VERBOSITY_NAME(WARNING):
        OH_LOG_WARN(LOG_APP, "%s", logMessage);
        break;
      case VERBOSITY_NAME(INFO):
        OH_LOG_INFO(LOG_APP, "%s", logMessage);
        break;
      default:
        OH_LOG_DEBUG(LOG_APP, "%s", logMessage);
        break;
    }
}

static napi_value TdSetLogVerbosityLevel(napi_env env, napi_callback_info info) {
    size_t argc = 1;
    napi_value args[1] = {nullptr};

    napi_get_cb_info(env, info, &argc, args , nullptr, nullptr);

    napi_valuetype valuetype0;
    napi_typeof(env, args[0], &valuetype0);

    int32_t verbosityLevel;
    napi_get_value_int32(env, args[0], &verbosityLevel);
    
    td_set_log_message_callback(verbosityLevel, on_log_message);
    return nullptr;
}

static napi_value TdJsonCreate(napi_env env, napi_callback_info info) {
    void* clt = td_json_client_create();
    napi_value result;
    napi_create_bigint_uint64(env, (int64_t)clt, &result);
    return result;
}

static napi_value TdJsonSend(napi_env env, napi_callback_info info) {
    size_t argc = 2;
    napi_value args[2] = {nullptr};

    napi_get_cb_info(env, info, &argc, args , nullptr, nullptr);

    napi_valuetype valuetype0;
    napi_typeof(env, args[0], &valuetype0);

    napi_valuetype valuetype1;
    napi_typeof(env, args[1], &valuetype1);

    bool lossLess = false;
    uint64_t client;
    napi_get_value_bigint_uint64(env, args[0], &client, &lossLess);
    if (!lossLess) {
        return nullptr;
    }
    
    std::string request = value2string(env, args[1]);
    td_json_client_send((void*)client, request.c_str());
    return nullptr;
}

static napi_value TdJsonReceive(napi_env env, napi_callback_info info) {
    size_t argc = 2;
    napi_value args[2] = {nullptr};

    napi_get_cb_info(env, info, &argc, args , nullptr, nullptr);

    napi_valuetype valuetype0;
    napi_typeof(env, args[0], &valuetype0);

    napi_valuetype valuetype1;
    napi_typeof(env, args[1], &valuetype1);

    bool lossLess = false;
    uint64_t client;
    napi_get_value_bigint_uint64(env, args[0], &client, &lossLess);
    if (!lossLess) {
        return nullptr;
    }
    
    double timeout;
    napi_get_value_double(env, args[1], &timeout);
    
    const char* content = td_json_client_receive((void*)client, timeout);
    if (content == nullptr) {
        return nullptr;
    }
    
    napi_value result;
    if (napi_create_string_utf8(env, content, NAPI_AUTO_LENGTH, &result) != napi_ok) {
        return nullptr;
    }
    
    return result;
}

static napi_value TdJsonExecute(napi_env env, napi_callback_info info) {
    size_t argc = 2;
    napi_value args[2] = {nullptr};

    napi_get_cb_info(env, info, &argc, args , nullptr, nullptr);

    napi_valuetype valuetype0;
    napi_typeof(env, args[0], &valuetype0);

    napi_valuetype valuetype1;
    napi_typeof(env, args[1], &valuetype1);

    bool lossLess = false;
    uint64_t client;
    napi_get_value_bigint_uint64(env, args[0], &client, &lossLess);
    if (!lossLess) {
        return nullptr;
    }
    
    std::string request = value2string(env, args[1]);
    const char * content = td_json_client_execute((void*)client, request.c_str());
    if (content == nullptr) {
        return nullptr;
    }
    
    napi_value result;
    if (napi_create_string_utf8(env, content, NAPI_AUTO_LENGTH, &result) != napi_ok) {
        return nullptr;
    }
    
    return result;
}

static napi_value TdJsonDestroy(napi_env env, napi_callback_info info) {
    size_t argc = 1;
    napi_value args[1] = {nullptr};

    napi_get_cb_info(env, info, &argc, args , nullptr, nullptr);

    napi_valuetype valuetype0;
    napi_typeof(env, args[0], &valuetype0);

    bool lossLess = false;
    uint64_t client;
    napi_get_value_bigint_uint64(env, args[0], &client, &lossLess);
    if (!lossLess) {
        return nullptr;
    }
    
    td_json_client_destroy((void*)client);        
    return nullptr;
}

EXTERN_C_START
static napi_value Init(napi_env env, napi_value exports)
{
    napi_property_descriptor desc[] = {
        { "tdCreate", nullptr, TdCreate, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "tdSend", nullptr, TdSend, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "tdReceive", nullptr, TdReceive, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "tdExecute", nullptr, TdExecute, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "tdSetLogVerbosityLevel", nullptr, TdSetLogVerbosityLevel, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "tdJsonCreate", nullptr, TdJsonCreate, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "tdJsonSend", nullptr, TdJsonSend, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "tdJsonReceive", nullptr, TdJsonReceive, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "tdJsonExecute", nullptr, TdJsonExecute, nullptr, nullptr, nullptr, napi_default, nullptr },
        { "tdJsonDestroy", nullptr, TdJsonDestroy, nullptr, nullptr, nullptr, napi_default, nullptr }
    };
    napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc);
    return exports;
}
EXTERN_C_END

static napi_module demoModule = {
    .nm_version = 1,
    .nm_flags = 0,
    .nm_filename = nullptr,
    .nm_register_func = Init,
    .nm_modname = "tdnapi",
    .nm_priv = ((void*)0),
    .reserved = { 0 },
};

extern "C" __attribute__((constructor)) void RegisterTdjsonModule(void)
{
    napi_module_register(&demoModule);
}
