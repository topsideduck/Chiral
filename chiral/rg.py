import os  # Provides functions for interacting with the operating system and manipulating file paths.


class RG:
    """
    A wrapper class for executing searches using the 'ripgrep' command-line tool.

    :param rg_executable: The path to the 'rg' executable.
    :type rg_executable: str | os.PathLike
    """

    def __init__(self, rg_executable: str | os.PathLike):
        """
        Initializes the RG object with the path to the 'rg' executable.

        :param rg_executable: The executable path for the 'rg' search tool.
        :type rg_executable: str | os.PathLike
        """

        self.rg_executable = rg_executable  # Store the path to the 'fd' command-line tool.
