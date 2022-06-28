#!/usr/bin/env python3

import random
import string

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class Crypto(object):
    def __init__(self) -> None:
        super().__init__()

        self.secret_key = b"ZdBGoq4JgWFzs0HxFo38Me0jxnrEIp1E"
        self.encoding_format = "utf-8"

    def generate_random_string(self, length):
        letters = (
            string.ascii_lowercase + string.ascii_uppercase + string.digits
        )
        return bytes(
            "".join(random.choice(letters) for _ in range(length)),
            self.encoding_format,
        )

    def decrypt(self, ciphertext):
        msg = AESGCM(self.secret_key).decrypt(
            ciphertext[:12], ciphertext[12:], None
        )
        return msg.decode(self.encoding_format)

    def encrypt(self, text):
        nonce = self.generate_random_string(12)
        return nonce + AESGCM(self.secret_key).encrypt(
            nonce, bytes(text, self.encoding_format), None
        )
