from json import JSONEncoder
from .user import User

class UserEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            serializedObj = {
                "access_token": obj.accessToken,
                "user_details": obj.userDetails
            }

            return serializedObj

        # Let the base class default method raise the TypeError
        return JSONEncoder.default(self, obj)