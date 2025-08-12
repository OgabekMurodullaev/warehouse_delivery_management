from django.core.cache import cache
from django.conf import settings
from ipaddress import ip_address, IPv4Address, IPv6Address
import time


def _hour_ttl():
    return 60*60

def _seconds_ttl(seconds):
    return seconds

def _key_target_hour(target: str):
    # normalize target (lowercase email)
    return f"verify:target:hour:{target.lower()}"

def _key_target_cooldown(target: str):
    return  f"verify:target:cooldown:{target.lower()}"

def _key_ip_hour(ip: str):
    return f"verify:ip:hour:{ip}"

def _key_global_day():
    # day key
    return f"verify:global:day:{time.strftime('%Y-%m-%d')}"

def incr_with_expire(key: str, ttl: int):
    added = cache.add(key, 0, ttl) # will set 0 if not exists
    try:
        val = cache.incr(key)
    except Exception:
        # fallback: get/set
        val = cache.get(key, 0) + 1
        cache.set(key, val, ttl)
    return val

def check_and_increment_target(target: str):
    cfg = settings.VERIFICATION
    hour_key = _key_target_hour(target)
    cooldown_key = _key_target_cooldown(target)

    # cooldown: if exists -> deny
    if cache.get(cooldown_key):
        # remaining cooldown seconds
        return False, "CooldownActive"

    # increment hour counter
    cache.set(cooldown_key, 1, cfg.get('RESEND_COOLDOWN_SECONDS', 60))
    return True, None

def check_and_increment_ip(ip: str):
    cfg = settings.VERIFICATION
    ip_key = _key_ip_hour(ip)
    count = incr_with_expire(ip_key, _hour_ttl())
    if count > cfg.get('IP_RESEND_LIMIT_PER_HOUR', 30):
        return False, "IPHourlyLimitExceeded"
    return True, None

def increment_global_day():
    key = _key_global_day()
    val = incr_with_expire(key, 24*60*60)
    return val