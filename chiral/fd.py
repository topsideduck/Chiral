import os  # Provides functions for interacting with the operating system and manipulating file paths.


class FD:
    """
    A wrapper class for executing searches using the 'fd-find' command-line tool.

    :param fd_executable: The path to the 'fd' executable.
    :type fd_executable: str | os.PathLike
    """

    def __init__(self, fd_executable: str | os.PathLike):
        """
        Initializes the FD object with the path to the 'fd' executable.

        :param fd_executable: The executable path for the 'fd' search tool.
        :type fd_executable: str | os.PathLike
        """

        self.fd_executable = fd_executable  # Store the path to the 'fd' command-line tool.

