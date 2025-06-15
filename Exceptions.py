class DataLoadError(Exception):
    """
    Custom exception raised when there is an issue loading data into the database.
    """
    pass

class FunctionMappingError(Exception):
    """
    Custom exception raised when a test data point cannot be mapped to any ideal function.
    """
    pass
