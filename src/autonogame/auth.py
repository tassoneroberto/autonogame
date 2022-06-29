#!/usr/bin/env python3

import logging
import traceback
from typing import Union

from autonogame.bot import OgameBot
from autonogame.config import Config
from autonogame.crypto import Crypto
from ogame import OGame

logging.getLogger(__name__)
logging.root.setLevel(logging.INFO)


class Auth(object):
    def __init__(self) -> None:
        super().__init__()

        self.config = Config()
        self.crypto = Crypto()

    def load_accounts(self) -> list[OgameBot]:
        logging.info("Loading accounts...")
        logged_in_accounts = []
        stored_accounts = self.config.get_stored_accounts()

        for account in stored_accounts:
            account_bot = self.login_client(
                account["universe"],
                account["email"],
                account["password"],
                account["token"],
            )
            if account_bot:
                logged_in_accounts.append(account_bot)
                logging.info(f"Account `{account['email']}` loaded!")
        return logged_in_accounts

    def login_client(
        self,
        account_universe,
        account_email,
        account_password,
        account_token=None,
    ) -> Union[OgameBot, None]:
        empire = self.login(
            universe=account_universe,
            email=account_email,
            password=account_password,
            token=account_token,
        )

        if empire:
            logging.info(f"Account `{account_email}` loaded!")
            credentials = {
                "universe": account_universe,
                "email": account_email,
                "password": account_password,
                "token": empire.token,
            }
            self.config.store_credentials(credentials)

            return OgameBot(empire)

        return None

    def login(self, universe, email, password, token=None):
        try:
            return OGame(
                universe=universe,
                username=email,
                password=password,
                token=token,
            )
        except Exception:
            logging.error(traceback.print_exc())

    def logout(self, account_bot: OgameBot):
        self.config.delete_account(
            universe=account_bot.empire.universe,
            username=account_bot.empire.username,
        )
        logging.info(
            f"Deleted credentials for account `{account_bot.empire.username}`"
        )
