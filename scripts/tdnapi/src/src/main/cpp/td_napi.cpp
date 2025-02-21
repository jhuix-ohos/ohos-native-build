#include <unistd.h>
#include <cstdarg>
#include <pthread.h>
#include <hilog/log.h> // hilog, need link libhilog_ndk.z.so
#include "td_work.h"

static napi_value TdCreate(napi_env env, napi_callback_info _) {
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

    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

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

    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    napi_valuetype valuetype0;
    napi_typeof(env, args[0], &valuetype0);

    double timeout;
    napi_get_value_double(env, args[0], &timeout);

    const char *content = td_receive(timeout);
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

    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    napi_valuetype valuetype0;
    napi_typeof(env, args[0], &valuetype0);

    std::string request = value2string(env, args[0]);
    const char *content = td_execute(request.c_str());
    if (content == nullptr) {
        return nullptr;
    }

    napi_value result;
    if (napi_create_string_utf8(env, content, NAPI_AUTO_LENGTH, &result) != napi_ok) {
        return nullptr;
    }

    return result;
}


static void on_log_message(int verbosityLevel, const char *logMessage) {
    auto pid = getpid();
    auto tid = pthread_self();
    switch (verbosityLevel) {
    case VERBOSITY_NAME(FATAL):
        OH_LOG_FATAL(LOG_APP, "[%u-%lu] %s", pid, tid, logMessage);
        break;
    case VERBOSITY_NAME(ERROR):
        OH_LOG_ERROR(LOG_APP, "[%u-%lu] %s", pid, tid, logMessage);
        break;
    case VERBOSITY_NAME(WARNING):
        OH_LOG_WARN(LOG_APP, "[%u-%lu] %s", pid, tid, logMessage);
        break;
    case VERBOSITY_NAME(INFO):
        OH_LOG_INFO(LOG_APP, "[%u-%lu] %s", pid, tid, logMessage);
        break;
    default:
        OH_LOG_DEBUG(LOG_APP, "[%u-%lu] %s", pid, tid, logMessage);
        break;
    }
}

static void log_message(int verbosityLevel, const char *format, ...) {
    va_list args;
    va_start(args, format);
    char txt[1024];
    int n = vsnprintf(txt, 1024, format, args);
    txt[n] = 0;
    va_end(args);
    on_log_message(verbosityLevel, txt);
}

static napi_value TdSetLogVerbosityLevel(napi_env env, napi_callback_info info) {
    size_t argc = 1;
    napi_value args[1] = {nullptr};

    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    napi_valuetype valuetype0;
    napi_typeof(env, args[0], &valuetype0);

    int32_t verbosityLevel;
    napi_get_value_int32(env, args[0], &verbosityLevel);

    td_set_log_message_callback(verbosityLevel, on_log_message);
    return nullptr;
}

static napi_value TdJsonCreate(napi_env env, napi_callback_info _) {
    void *clt = td_json_client_create();
    napi_value result;
    napi_create_bigint_uint64(env, (int64_t)clt, &result);
    return result;
}

static napi_value TdJsonSend(napi_env env, napi_callback_info info) {
    size_t argc = 2;
    napi_value args[2] = {nullptr};

    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

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
    td_json_client_send((void *)client, request.c_str());
    return nullptr;
}

static napi_value TdJsonReceive(napi_env env, napi_callback_info info) {
    size_t argc = 2;
    napi_value args[2] = {nullptr};

    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

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

    const char *content = td_json_client_receive((void *)client, timeout);
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

    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

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
    const char *content = td_json_client_execute((void *)client, request.c_str());
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

    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    napi_valuetype valuetype0;
    napi_typeof(env, args[0], &valuetype0);

    bool lossLess = false;
    uint64_t client;
    napi_get_value_bigint_uint64(env, args[0], &client, &lossLess);
    if (!lossLess) {
        return nullptr;
    }

    td_json_client_destroy((void *)client);
    return nullptr;
}

///////////////////////////////////////////////////////////////////

static napi_value TdClientCreate(napi_env env, napi_callback_info info) {
    size_t argc = 1;
    napi_value args[1] = {nullptr};

    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    napi_valuetype valuetype0;
    napi_typeof(env, args[0], &valuetype0);

    double timeout;
    napi_get_value_double(env, args[0], &timeout);

    void *clt = td_json_client_create();
    auto worker = new ReceiveWorker(clt, timeout);
    napi_value result;
    napi_create_bigint_uint64(env, (int64_t)worker, &result);
    return result;
}

static napi_value TdClientSend(napi_env env, napi_callback_info info) {
    size_t argc = 2;
    napi_value args[2] = {nullptr};

    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    napi_valuetype valuetype0;
    napi_typeof(env, args[0], &valuetype0);

    napi_valuetype valuetype1;
    napi_typeof(env, args[1], &valuetype1);

    bool lossLess = false;
    uint64_t obj;
    napi_get_value_bigint_uint64(env, args[0], &obj, &lossLess);
    if (!lossLess) {
        return nullptr;
    }

    std::string request = value2string(env, args[1]);
    ReceiveWorker *worker = reinterpret_cast<ReceiveWorker *>(obj);
    td_json_client_send((void *)worker->GetClient(), request.c_str());
    return nullptr;
}

