#!/usr/bin/env python3

import logging
import threading
import tkinter as tk
from tkinter import ttk

from autonogame.auth import Auth
from autonogame.bot import OgameBot
from autonogame.config import Config

logging.getLogger(__name__)
logging.root.setLevel(logging.INFO)


class TabAccount(ttk.Frame):
    def __init__(self, bot: OgameBot):
        super().__init__()
        self.bot = bot
        self.auth = Auth()
        self.config = Config()
        self.settings = self.config.get_stored_settings(
            self.bot.empire.universe, self.bot.empire.username
        )
        self.bot.attach_observer(self.notify)

        # User info frame
        self.tab_account_labelframe_user = tk.LabelFrame(
            self, text="User info"
        )
        self.tab_account_labelframe_user.grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.W
        )

        self.label_email = tk.Label(
            self.tab_account_labelframe_user,
            text=f"Email: {self.bot.empire.username}",
        )
        self.label_email.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.label_server_number = tk.Label(
            self.tab_account_labelframe_user,
            text=f"Server number: {self.bot.empire.server_number}",
        )
        self.label_server_number.grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.W
        )

        self.label_server_id = tk.Label(
            self.tab_account_labelframe_user,
            text=f"Server ID: {self.bot.empire.server_id}",
        )
        self.label_server_id.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        self.label_language = tk.Label(
            self.tab_account_labelframe_user,
            text=f"Language: {self.bot.empire.language}",
        )
        self.label_language.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

        self.label_universe = tk.Label(
            self.tab_account_labelframe_user,
            text=f"Universe: {self.bot.empire.universe}",
        )
        self.label_universe.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)

        self.button_logout = tk.Button(
            self.tab_account_labelframe_user,
            text="Logout",
            command=self.logout,
            width=25,
        )
        self.button_logout.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)

        # Bot settings frame
        self.tab_settings_labelframe_user = tk.LabelFrame(
            self, text="Settings"
        )
        self.tab_settings_labelframe_user.grid(
            row=0, column=1, padx=5, pady=5, sticky=tk.W
        )

        self.tab_settings_check_buildres_var = tk.BooleanVar(
            value=self.settings["build_resources"]
        )
        self.tab_settings_check_buildres = tk.Checkbutton(
            self.tab_settings_labelframe_user,
            text="Build resources",
            variable=self.tab_settings_check_buildres_var,
        )
        self.tab_settings_check_buildres.grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.W
        )

        self.tab_settings_check_builddepot_var = tk.BooleanVar(
            value=self.settings["build_deposits"]
        )
        self.tab_settings_check_builddepot = tk.Checkbutton(
            self.tab_settings_labelframe_user,
            text="Build deposits",
            variable=self.tab_settings_check_builddepot_var,
        )
        self.tab_settings_check_builddepot.grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.W
        )

        self.tab_settings_check_buildfac_var = tk.BooleanVar(
            value=self.settings["build_facilities"]
        )
        self.tab_settings_check_buildfac = tk.Checkbutton(
            self.tab_settings_labelframe_user,
            text="Build facilities",
            variable=self.tab_settings_check_buildfac_var,
        )
        self.tab_settings_check_buildfac.grid(
            row=2, column=0, padx=5, pady=5, sticky=tk.W
        )

        self.button_save_settings = tk.Button(
            self.tab_settings_labelframe_user,
            text="Save",
            command=self.save_settings,
            width=25,
        )
        self.button_save_settings.grid(
            row=3, column=0, padx=5, pady=5, sticky=tk.W
        )

        # Bot commands frame
        self.tab_account_labelframe_commands = tk.LabelFrame(self, text="Bot")
        self.tab_account_labelframe_commands.grid(
            row=0, column=3, padx=5, pady=5, sticky=tk.W
        )

        self.label_botstatus = tk.Label(
            self.tab_account_labelframe_commands, text="Status: idle"
        )
        self.label_botstatus.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.button_start = tk.Button(
            self.tab_account_labelframe_commands,
            text="Start",
            command=self.start_bot,
            width=20,
        )
        self.button_start.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

        self.button_stop = tk.Button(
            self.tab_account_labelframe_commands,
            text="Stop",
            command=self.stop_bot,
            width=20,
            state=tk.DISABLED,
        )
        self.button_stop.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)

        # Logs
        self.text_logs = tk.Text(self, height="20", width="80")
        self.text_logs.grid(row=2, column=0, padx=5, pady=5, columnspan=2)

    def notify(self, message: str):
        if self.bot.logout_command:
            return
        self.text_logs.insert(tk.END, message + "\n")
        logging.info(f"Bot: {message}")
        self.update_bot_status()

    def update_bot_status(self):
        bot_status_text = "running"
        if not self.bot.running:
            bot_status_text = "stopped"
        if self.bot.running and self.bot.stop_command:
            bot_status_text = "stopping"
        self.label_botstatus.config(text=f"Status: {bot_status_text}")

    def start_bot(self):
        self.disable_buttons_start_pressed()
        self.text_logs.insert(tk.END, "Starting..." + "\n")
        x = threading.Thread(target=self.bot.start)
        x.start()

    def stop_bot(self):
        if not self.bot.running:
            self.text_logs.insert(tk.END, "The bot is already stopped" + "\n")
        elif self.bot.stop_command:
            self.text_logs.insert(
                tk.END, "The bot is already stopping..." + "\n"
            )
        else:
            self.enable_buttons_stop_pressed()
            self.text_logs.insert(tk.END, "Stopping..." + "\n")
            self.bot.stop()

    def disable_buttons_start_pressed(self):
        # enable stop button
        self.button_stop.config(state=tk.NORMAL)
        # disable all
        self.button_logout.config(state=tk.DISABLED)
        self.tab_settings_check_buildres.config(state=tk.DISABLED)
        self.tab_settings_check_buildfac.config(state=tk.DISABLED)
        self.tab_settings_check_builddepot.config(state=tk.DISABLED)
        self.button_save_settings.config(state=tk.DISABLED)
        self.button_start.config(state=tk.DISABLED)

    def enable_buttons_stop_pressed(self):
        # disable stop button
        self.button_stop.config(state=tk.DISABLED)
        # enable all
        self.button_logout.config(state=tk.NORMAL)
        self.tab_settings_check_buildres.config(state=tk.NORMAL)
        self.tab_settings_check_buildfac.config(state=tk.NORMAL)
        self.tab_settings_check_builddepot.config(state=tk.NORMAL)
        self.button_save_settings.config(state=tk.NORMAL)
        self.button_start.config(state=tk.NORMAL)

    def logout(self):
        # stop notify
        self.bot.logout()
        # stop bot
        self.stop_bot()
        # delete credentials
        self.auth.logout(self.bot)
        # remove tab from gui
        self.pack_forget()
        self.destroy()
        logging.info("Logged out")

    def save_settings(self):
        settings = {
            "build_resources": self.tab_settings_check_buildres_var.get(),
            "build_deposits": self.tab_settings_check_builddepot_var.get(),
            "build_facilities": self.tab_settings_check_buildfac_var.get(),
        }
        self.config.save_settings(
            universe=self.bot.empire.universe,
            username=self.bot.empire.username,
            settings=settings,
        )
        logging.info("Settings saved")
