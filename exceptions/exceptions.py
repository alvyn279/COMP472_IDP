class ExceedingSearchPathLengthError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'ExceedingSearchPathLengthError, {0} '.format(self.message)
        else:
            return 'ExceedingSearchPathLengthError: the search path exceeded requirements'
