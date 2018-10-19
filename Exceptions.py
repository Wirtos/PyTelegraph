class TelegraphError(Exception):
    def __init__(self, message=''):
        super(TelegraphError, self).__init__()
        message.capitalize()
        self.message = message

    def __str__(self):
        return '{}'.format(self.message)


class ShortNameRequired(TelegraphError):
    pass


class AccessTokenInvalid(TelegraphError):
    pass


class AuthorUrlInvalid(TelegraphError):
    pass


class FieldsFormatInvalid(TelegraphError):
    pass


class PageNotFound(TelegraphError):
    pass


class YearInvalid(TelegraphError):
    pass


class MonthInvalid(TelegraphError):
    pass


class DayMissing(TelegraphError):
    pass


class MonthMissing(TelegraphError):
    pass


class YearMissing(TelegraphError):
    pass


exceptions_raise = {
    'SHORT_NAME_REQUIRED': ShortNameRequired,
    'ACCESS_TOKEN_INVALID': AccessTokenInvalid,
    'FIELDS_FORMAT_INVALID': FieldsFormatInvalid,
    'PAGE_NOT_FOUND': PageNotFound,
    'YEAR_INVALID': YearInvalid,
    'MONTH_INVALID': MonthInvalid,
    'DAY_MISSING': DayMissing,
    'MONTH_MISSING': MonthMissing,
    'YEAR_MISSING': YearMissing,
    'AUTHOR_URL_INVALID': AuthorUrlInvalid

}
