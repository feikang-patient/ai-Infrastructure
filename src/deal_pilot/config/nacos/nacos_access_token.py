import time
import asyncio
import httpx
from deal_pilot.config.nacos_settings import nacos_settings

_access_token: str | None = None
_expires_at = 0
_token_lock = asyncio.Lock()


async def get_access_token() -> str:

    global _access_token, _expires_at
    if _access_token and time.monotonic() < _expires_at:
        return _access_token

    # 同一时刻只能一个协程进入锁去获取
    async with _token_lock:
        if _access_token and time.monotonic() < _expires_at:
            return _access_token
        # 重新获取 token
        start_time = time.monotonic()  # 提前
        async with httpx.AsyncClient(
            base_url=nacos_settings.server_address, timeout=10
        ) as client:
            response = await client.post(
                "/nacos/v3/auth/user/login",
                data={
                    "username": nacos_settings.username,
                    "password": nacos_settings.password,
                },
            )
            response.raise_for_status()
            login_result = response.json()

        token = login_result["accessToken"]
        ttl = float(login_result["tokenTtl"])  # token 有效期，单位秒
        _access_token = token
        _expires_at = start_time + ttl - 30

        return token
