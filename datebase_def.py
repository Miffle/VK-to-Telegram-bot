import sqlite3


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
    sub = cursor.execute("SELECT subscrition FROM Users WHERE user_id = ?", (tgid,))
    return bool(sub)


def api_check(tgid):
    connection = sqlite3.connect('identifier.sqlite')
    cursor = connection.cursor()
    api = cursor.execute("SELECT VK_api FROM Users WHERE user_id = ?", (tgid,)).fetchall()
    return api[0]
