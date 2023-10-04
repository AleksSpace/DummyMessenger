# Список имен пользователей
import logging

USER_NAMES = ["User1", "User2", "User3", "User4", "User5", "User6", "User7", "User8", "User9", "User10"]

# Список URL-адресов реплик сервера
# SERVER_REPLICAS = ["http://127.0.0.1:8002", "http://127.0.0.1:8003"]
SERVER_REPLICAS = ["http://nginx", ]

# Количество запросов для каждой корутины
REQUESTS_PER_COROUTINE = 100

# Количество одновременно запускаемых корутин
CONCURRENT_COROUTINES = 50


logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

handler = logging.FileHandler('error_client.log', encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
