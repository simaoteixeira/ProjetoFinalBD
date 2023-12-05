def getErrorsObject(errorsContext):
    errorsList = list(errorsContext['errors'])
    errosN = len(errorsList)
    errors = {}

    for i in range(errosN):
        errors[errorsList[i][0]] = errorsList[i][1][0]

    return errors