import requests as rq
import json
from psycopg2 import sql
from datetime import date

from config.db import connection

# This is a list of all database fields that don't have their date come from Github
DATABASE_FIELD_LIST = ["registration_date"]


class User():
    def __init__(self, accessToken) -> None:
        self.__accessToken = accessToken
        self.__userDetails = {}

        self.getGithubInfo()

    @property
    def accessToken(self):
        return self.__accessToken

    @property
    def userDetails(self):
        '''
        Returns the Github user details

        Dict{
            id: The github user id
            email: The github user email
            name: The github name
            login: The github handle
            avatar_url: The URL to the user's gravatar
        }
        '''
        return self.__userDetails

    def __eq__(self, other):
        if isinstance(other, User):
            return self.__userDetails["id"] == other.__userDetails["id"]

        return False

    def toDict(self):
        userDict = {
            "access_token": self.__accessToken,
            "user_details": self.__userDetails
        }

        return userDict

    def getGithubInfo(self):
        '''
        Gets the authenticated user's public and private information from Github
        '''
        url = "https://api.github.com/user"
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {self.accessToken}"
        }

        # Make call to User information endpoint with authenticated header
        request = rq.get(url, headers=headers)
        request.raise_for_status()

        # Return JSON info
        self.__userDetails.update(json.loads(request.text))

        return True

    def getUserDatabaseInfo(self):
        selectQuery = sql.SQL("SELECT {fields} FROM player WHERE github_user_id = {id} LIMIT 1").format(
            fields=sql.SQL(", ").join(map(sql.Identifier, DATABASE_FIELD_LIST)),
            id=sql.Literal(self.__userDetails["id"])
        )

        # Get a connection and a cursor from the pool
        cursor = connection.cursor()

        # Execute
        cursor.execute(selectQuery)
        data = cursor.fetchone()

        # Close the cursor and give the connection back to the pool
        cursor.close()

        # Commit changes
        connection.commit()

        if data is not None:
            print(data)
            self.__userDetails.update(data)

    def insertUser(self):
        # Prepare our insert query
        insertQuery = sql.SQL('''INSERT INTO player (github_user_id, email, name, login, avatar_url, registration_date)
            VALUES ({gh_id}, {email}, {name}, {login}, {avatar_url}, {reg_date}) ON CONFLICT DO NOTHING''').format(
            gh_id=sql.Literal(self.__userDetails["id"]),
            email=sql.Literal(self.__userDetails["email"]),
            name=sql.Literal(self.__userDetails["name"]),
            login=sql.Literal(self.__userDetails["login"]),
            avatar_url=sql.Literal(self.__userDetails["avatar_url"]),
            reg_date=sql.Literal(date.today())
        )

        # Get a connection from the pool and execute
        cursor = connection.cursor()

        # Else, insert him
        cursor.execute(insertQuery)

        # Close the cursor and give the connection back to the pool
        cursor.close()

        # Commit changes
        connection.commit()

    @staticmethod
    def isCurrentLoggedIn(username, session):
        if "users" in session.keys():
            return username == session["user"]["user_details"]["login"]
        else:
            return False

    @staticmethod
    def getUserInfoByLogin(login):
        # Get data query
        dataQuery = sql.SQL("SELECT * FROM player WHERE login = {user_login} LIMIT 1").format(
            user_login=sql.Literal(login)
        )

        # Get connection and cursor from pool
        cursor = connection.cursor()

        # Get data from database
        cursor.execute(dataQuery)
        data = cursor.fetchone()

        # Close cursor and give connection back
        cursor.close()

        # Commit changes
        connection.commit()

        # TODO: CONVERT RESULT TO DICT
        # Return a "user_details" dict containing name, profile, avatar, etc
        return data
