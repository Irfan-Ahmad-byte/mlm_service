import json

from app.core.redis import check_redis_connection
from app.configs.configs import settings
from app.utils.logs import get_logger


logger = get_logger(__name__)

redis_client = check_redis_connection()

def cache_key_user(user_id): return f"mlm_user:{user_id}"
def cache_key_downline(user_id): return f"mlm_downline:{user_id}"

# Serialize and Deserialize
def serialize(obj): return json.dumps(obj, default=str)
def deserialize(json_str): return json.loads(json_str)

def get_cached_user(user_id):
    if not settings.REDIS_ENABLED:
        logger.debug("Redis is not enabled, skipping cache retrieval for user.")
        return None
    data = redis_client.get(cache_key_user(user_id))
    return deserialize(data) if data else None

def set_cached_user(user_id, data):
    if not settings.REDIS_ENABLED:
        logger.debug("Redis is not enabled, skipping cache setting for user.")
        return None
    redis_client.setex(cache_key_user(user_id), 3600, serialize(data))

def get_cached_downline(user_id):
    if not settings.REDIS_ENABLED:
        logger.debug("Redis is not enabled, skipping cache retrieval for downline.")
        return None
    data = redis_client.get(cache_key_downline(user_id))
    return deserialize(data) if data else None

def set_cached_downline(user_id, data):
    if not settings.REDIS_ENABLED:
        logger.debug("Redis is not enabled, skipping cache setting for downline.")
        return None
    redis_client.setex(cache_key_downline(user_id), 3600, serialize(data))

def invalidate_user_cache(user_id):
    if not settings.REDIS_ENABLED:
        logger.debug("Redis is not enabled, skipping cache invalidation for user.")
        return None
    redis_client.delete(cache_key_user(user_id))
    redis_client.delete(cache_key_downline(user_id))