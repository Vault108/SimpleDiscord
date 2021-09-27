"""
A gui to send webhooks to a specified discord channel.
Written by @Vault108
"""
import tkinter as tk
import sys
import json
from tkinter import Tk
from tkinter import messagebox
from discord_webhook import DiscordWebhook
from loguru import logger
from ratelimit import limits
__version__ = "0.0.7a"


def simple_discord():
    """
    The actual program
    """
    logger.success("Simple Discord Started. Version: " + __version__)

    def bye():
        logger.success("Simple Discord Ended")
        sys.exit()

    def sendawebhok():
        @logger.catch
        @limits(calls=1, period=10)
        def realsend():
            try:
                content = msg.get("1.0", "end")
                url = json.load(open("settings.json"))["webhook"]
                uname = json.load(open("settings.json"))["username"]
                webhook = DiscordWebhook(
                    url=url, username=uname, content=content)
                webhook.timeout = 20
                response = webhook.execute()
                logger.success(response)
            except FileNotFoundError:
                logger.error(
                    "Please check your settings")
                messagebox.showerror(
                    title="No Url or Username set!",
                    message="Please check your settings.")
        msgbody = tk.Tk()
        msgbody.title("Webhook Messssage Input")
        msgbody.configure(bg="#738ADB")
        msgbody.geometry("")
        msg = tk.Text(msgbody, height=10)
        msg.grid(row=2, column=2, padx=5, pady=5)
        tk.Button(msgbody, text="Send", command=realsend,
                  bd="0", bg="#738ADB", fg="white").grid(row=3, column=2)
        tk.Button(msgbody, text="Main Menu", command=msgbody.destroy,
                  bd="0", bg="#738ADB", fg="white").grid(row=4, column=2)
        msgbody.mainloop()

    def settings():
        @logger.catch
        def settingsdump():
            username = usernameinputwindow.get(
                "1.0", "end").strip("\t").strip("\n,.")
            logger.info("Added Username " + username)
            webhook = urlinputwindow.get("1.0", "end").strip("\n")
            logger.info("Added Webhook")
            data = {"webhook": webhook, "username": username}
            with open("settings.json", "w") as json_file:
                json.dump(data, json_file, sort_keys=True, indent=4)
            settings.destroy()
        settings = Tk()
        settings.configure(bg="#738ADB")
        settings.title("Settings")
        settings.resizable(False, False)
        urlinputwindow = tk.Text(settings, height=4)
        urlinputwindow.grid(row=2, column=1, padx=5, pady=5)
        usernameinputwindow = tk.Text(settings, height=1)
        usernameinputwindow.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(
            settings,
            fg="white",
            background="#738ADB",
            text="Username").grid(
            row=0,
            column=0)
        tk.Label(
            settings,
            fg="white",
            background="#738ADB",
            text="Webhook URL").grid(
            row=2,
            column=0)
        tk.Button(
            settings,
            text="Save",
            command=settingsdump,
            bd="0",
            bg="#738ADB",
            width="5",
            fg="white").grid(
            row=4,
            column=1)

        settings.mainloop()

    MainWindow = Tk()
    MainWindow.configure(bg="#738ADB")
    MainWindow.title("Simple Discord " + __version__)
    MainWindow.resizable(False, False)
    tk.Button(MainWindow, text="Send Message", command=sendawebhok,
              bd="0", fg="#ffffff", bg="#738ADB",).grid(row=1, column=1)
    tk.Button(MainWindow, text="Settings", command=settings, width="20",
              bd="0", fg="#ffffff", bg="#738ADB").grid(row=2, column=1)
    tk.Button(MainWindow, text="Exit", command=bye, width="20",
              bd="0", fg="#ffffff", bg="#738ADB",).grid(row=3, column=1)
    tk.Label(MainWindow, text=__version__, fg="#ffffff",
             bg="#738ADB").grid(row=3, column=0)
    MainWindow.mainloop()


logger.add(
    "Logs/{time}.log",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")
simple_discord()