// Do not call again until the promise is resolved/rejected.
static napi_value TdClientReceive(napi_env env, napi_callback_info info) {
    size_t argc = 2;
    napi_value args[2] = {nullptr};

    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    napi_valuetype valuetype0;
    napi_typeof(env, args[0], &valuetype0);

    bool lossLess = false;
    uint64_t obj;
    napi_get_value_bigint_uint64(env, args[0], &obj, &lossLess);
    if (!lossLess) {
        // return failedPromise(env, "input params are invalid");
        return nullptr;
    }

    napi_ref callbackRef = nullptr;
    napi_create_reference(env, args[1], 1, &callbackRef);
    ReceiveWorker *worker = reinterpret_cast<ReceiveWorker *>(obj);
    return worker->NewTask(env, callbackRef);
}

static napi_value TdClientExecute(napi_env env, napi_callback_info info) {
    size_t argc = 2;
    napi_value args[2] = {nullptr};

    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    napi_valuetype valuetype0;
    napi_typeof(env, args[0], &valuetype0);

    napi_valuetype valuetype1;
    napi_typeof(env, args[1], &valuetype1);

    bool lossLess = false;
    uint64_t obj;
    napi_get_value_bigint_uint64(env, args[0], &obj, &lossLess);
    if (!lossLess) {
        return nullptr;
    }

    std::string request = value2string(env, args[1]);
    ReceiveWorker *worker = reinterpret_cast<ReceiveWorker *>(obj);
    const char *response = td_json_client_execute((void *)worker->GetClient(), request.c_str());
    if (response == nullptr) {
        return nullptr;
    }

    napi_value result;
    if (napi_create_string_utf8(env, response, NAPI_AUTO_LENGTH, &result) != napi_ok) {
        return nullptr;
    }

    return result;
}

// Preferably do not call this if the receive promise is pending.
static napi_value TdClientDestroy(napi_env env, napi_callback_info info) {
    size_t argc = 1;
    napi_value args[1] = {nullptr};

    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    napi_valuetype valuetype0;
    napi_typeof(env, args[0], &valuetype0);

    bool lossLess = false;
    uint64_t obj;
    napi_get_value_bigint_uint64(env, args[0], &obj, &lossLess);
    if (!lossLess) {
        return nullptr;
    }

    ReceiveWorker *worker = reinterpret_cast<ReceiveWorker *>(obj);
    delete worker;
    return nullptr;
}


static ReceiveWorker worker;

// Create the worker and set the receive timeout explicitly.
static napi_value TdInit(napi_env env, napi_callback_info info) {
    size_t argc = 1;
    napi_value args[1] = {nullptr};

    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    napi_valuetype valuetype0;
    napi_typeof(env, args[0], &valuetype0);

    double timeout;
    napi_get_value_double(env, args[0], &timeout);
    worker.SetTimeout(timeout);
    return nullptr;
}

// Should not be called again until promise is resolved/rejected.
static napi_value TdAsyncReceive(napi_env env, napi_callback_info info) {
    size_t argc = 1;
    napi_value args[1] = {nullptr};

    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    napi_ref callbackRef = nullptr;
    napi_create_reference(env, args[0], 1, &callbackRef);
    worker.NewTask(env, callbackRef);
    return nullptr;
}

EXTERN_C_START
static napi_value Init(napi_env env, napi_value exports) {
    napi_property_descriptor desc[] = {
        {"tdCreate", nullptr, TdCreate, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"tdSend", nullptr, TdSend, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"tdReceive", nullptr, TdReceive, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"tdExecute", nullptr, TdExecute, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"tdInit", nullptr, TdInit, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"tdAsyncReceive", nullptr, TdAsyncReceive, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"tdSetLogVerbosityLevel", nullptr, TdSetLogVerbosityLevel, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"tdJsonCreate", nullptr, TdJsonCreate, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"tdJsonSend", nullptr, TdJsonSend, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"tdJsonReceive", nullptr, TdJsonReceive, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"tdJsonExecute", nullptr, TdJsonExecute, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"tdJsonDestroy", nullptr, TdJsonDestroy, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"tdClientCreate", nullptr, TdClientCreate, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"tdClientSend", nullptr, TdClientSend, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"tdClientReceive", nullptr, TdClientReceive, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"tdClientExecute", nullptr, TdClientExecute, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"tdClientDestroy", nullptr, TdClientDestroy, nullptr, nullptr, nullptr, napi_default, nullptr}};
    napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc);
    return exports;
}
EXTERN_C_END

static napi_module tdModule = {
    .nm_version = 1,
    .nm_flags = 0,
    .nm_filename = nullptr,
    .nm_register_func = Init,
    .nm_modname = "tdnapi",
    .nm_priv = ((void *)0),
    .reserved = {0},
};

extern "C" __attribute__((constructor)) void RegisterTdnapiModule(void) { napi_module_register(&tdModule); }
