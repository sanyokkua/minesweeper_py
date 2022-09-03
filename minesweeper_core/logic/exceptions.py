""" """


class IncorrectCoordinatesException(Exception):
    """ """

    def __init__(self, message: str) -> None:
        """_summary_

        Args:
            message (str): _description_
        """
        Exception.__init__(self, message)
