class Error(Exception):
    pass

class CannotAuthorise(Error):
    def __init__(self, user):
        self.user = user
        self.message = f'{user} could not login'
        super().__init__(self.message)





