class Error(Exception):
    pass

class CannotAuthoriseUser(Error):
    def __init__(self, user):
        self.user = user
        self.message = f'{self.user} could not login'
        super().__init__(self.message)

class ResponseError(Error):
    def __init__(self, status_code):
        self.status_code = status_code
        self.message = f'Request unsuccessful, status code: {status_code}'
        super().__init__(self.message)


class DataHasNullValues(Error):
    pass

class NoDataToLoad(Error):
    pass


class NoValidDataToLoad(Error):
    pass







