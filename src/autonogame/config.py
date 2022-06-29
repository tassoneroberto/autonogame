#!/usr/bin/env python3

import configparser
import glob
import logging
import os
import traceback

from autonogame.bot import OgameBot
from autonogame.crypto import Crypto
from ogame import OGame

logging.getLogger(__name__)
logging.root.setLevel(logging.INFO)


class Config(object):
    def __init__(self) -> None:
        super().__init__()

        # create configuration folder if it does not exist
        self.app_folder = os.path.join(os.getenv("APPDATA"), "autonogame")
        self.accounts_folder = os.path.join(self.app_folder, "accounts")
        for folder in [self.app_folder, self.accounts_folder]:
            if not os.path.exists(folder):
                os.makedirs(folder)

        self.config_parser = configparser.ConfigParser()
        self.crypto = Crypto()

    def exists_account(self) -> bool:
        return len(os.listdir(self.accounts_folder)) != 0

    def get_stored_accounts(self) -> list[OgameBot]:
        accounts = []
        os.chdir(self.accounts_folder)
        if len(os.listdir(self.accounts_folder)) != 0:
            for file in glob.glob("*.ini"):
                account = {}
                self.config_parser.read(file)
                account["universe"] = self.config_parser["credentials"][
                    "universe"
                ]
                account["email"] = self.config_parser["credentials"]["email"]
                with open(
                    f"{account['universe']}_"
                    + f"{account['email']}_secret1.bin".lower(),
                    "rb",
                ) as encrypted_password_file:
                    account["password"] = self.crypto.decrypt(
                        encrypted_password_file.read()
                    )
                with open(
                    f"{account['universe']}_"
                    + f"{account['email']}_secret2.bin".lower(),
                    "rb",
                ) as encrypted_token_file:
                    account["token"] = self.crypto.decrypt(
                        encrypted_token_file.read()
                    )
                accounts.append(account)
        return accounts

    def already_logged_in(self, account_universe, account_email) -> bool:
        os.chdir(self.accounts_folder)
        for file in glob.glob("*.ini"):
            account_info = file[0:-4].lower().split("_")
            return (
                account_universe.lower() == account_info[0]
                and account_email.lower() == account_info[1]
            )

    def login_client(
        self,
        account_universe,
        account_email,
        account_password,
        account_token=None,
    ) -> OgameBot:
        empire = self.login(
            universe=account_universe,
            email=account_email,
            password=account_password,
            token=account_token,
        )

        if empire:
            # Store settings
            config = configparser.ConfigParser()
            config.add_section("credentials")
            config["credentials"]["universe"] = account_universe
            config["credentials"]["email"] = account_email
            with open(
                f"{account_universe}_{account_email}.ini".lower(), "w"
            ) as configFile:
                config.write(configFile)

            # store encrypted password
            with open(
                f"{account_universe}_{account_email}_secret1.bin".lower(), "wb"
            ) as encrypted_password_file:
                encrypted_password_file.write(
                    self.crypto.encrypt_password(account_password)
                )

            # store session token
            with open(
                f"{account_universe}_{account_email}_secret2.bin".lower(), "wb"
            ) as encrypted_token_file:
                encrypted_token_file.write(
                    self.crypto.encrypt_password(empire.token)
                )

            return OgameBot(empire)

        return False

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

    def delete_account(self, universe, username):
        for file in os.listdir(self.accounts_folder):
            if file.startswith(f"{universe}_{username}".lower()):
                if os.path.exists(file):
                    os.remove(file)
                else:
                    logging.error(
                        "Error: the configuration file can not be deleted."
                    )

    def store_credentials(self, credentials):
        if not self.config_parser.has_section("credentials"):
            self.config_parser.add_section("credentials")
        self.config_parser["credentials"]["universe"] = credentials["universe"]
        self.config_parser["credentials"]["email"] = credentials["email"]
        file_prefix = f"{credentials['universe']}_{credentials['email']}"
        with open(f"{file_prefix}.ini".lower(), "w") as configFile:
            self.config_parser.write(configFile)

        # store encrypted password
        with open(
            f"{file_prefix}_secret1.bin".lower(), "wb"
        ) as encrypted_password_file:
            encrypted_password_file.write(
                self.crypto.encrypt(credentials["password"])
            )

        # store session token
        with open(
            f"{file_prefix}_secret2.bin".lower(), "wb"
        ) as encrypted_token_file:
            encrypted_token_file.write(
                self.crypto.encrypt(credentials["token"])
            )

    def save_settings(self, universe, username, settings):
        config_file = f"{universe}_{username}.ini".lower()
        self.config_parser.read(config_file)
        if not self.config_parser.has_section("settings"):
            self.config_parser.add_section("settings")
        for key, value in settings.items():
            self.config_parser["settings"][key] = str(value)
        with open(config_file, "w") as configFile:
            self.config_parser.write(configFile)

    def get_stored_settings(self, universe, username):
        config_file = f"{universe}_{username}.ini".lower()
        self.config_parser.read(config_file)

        # set default settings
        settings = {}
        # TODO use enums
        settings["build_resources"] = True
        settings["build_deposits"] = True
        settings["build_facilities"] = True

        # settings found
        if self.config_parser.has_section("settings"):
            for key, value in self.config_parser["settings"].items():
                settings[key] = value

        return settings
