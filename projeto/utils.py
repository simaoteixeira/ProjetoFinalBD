from datetime import datetime

from django.shortcuts import render, redirect

from projeto.enums.USERGROUPS import USERGROUPS


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


def permission_required(*permissions: USERGROUPS):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if request.user.groups.filter(name__in=permissions).exists():
                return view_func(request, *args, **kwargs)
            else:
                return redirect('login')

        return wrap

    return decorator
