import base64
from typing import TypeVar
from models.user import User
from api.v1.auth.auth import Auth

class BasicAuth(Auth):
    """ Basic Authentication """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ Extracts the Base64 string from the Authorization header """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """ Decodes the Base64 string to get the credentials """
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header).decode('utf-8')
            return decoded
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """ Extracts user credentials (email, password) from the decoded base64 string """
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return decoded_base64_authorization_header.split(":", 1)

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Returns a User object from the email and password """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        user = User.search({"email": user_email})
        if not user:
            return None
        user = user[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns the current user object for the request """
        header = self.authorization_header(request)
        if header is None:
            return None
        base64_str = self.extract_base64_authorization_header(header)
        if base64_str is None:
            return None
        decoded_str = self.decode_base64_authorization_header(base64_str)
        if decoded_str is None:
            return None
        email, password = self.extract_user_credentials(decoded_str)
        if email is None or password is None:
            return None
        return self.user_object_from_credentials(email, password)
