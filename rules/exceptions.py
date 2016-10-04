# coding: utf-8
class BaseRulesError(Exception):
    pass


class ValidateError(BaseRulesError):
    pass


class NotSetError(BaseRulesError):
    pass