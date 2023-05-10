import sqlite3 
from constants import DATABASE_NAME, EXPERIENCE_RATE, START_XP
import math

class Experience():
    def __init__(self):
        connection = sqlite3.connect(f'{DATABASE_NAME}.db')
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                    (userid TEXT PRIMARY KEY, xp INTEGER, level INTEGER, messages INTEGER)''')
        connection.close()

    def user_exists(self, userid):
        connection = sqlite3.connect(f'{DATABASE_NAME}.db')
        cursor = connection.cursor()
        cursor.execute("SELECT userid FROM users WHERE userid=?", (userid,))
        exists = cursor.fetchone() is not None
        connection.close()
        return exists

    def add_user_to_db(self, userid, xp=0, level=1, messages=0):
        connection = sqlite3.connect(f'{DATABASE_NAME}.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (userid, xp, level, messages) VALUES (?, ?, ?, ?)", (userid, xp, level, messages))    
        connection.commit()
        connection.commit()

    def level_up(self, userid):
        connection = sqlite3.connect(f'{DATABASE_NAME}.db')
        cursor = connection.cursor()
        cursor.execute(f"SELECT xp, level, messages FROM users WHERE userid = {userid}")
        result = cursor.fetchone()
        new_level = self.level_for_xp(result[0])
        cursor.execute(f"UPDATE users SET xp = {result[0]}, level = {new_level}, messages = {result[2]} WHERE userid = {userid}")  
        connection.commit()
        if new_level != result[1]:
            return new_level
        else:
            return False

    def xp_for_level(self, level):
        return math.ceil(START_XP * math.exp(EXPERIENCE_RATE * level))

    def level_for_xp(self, xp):
        return math.floor(math.log(xp/START_XP) / EXPERIENCE_RATE)
    
    def add_experience(self, userid, xp):
        connection = sqlite3.connect(f'{DATABASE_NAME}.db')
        cursor = connection.cursor()
        cursor.execute(f"SELECT xp, messages FROM users WHERE userid = {userid}")
        result = cursor.fetchone()
        new_xp = result[0] + xp
        cursor.execute(f"UPDATE users SET xp = {new_xp}, messages = {result[1] + 1} WHERE userid = {userid}")
        connection.commit()