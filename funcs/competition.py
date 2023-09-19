class Competition():
    def __init__(self) -> None:
        self.__competitionInfo = self.getInfo()
        self.__userScore = self.getUserScoreByName(self.__competitionID["login"])

    @property
    def competitionInfo(self):
        return self.__competitionInfo

    @property
    def userScore(self):
        return self.__userScore

    def __eq__(self, other):
        if isinstance(other, Competition):
            return self.__competitionInfo["id"] == other.__competitionInfo["id"]

        return False

    def toDict(self):
        userDict = {
            "competition_info": self.__competitionInfo,
            "user_score": self.__userScore
        }

        return userDict

    @staticmethod
    def getUserScoreByName(username):
        ...
        # Query the database for an user with that name, return error if not found
        # Get data from database
        # Return a "user_score"
        return {"competitions": [
            {
                "id": 1,
                "name": "Test Competition",
                "score": 400
            }
        ]}
