import httpx
import random
import asyncio
import time

from config_client import REQUESTS_PER_COROUTINE, USER_NAMES, SERVER_REPLICAS, CONCURRENT_COROUTINES, logger


async def send_requests():
    """Функция для отправки запросов"""
    async with httpx.AsyncClient(timeout=20) as client:
        for _ in range(1, REQUESTS_PER_COROUTINE + 1):
            user = random.choice(USER_NAMES)
            message = {"sender": user, "text": "Hello, server!"}
            server_url = random.choice(SERVER_REPLICAS)
            try:
                await client.post(server_url + "/server/send_message/", json=message)
            except Exception as e:
                logger.error(f"Во время выполнения запроса произошла ошибка: {str(e)}")


async def main():
    """Запуск корутины"""
    start_time = time.time()
    tasks = [send_requests() for _ in range(CONCURRENT_COROUTINES)]
    await asyncio.gather(*tasks)
    end_time = time.time()
    total_time = end_time - start_time
    requests_per_second = REQUESTS_PER_COROUTINE * CONCURRENT_COROUTINES // total_time
    time_per_request = total_time / (REQUESTS_PER_COROUTINE * CONCURRENT_COROUTINES)

    print(f"Total time for 5000 requests: {total_time:.2f} seconds")
    print(f"Time per request: {time_per_request:.2f} seconds")
    print(f"Requests per second: {requests_per_second} requests/second")

if __name__ == "__main__":
    asyncio.run(main())
