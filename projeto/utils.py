from datetime import datetime


def getErrorsObject(errorsContext):
    errorsList = list(errorsContext['errors'])
    errosN = len(errorsList)
    errors = {}

    for i in range(errosN):
        errors[errorsList[i][0]] = errorsList[i][1][0]

    return errors

def compareDates(date1, date2):
    datetime_format = "%Y-%m-%d"

    date1 = datetime.strptime(date1, datetime_format)
    date2 = datetime.strptime(date2, datetime_format)

    return date1 > date2

def forDjango(cls):
    cls.do_not_call_in_templates = True
    return cls