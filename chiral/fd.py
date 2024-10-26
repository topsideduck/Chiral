import subprocess  # Allows interaction with system processes and command-line tools.
import os  # Provides functions for interacting with the operating system and manipulating file paths.
from typing import TypedDict  # TypedDict lets us define structured dictionaries with specific keys and value types.


class SearchType(TypedDict):
    """
    Specifies the types of filesystem items to search for.

    :cvar file: Set to True to search for regular files.
    :type file: bool
    :cvar directory: Set to True to search for directories.
    :type directory: bool
    :cvar symlink: Set to True to search for symbolic links.
    :type symlink: bool
    """

    file: bool
    directory: bool
    symlink: bool


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

    def search_file(
            self,
            search: str | os.PathLike,
            search_path: str | os.PathLike = os.path.expanduser("~"),
            case_sensitive: bool = False,
            search_type: SearchType | None = None,
    ) -> list[str]:
        """
        Searches for files, directories, or symlinks using the specified search parameters.

        :param search: The search pattern or filename to look for.
        :type search: str | os.PathLike
        :param search_path: The directory to start the search from. Defaults to the user's home directory.
        :type search_path: str | os.PathLike, optional
        :param case_sensitive: If True, the search is case-sensitive; otherwise, it is case-insensitive.
            Defaults to False.
        :type case_sensitive: bool, optional
        :param search_type: A dictionary specifying the types of items to search for (files, directories,
            symlinks). Defaults to searching all types if None.
        :type search_type: SearchType | None, optional
        :return: A list of absolute paths that match the search criteria.
        :rtype: list[str]
        """

        # If no search type is specified, default to searching for files, directories, and symlinks.
        if search_type is None:
            search_type = {
                "file": True,
                "directory": True,
                "symlink": True,
            }

        results: list[str] = []  # Initialize an empty list to store search results.

        # Build the command to execute using the specified search parameters.
        command: list[str] = [
            self.fd_executable,
            "--case-sensitive" if case_sensitive else "--ignore-case",  # Set case-sensitivity based on input.
            "--absolute-path",  # Output absolute paths for search results.
            "-tf" if search_type["file"] else "",  # Include the file flag if searching for files.
            "-td" if search_type["directory"] else "",  # Include the directory flag if searching for directories.
            "-tl" if search_type["symlink"] else "",  # Include the symlink flag if searching for symlinks.
            f"--search-path={search_path}",  # Define the base directory for the search.
            "--color=never",  # Disable color in output for easier processing.
            search  # Add the search term or pattern to the command.
        ]

        # Start the 'fd' command as a subprocess, capturing its output line-by-line.
        find_file = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Process each line of output from the subprocess.
        while True:
            line = find_file.stdout.readline()  # Read the next line of output.
            if not line:  # If no line is returned, the search is complete.
                break

            results.append(line.rstrip())  # Strip trailing newlines and add the result to the list.

        return results  # Return the list of matched paths.
