import hashlib
import random
import motor


class DatabaseConnection():
    db = None

    def __init__(self):
        if self.db is None:
            self.db = motor.motor_tornado.MotorClient('localhost', 27017).test

    async def get_user(self, email):
        user = await self.db.users.find_one({'email': email})
        print(user)
        return user

    def create_user(self, email, name, password):
        return self.db.users.insert(
            {
                'email': email,
                'name': name,
                'password': hashlib.sha256(str.encode(password)).hexdigest()
            }
        )

    async def update_user(self, email, key, value):
        return await self.db.users.update({'email': email}, {'$set': {key: value}})

    def add_reading(self, language, level, text, questions, answers):
        return self.db.readings.insert(
            {
                'language': language,
                'level': level,
                'text': text,
                'questions': questions,
                'answers': answers
            }
        )

    async def get_reading(self, language, level):
        cursor = self.db.readings.find({'language': language, 'level': level})
        readings = await cursor.to_list(None)
        if len(readings) > 0:
            return random.choice(readings)
        else:
            return None

    def add_alphabet(self, language, alphabet):
        return self.db.readings.insert(
            {
                'language': language,
                'alphabet': alphabet
            }
        )

    async def get_alphabet(self, language):
        alphabet = await self.db.readings.find_one({'language': language})
        return alphabet

    async def update_game_score(self, email, game, language, score, increment=True):
        user = await self.get_user(email)
        if game in user:
            if language in user[game] and increment:
                return await self.db.users.update({'email': email}, {'$inc': {game+"."+language: score}})
            else:
                return await self.db.users.update({'email': email}, {'$set': {game + "." + language: score}})
        else:
            return await self.db.users.update({'email': email}, {'$set': {game: {language: score}}})