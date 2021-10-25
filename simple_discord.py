"""
A gui to send webhooks to a specified discord channel.
Written by @Vault108
"""
import tkinter as tk
import sys
import os
import json
from tkinter import Tk
from tkinter import messagebox
from discord_webhook import DiscordWebhook
from loguru import logger
from ratelimit import limits
__version__ = "0.0.10a"


def simple_discord():
    """
    Main Window
    """
    logger.success("Simple Discord Started. Version: " + __version__)
    main_window = Tk()
    main_window.configure(bg="#738ADB")
    main_window.title("Simple Discord " + __version__)
    main_window.resizable(False, False)
    tk.Button(
        main_window,
        text="Send Message",
        command=sendawebhok,
        bd="0",
        fg="#ffffff",
        bg="#738ADB",).grid(
        row=1,
        column=1)
    tk.Button(
        main_window,
        text="Settings",
        command=settings,
        width="20",
        bd="0",
        fg="#ffffff",
        bg="#738ADB").grid(
        row=2,
        column=1)
    tk.Button(
        main_window,
        text="Exit",
        command=bye,
        width="20",
        bd="0",
        fg="#ffffff",
        bg="#738ADB").grid(
        row=4,
        column=1)
    tk.Label(
        main_window,
        text=__version__,
        fg="#ffffff",
        bg="#738ADB").grid(
        row=1,
        column=0)
    tk.Button(
        main_window,
        text="Delete Logs",
        command=deletelogs,
        bd="0",
        bg="#738ADB",
        width="10",
        fg="white").grid(
        row=3,
        column=1)

    main_window.mainloop()


def deletelogs():
    """
    Clears Logs
    """
    logfolder = "Logs/"
    try:
        for files in os.listdir(logfolder):
            os.remove(os.path.join(logfolder, files))
            logger.info("Deleted " + files)
    except PermissionError:
        pass


def settings():
    """
    The settings.
    """
    @logger.catch
    def settingsdump():
        """
        function to dump settings
        """
        username = usernameinputwindow.get(
            "1.0", "end").strip("\t").strip("\n,.")
        logger.info("Added Username " + username)
        webhook = urlinputwindow.get("1.0", "end").strip("\n")
        logger.info("Added Webhook ")  # Do not log url for webhook
        data = {
            "webhook": webhook,
            "username": username
        }
        with open("settings.json", "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, sort_keys=True, indent=4)
            json_file.close()
        settings_window.destroy()
    settings_window = Tk()
    settings_window.configure(bg="#738ADB")
    settings_window.title("Settings")
    settings_window.resizable(False, False)
    urlinputwindow = tk.Text(
        settings_window,
        height=4)
    urlinputwindow.grid(
        row=2,
        column=1,
        padx=5,
        pady=5)
    usernameinputwindow = tk.Text(
        settings_window,
        height=1)
    usernameinputwindow.grid(
        row=0,
        column=1,
        padx=5,
        pady=5)
    tk.Label(
        settings_window,
        fg="white",
        background="#738ADB",
        text="Username").grid(
        row=0,
        column=0)
    tk.Label(
        settings_window,
        fg="white",
        background="#738ADB",
        text="Webhook URL").grid(
        row=2,
        column=0)
    tk.Button(
        settings_window,
        text="Save",
        command=settingsdump,
        bd="0",
        bg="#738ADB",
        width="5",
        fg="white").grid(
        row=4,
        column=1)
    settings_window.mainloop()


def bye():
    """
    Quits the program
    """
    logger.success("Simple Discord Ended")
    sys.exit()


def sendawebhok():
    """
    Send the web hook
    """
    @logger.catch
    @limits(calls=1, period=10)
    def realsend():
        try:
            content = msg.get("1.0", "end")
            with open("settings.json", encoding="utf-8") as settings_file:
                settingjson = json.load(settings_file)
                url = settingjson["webhook"]
                uname = settingjson["username"]
                settings_file.close()
            webhook = DiscordWebhook(
                url=url,
                username=uname,
                content=content)
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
    msgbody.configure(
        bg="#738ADB")
    msgbody.geometry("")
    msg = tk.Text(
        msgbody,
        height=10)
    msg.grid(
        row=2,
        column=2,
        padx=5,
        pady=5)
    tk.Button(
        msgbody,
        text="Send",
        command=realsend,
        bd="0",
        bg="#738ADB",
        fg="white").grid(
        row=3,
        column=2)
    tk.Button(
        msgbody,
        text="Main Menu",
        command=msgbody.destroy,
        bd="0",
        bg="#738ADB",
        fg="white").grid(
        row=4,
        column=2)
    msgbody.mainloop()


logger.add(
    "Logs/{time}.log",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")

simple_discord()
