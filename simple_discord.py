"""
A gui to send webhooks to a specified discord channel.
Written by @Vault108
"""
import tkinter as tk
import sys
import os
import json
import webbrowser
from tkinter import Tk
from tkinter import messagebox
from tkinter import Menu
from discord_webhook import DiscordWebhook
from loguru import logger
from ratelimit import limits
__version__ = "0.0.14a"


def simple_discord():
    """
    Main Window
    """
    logger.success("Simple Discord Started. Version: " + __version__)
    main_window = Tk()
    main_window.title("Simple Discord ")
    main_window.resizable(False, False)
    main_menu = Menu(main_window)
    main_filemenu = Menu(main_menu, tearoff=0,
                         bd=0, activebackground="#738ADB")
    main_filemenu.add_command(label="Settings", command=settings)
    main_filemenu.add_command(label="Delete Logs", command=deletelogs)
    main_filemenu.add_command(label="Exit", command=bye)
    main_menu.add_cascade(label="Edit", menu=main_filemenu)
    main_window.configure(bg="#738ADB", menu=main_menu)
    about_menu = Menu(main_window, tearoff=0,
                      bd=0, activebackground="#738ADB")
    about_menu.add_command(label="About", command=about)
    about_menu.add_command(label="Support", command=bug)
    main_menu.add_cascade(label="Help", menu=about_menu)
    tk.Button(
        main_window,
        text="Send Message",
        command=sendawebhok,
        highlightthickness=0,
        width=20,
        bd="0",
        fg="#ffffff",
        bg="#738ADB",).grid(
        row=1,
        column=1)
    tk.Button(
        main_window,
        text="Settings",
        command=settings,
        highlightthickness=0,
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
        highlightthickness=0,
        width="20",
        bd="0",
        fg="#ffffff",
        bg="#738ADB").grid(
        row=4,
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
        Function to dump settings
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
        highlightthickness=0,
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
        """
        Actual sending of the webhook.
        """
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
        highlightthickness=0,
        bd="0",
        bg="#738ADB",
        fg="white").grid(
        row=3,
        column=2)
    tk.Button(
        msgbody,
        text="Main Menu",
        command=msgbody.destroy,
        highlightthickness=0,
        bd="0",
        bg="#738ADB",
        fg="white").grid(
        row=4,
        column=2)
    msgbody.mainloop()


def about():
    """
    The about window
    """
    about_window = Tk()
    about_window.title("About ")
    about_window.configure(bg="#738ADB")
    about_window.resizable(False, False)
    tk.Label(about_window, bg="#738ADB",
             text="Version: " + __version__).grid(row=1, column=1)
    tk.Label(about_window, bg="#738ADB",
             text="Written by: Vault108").grid(row=2, column=1)
    tk.Label(about_window, bg="#738ADB",
             text="License: GNU GPL V3 ").grid(row=3, column=1)
    about_window.mainloop()


def bug():
    """
    Something not working right? Have a question? Need some help?
    This function will help you open an issue on github.
    """
    webbrowser.open_new(
        "https://github.com/Vault108/SimpleDiscord/issues/new/choose?")


logger.add(
    "Logs/{time}.log",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")


if __name__ == "__main__":
    simple_discord()
