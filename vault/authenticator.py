import time
import hmac
import hashlib
import base64
import struct


class TOTP:
    def __init__(self, secret: str, digits: int = 6, interval: int = 30):
        self.secret = secret
        self.digits = digits
        self.interval = interval

    def _time_counter(self) -> int:
        return int(time.time()) // self.interval

    def _hmac_sha1(self, counter: int) -> bytes:
        key = base64.b32decode(self.secret.upper(), casefold=True)
        msg = struct.pack(">Q", counter)
        return hmac.new(key, msg, hashlib.sha1).digest()

    def generate(self) -> str:
        counter = self._time_counter()
        hmac_digest = self._hmac_sha1(counter)

        offset = hmac_digest[-1] & 0x0F
        code = struct.unpack(">I", hmac_digest[offset:offset + 4])[0]
        code &= 0x7FFFFFFF

        otp = code % (10 ** self.digits)
        return str(otp).zfill(self.digits)

    def verify(self, token: str, window: int = 1) -> bool:
        """
        window = allowed time drift (± steps)
        """
        current = self._time_counter()

        for i in range(-window, window + 1):
            counter = current + i
            hmac_digest = self._hmac_sha1(counter)

            offset = hmac_digest[-1] & 0x0F
            code = struct.unpack(">I", hmac_digest[offset:offset + 4])[0]
            code &= 0x7FFFFFFF
            otp = str(code % (10 ** self.digits)).zfill(self.digits)

            if otp == token:
                return True

        return False
