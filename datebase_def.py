import sqlite3
import threading

import auto_check_new_message


def add_on_start(userid):
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    result = cursor.execute('SELECT * FROM `Users` WHERE `user_id` = ?', (userid,)).fetchall()
    if not bool(len(result)):
        cursor.execute("INSERT INTO `Users` VALUES(?, ?, ?);", (userid, False, 0))
    connection.commit()
    connection.close()


def insert_in_db(userid, vk_user_api):
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    result = cursor.execute('SELECT * FROM `Users` WHERE `user_id` = ?', (userid,)).fetchall()
    if not bool(len(result)):
        cursor.execute("INSERT INTO `Users` VALUES(?, ?, ?);", (userid, True, vk_user_api))
    else:
        subscribe(userid, vk_user_api)
    connection.commit()
    connection.close()


def subscribe(userid, vk_user_api):
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    cursor.execute("UPDATE `Users` SET `subscrition` = ? WHERE `user_id` = ?", (True, userid))
    cursor.execute("UPDATE `Users` SET `VK_api` = ? WHERE `user_id` = ?", (vk_user_api, userid))
    connection.commit()
    connection.close()


def unsubscribe(userid):
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    cursor.execute("UPDATE `Users` SET `subscrition` = ? WHERE `user_id` = ?", (False, userid))
    connection.commit()
    connection.close()


def sub_check(tgid):
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    sub = cursor.execute("SELECT subscrition FROM Users WHERE user_id = ?", (tgid,)).fetchall()
    connection.close()
    return bool(sub[0][0])


def api_check(tgid):
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    api = cursor.execute("SELECT VK_api FROM Users WHERE user_id = ?", (tgid,)).fetchall()
    connection.close()
    return api[0]


def renew_polling_threads(bot):
    connection = sqlite3.connect('identifier.sqlite')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    users = cursor.execute("SELECT * FROM Users").fetchall()
    for user_row in users:
        api_key = user_row["VK_api"]
        user_id = user_row["user_id"]
        if user_row["subscrition"]:
            threading.Thread(target=auto_check_new_message.new_message, args=(api_key, user_id, bot)).start()
    connection.close()
