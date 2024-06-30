from fastapi import FastAPI, Request, Response
from concurrent.futures import ThreadPoolExecutor
import uvicorn
import asyncio
import time

app = FastAPI()

thread_poll = ThreadPoolExecutor(max_workers=10)


@app.get("/asy2")
async def asyncio2(request: Request):
    request_message = request.query_params.get("msg")

    # 获取asyncio loop
    loop = asyncio.get_event_loop()

    task = {
        "msg": request_message
    }

    # 准备计算方法
    def task_handler():
        print(f"task received:" + task["msg"])
        task_result = task["msg"].upper()
        time.sleep(10)
        return task_result

    # 提交给线程池执行 并等待结果 在这期间可以接受其他请求
    result = await loop.run_in_executor(thread_poll, task_handler)
    return Response(result)


if __name__ == '__main__':
    # 启动 并使用postman测试
    uvicorn.run(app, host='localhost', port=8000)

