#!/usr/bin/env python3

import tkinter as tk
from threading import Thread
from tkinter import messagebox, ttk

from autonogame.auth import Auth
from autonogame.config import Config
from autonogame.tab_account import TabAccount
from autonogame.version import __version__


class GUI(object):
    def __init__(self):
        self.window = tk.Tk()
        self.window.title(f"autonogame v{__version__}")
        self.window.resizable(False, False)
        self.window_height = 500
        self.window_width = 630
        self.update_window_size()
        self.padx = 15
        self.pady = 15

        self.tab_parent = ttk.Notebook(self.window)
        self.initialize_add_tab()
        self.tab_parent.pack(expand=1, fill="both")

        self.auth = Auth()
        self.config = Config()
        if self.config.exists_account():
            Thread(target=self.load_accounts, args=()).start()

        self.window.bind("<Return>", self.enter_pressed)

        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", on_closing)
        self.window.mainloop()

    def load_accounts(self):
        self.disable_login()
        self.tab_login_label_message_var.set("Loading...")
        self.loaded_accounts = self.auth.load_accounts()
        for loaded_account in self.loaded_accounts:
            self.add_account_tab(loaded_account)
        self.enable_login()
        self.clear_login_form()

    def update_window_size(self):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (self.window_width / 2))
        y_cordinate = int((screen_height / 2) - (self.window_height / 2))
        self.window.geometry(
            "{}x{}+{}+{}".format(
                self.window_width, self.window_height, x_cordinate, y_cordinate
            )
        )

    def disable_login(self):
        self.tab_login_entry_universe.config(state=tk.DISABLED)
        self.tab_login_entry_email.config(state=tk.DISABLED)
        self.tab_login_entry_password.config(state=tk.DISABLED)
        self.tab_login_checkbox_save.config(state=tk.DISABLED)
        self.tab_login_button.config(state=tk.DISABLED)

    def enable_login(self):
        self.tab_login_entry_universe.config(state=tk.NORMAL)
        self.tab_login_entry_email.config(state=tk.NORMAL)
        self.tab_login_entry_password.config(state=tk.NORMAL)
        self.tab_login_checkbox_save.config(state=tk.NORMAL)
        self.tab_login_button.config(state=tk.NORMAL)

    def clear_login_form(self):
        self.tab_login_entry_universe.delete(0, tk.END)
        self.tab_login_entry_email.delete(0, tk.END)
        self.tab_login_entry_password.delete(0, tk.END)
        self.tab_login_label_message_var.set("")

    def enter_pressed(self, event):
        self.login_button()

    def login_button(self):
        self.tab_login_label_message_var.set("")

        account_universe = self.tab_login_entry_universe.get()
        account_email = self.tab_login_entry_email.get()
        account_password = self.tab_login_entry_password.get()

        if not account_universe or not account_email or not account_password:
            self.tab_login_label_message_var.set("All fields are required")
            return

        if self.config.already_logged_in(account_universe, account_email):
            self.tab_login_label_message_var.set("Account already added")

        account_bot = self.auth.login_client(
            account_universe, account_email, account_password
        )
        if account_bot:
            self.add_account_tab(account_bot)
        else:
            self.tab_login_label_message_var.set("Login failed")

    def add_account_tab(self, account_bot):
        new_tab = TabAccount(account_bot)
        self.tab_parent.add(
            new_tab,
            text=account_bot.empire.universe
            + "|"
            + account_bot.empire.username,
        )
        self.tabs_count += 1
        self.update_window_size()
        self.tab_parent.select(self.tabs_count - 1)
        self.clear_login_form()

    def show_logs(self):
        pass

    def initialize_add_tab(self):
        self.tab_add = ttk.Frame(self.tab_parent)

        self.tab_login_labelframe = tk.LabelFrame(
            self.tab_add, text="Add new account"
        )
        self.tab_login_labelframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.tab_login_label_universe = tk.Label(
            self.tab_login_labelframe, text="Universe:"
        )
        self.tab_login_label_universe.grid(
            row=0, column=0, padx=self.padx, pady=self.pady
        )
        self.tab_login_entry_universe = tk.Entry(self.tab_login_labelframe)
        self.tab_login_entry_universe.grid(
            row=0, column=1, padx=self.padx, pady=self.pady
        )

        self.tab_login_label_email = tk.Label(
            self.tab_login_labelframe, text="Email:"
        )
        self.tab_login_label_email.grid(
            row=1, column=0, padx=self.padx, pady=self.pady
        )
        self.tab_login_entry_email = tk.Entry(self.tab_login_labelframe)
        self.tab_login_entry_email.grid(
            row=1, column=1, padx=self.padx, pady=self.pady
        )

        self.tab_login_label_password = tk.Label(
            self.tab_login_labelframe, text="Password:"
        )
        self.tab_login_label_password.grid(
            row=2, column=0, padx=self.padx, pady=self.pady
        )
        self.tab_login_entry_password = tk.Entry(
            self.tab_login_labelframe, show="*"
        )
        self.tab_login_entry_password.grid(
            row=2, column=1, padx=self.padx, pady=self.pady
        )

        self.tab_login_checkbox_save_var = tk.IntVar(value=1)
        self.tab_login_checkbox_save = tk.Checkbutton(
            self.tab_login_labelframe,
            text="Remember account",
            variable=self.tab_login_checkbox_save_var,
        )
        self.tab_login_checkbox_save.grid(row=3, column=0, columnspan=2)

        self.tab_login_button = tk.Button(
            self.tab_login_labelframe,
            text="Login",
            command=self.login_button,
            width=25,
        )
        self.tab_login_button.grid(
            row=4, column=0, columnspan=2, padx=self.padx, pady=self.pady
        )

        self.tab_login_label_message_var = tk.StringVar()
        self.tab_login_label_message = tk.Label(
            self.tab_login_labelframe,
            textvariable=self.tab_login_label_message_var,
        )
        self.tab_login_label_message.grid(
            row=5, column=0, padx=self.padx, pady=self.pady
        )

        self.tab_parent.add(self.tab_add, text="+")
        self.tabs_count = 1


def main():
    GUI()


if __name__ == "__main__":
    main()
