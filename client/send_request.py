import httpx
import random
import asyncio
import time

from config_client import REQUESTS_PER_COROUTINE, USER_NAMES, SERVER_REPLICAS, CONCURRENT_COROUTINES


async def send_requests():
    """Функция для отправки запросов"""
    async with httpx.AsyncClient() as client:
        start_time = time.time()
        for _ in range(REQUESTS_PER_COROUTINE):
            user = random.choice(USER_NAMES)
            message = {"sender": user, "text": "Hello, server!"}
            server_url = random.choice(SERVER_REPLICAS)
            response = await client.post(server_url + "/server/send_message/", json=message)
            if response.status_code != 200:
                print(f"Request failed with status code {response.status_code}")
        end_time = time.time()
        return end_time - start_time


async def main():
    """Запуск корутины"""
    tasks = [send_requests() for _ in range(CONCURRENT_COROUTINES)]
    results = await asyncio.gather(*tasks)

    total_time = sum(results)
    requests_per_second = REQUESTS_PER_COROUTINE * CONCURRENT_COROUTINES / total_time

    print(f"Total time for 5000 requests: {total_time} seconds")
    print(f"Time per request: {total_time / (REQUESTS_PER_COROUTINE * CONCURRENT_COROUTINES)} seconds")
    print(f"Requests per second: {requests_per_second} requests/second")

if __name__ == "__main__":
    asyncio.run(main())
