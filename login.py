from grpclib.client import Channel

from generated.common import (
    XiLocale,
    XiDeviceId,
    XiClientVersion,
    XiDeviceIdDevicePrefix,
)
from generated.mobile.login.v1 import (
    LoginResponse,
    MobileLoginStub,
    UsernameCredentials,
    AndroidInfo,
    LoginRequest,
)

LOGIN_HOST = "login.kikprod.net"
BOT_NAME = "MyBot"


def key_from_password(username: str, password: str) -> str:
    # See https://github.com/tomer8007/kik-bot-api-unofficial/blob/new/kik_unofficial/utilities/cryptographic_utilities.py#L35
    raise NotImplementedError


async def login(
    username: str, password: str, device_id: str, android_id: str
) -> LoginResponse:
    channel = Channel(host=LOGIN_HOST, port=443, ssl=True)
    try:
        service = MobileLoginStub(channel)

        username_creds = UsernameCredentials(
            username=username,
            username_derived_passkey=key_from_password(username, password),
        )
        android_info = AndroidInfo(brand=BOT_NAME, android_id=android_id)

        response = await service.login(
            LoginRequest(
                username_creds=username_creds,
                locale=XiLocale(locale="en"),
                android_info=android_info,
                device_id=XiDeviceId(prefix=XiDeviceIdDevicePrefix.CAN, id=device_id),
                version=XiClientVersion(17, 1, 2, "31577"),
                recaptcha_token="none",
            )
        )
        return response
    finally:
        channel.close()
