from grpclib.client import Channel

from generated.common import (
    XiDeviceId,
    XiLocale,
    XiClientVersion,
    XiDeviceIdDevicePrefix,
)
from generated.mobile.login.jwt.v1 import (
    RefreshTokenResponse,
    MobileLoginJwtStub,
    RefreshTokenRequest,
)
from generated.mobile.login.v1 import UsernameCredentials, AndroidInfo

JWT_HOST = "api.kikprod.net"
BOT_NAME = "MyBot"


def key_from_password(uername: str, password: str) -> str:
    # See https://github.com/tomer8007/kik-bot-api-unofficial/blob/new/kik_unofficial/utilities/cryptographic_utilities.py#L35
    raise NotImplementedError


async def refresh(
    username: str, password: str, device_id: str, android_id: str, refresh_token: str
) -> RefreshTokenResponse:
    channel = Channel(host=JWT_HOST, port=443, ssl=True)
    try:
        service = MobileLoginJwtStub(channel)

        username_creds = UsernameCredentials(
            username=username,
            username_derived_passkey=key_from_password(username, password),
        )
        android_info = AndroidInfo(brand=BOT_NAME, android_id=android_id)

        response = await service.refresh_token(
            RefreshTokenRequest(
                username_creds=username_creds,
                device_id=XiDeviceId(prefix=XiDeviceIdDevicePrefix.CAN, id=device_id),
                locale=XiLocale(locale="en"),
                version=XiClientVersion(17, 1, 2, "31577"),
                android_info=android_info,
                recaptcha_token="none",
                refresh_token=refresh_token,
            )
        )
        return response
    finally:
        channel.close()
