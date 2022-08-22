import requests as rq

class User():
    def __init__(self, accessToken) -> None:
        self.__accessToken = accessToken
        self.__userDetails = self.getLoggedUserInfo()

    @property
    def accessToken(self):
        return self.__accessToken

    @property
    def userDetails(self):
        return self.__userDetails

    def getLoggedUserInfo(self):
        '''
        Gets the authenticated user's public and private information
        '''
        url = "https://api.github.com/user"
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {self.accessToken}"
        }

        # Make call to User information endpoint with authenticated header
        request = rq.get(url, headers=headers)

        # Return JSON info
        return request.json()
