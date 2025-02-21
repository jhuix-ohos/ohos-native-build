#include <string>
#include <mutex>
#include <condition_variable>
#include "napi/native_api.h"
#include "td/telegram/td_json_client.h"

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
static void log_message(int verbosityLevel, const char *format, ...);

// static napi_value failedPromise(napi_env env, const char *message) {
//     napi_value failed_promise = nullptr;
//     napi_deferred failed_deferred = nullptr;
//     napi_create_promise(env, &failed_deferred, &failed_promise);
//     napi_value result = nullptr;
//     std::string error = message;
//     napi_create_string_utf8(env, error.c_str(), error.length(), &result);
//     napi_reject_deferred(env, failed_deferred, result);
//     return failed_promise;
// }

class ReceiveWorker {
public:
    ReceiveWorker()
        : client(nullptr)
        , timeout(0)
        , stop(false)
        , ready(false)
        , asyncWork(nullptr)
        , response(nullptr)
        , callbackRef(nullptr) {}
    ReceiveWorker(void *client, double timeout)
        : client(client)
        , timeout(timeout)
        , stop(false)
        , ready(false)
        , asyncWork(nullptr)
        , response(nullptr)
        , callbackRef(nullptr) {}
    ~ReceiveWorker() {
        if (ready) {
            std::unique_lock<std::mutex> lock(mutex);
            stop = true;
            cv.wait(lock);
        }
        if (client != nullptr) {
            td_json_client_destroy(client);
            client = nullptr;
        }
    }

    // A task can be added only after the previous task is finished.
    napi_value NewTask(napi_env env, napi_ref callbackRef) {
        // if (deferred != nullptr) {
        //    return failedPromise(env, "td receive is not finished yet");
        // }

        // napi_value promise = nullptr;
        // napi_status status = napi_create_promise(env, &deferred, &promise);
        // if (status != napi_ok) {
        //     return failedPromise(env, "td receive promise be created failed");
        // }

        this->callbackRef = callbackRef;
        napi_value resourceName = nullptr;
        napi_create_string_utf8(env, "AsyncTdTask", NAPI_AUTO_LENGTH, &resourceName);
        // 创建异步任务
        napi_create_async_work(env, nullptr, resourceName, ExecuteCB, CompleteCB, this, &asyncWork);
        // 将异步任务加入队列
        napi_queue_async_work(env, asyncWork);
        return nullptr;
    }

    inline void *GetClient() { return client; }
    inline void SetTimeout(double timeout) { this->timeout = timeout; }

private:
    static void ExecuteCB(napi_env env, void *data) {
        ReceiveWorker *worker = reinterpret_cast<ReceiveWorker *>(data);
        worker->ready = true;
        worker->response = nullptr;
        while (!worker->stop) {
            const char *response = worker->client == nullptr ? td_receive(worker->timeout)
                                                             : td_json_client_receive(worker->client, worker->timeout);
            // TDLib stores the response in thread-local storage that is deallocated
            // on execute() and receive(). Since we never call execute() in this
            // thread, it should be safe not to copy the response here.
            if (nullptr == response) {
                log_message(VERBOSITY_NAME(WARNING), "td %p receive data is null", worker->client);
                continue;
            }

            // napi_value result = nullptr;
            // napi_create_string_utf8(env, response, strlen(response), &result);
            // napi_resolve_deferred(env, worker->deferred, result);
            worker->response = response;
            break;
        }

        // napi_value result = nullptr;
        // std::string error = "completed td receive";
        // napi_create_string_utf8(env, error.c_str(), error.length(), &result);
        // napi_reject_deferred(env, worker->deferred, result);
    }

    static void CompleteCB(napi_env env, napi_status status, void *data) {
        ReceiveWorker *worker = reinterpret_cast<ReceiveWorker *>(data);
        if (worker->response) {
            // napi_resolve_deferred(env, worker->deferred, worker->result);
            napi_value callbackArgs[1] = {nullptr};
            napi_create_string_utf8(env, worker->response, strlen(worker->response), &callbackArgs[0]); 
            napi_value callback = nullptr;
            napi_get_reference_value(env, worker->callbackRef, &callback);
            napi_value result;
            napi_value undefined;
            napi_get_undefined(env, &undefined);
            status = napi_call_function(env, undefined, callback, 1, callbackArgs, &result);
            if (status != napi_ok) {
                log_message(VERBOSITY_NAME(ERROR),
                    "after td %p receive data, call function failed",
                    worker->client, status);
            }
        }
        worker->ready = false;
        if (!worker->stop) {
            napi_queue_async_work(env, worker->asyncWork);
        } else {
            napi_delete_reference(env, worker->callbackRef);
            napi_delete_async_work(env, worker->asyncWork);
            // napi_value result = nullptr;
            // std::string error = "completed td receive";
            // napi_create_string_utf8(env, error.c_str(), error.length(), &result);
            // napi_reject_deferred(env, worker->deferred, result);
            worker->cv.notify_all();            
        }
    }

    void *client;
    double timeout;
    volatile bool stop;
    volatile bool ready;
    std::mutex mutex;
    std::condition_variable cv;
    napi_async_work asyncWork;
    // napi_deferred deferred;
    const char *response;
    napi_ref callbackRef;
};
