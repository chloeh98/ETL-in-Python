class Error(Exception):
    pass

class CannotAuthoriseUser(Error):
    def __init__(self, user):
        self.user = user
        self.message = f'{self.user} could not login'
        super().__init__(self.message)

class AccessTokenNotAuthorised(Error):
    def __init__(self, status_code):
        self.status_code = status_code
        self.message = f'unable to get access token, status code: {status_code}'
        super().__init__(self.message)

class NotLoginPage(Error):
    pass






