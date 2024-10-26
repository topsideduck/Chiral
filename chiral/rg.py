import json  # Provides tools for parsing and generating JSON data, used here to interpret ripgrep's JSON output.
import subprocess  # Allows interaction with system processes and command-line tools.
import os  # Provides functions for interacting with the operating system and manipulating file paths.


class RG:
    """
    A wrapper class for executing file searches using the 'ripgrep' (rg) command-line tool.

    :param rg_executable: The path to the 'rg' executable.
    :type rg_executable: str | os.PathLike
    """

    def __init__(self, rg_executable: str | os.PathLike):
        """
        Initializes the RG object with the path to the 'rg' executable.

        :param rg_executable: The executable path for the 'rg' (ripgrep) search tool.
        :type rg_executable: str | os.PathLike
        """
        self.rg_executable = rg_executable

    @staticmethod
    def process_rg_json(output: list[str]) -> list[dict]:
        """
        Processes a list of JSON-formatted strings output by the ripgrep tool, extracting matches.

        :param output: A list of JSON strings, each containing data about a match or other event.
        :type output: list[str]
        :return: A list of dictionaries, each representing a matched item in the search results.
        :rtype: list[dict]
        """
        results = []

        for result in output:
            data = json.loads(result)  # Parse each JSON string into a dictionary.

            if data['type'] == 'match':  # Only process entries marked as 'match'.
                results.append(data)  # Append each match entry to the results list.

        return results  # Return the list of match entries.

    def search_file(
            self,
            search: str | os.PathLike,
            search_path: str | os.PathLike = os.path.expanduser("~"),
            case_sensitive: bool = False,
            smart_case: bool = False,
            follow_symlinks: bool = False,
            search_hidden: bool = False,
    ) -> list[dict]:
        """
        Searches for files within the specified path using the ripgrep search tool.

        :param search: The search pattern or filename to look for.
        :type search: str | os.PathLike
        :param search_path: The directory to start the search from. Defaults to the user's home directory.
        :type search_path: str | os.PathLike, optional
        :param case_sensitive: If True, the search is case-sensitive; otherwise, it is case-insensitive.
            Defaults to False.
        :type case_sensitive: bool, optional
        :param smart_case: If True, enables smart case matching, which automatically adjusts case-sensitivity
            based on the search term's casing. Defaults to False.
        :type smart_case: bool, optional
        :param follow_symlinks: If True, follows symbolic links during the search. Defaults to False.
        :type follow_symlinks: bool, optional
        :param search_hidden: If True, includes hidden files and directories in the search. Defaults to False.
        :type search_hidden: bool, optional
        :return: A list of strings, each representing a path that matches the search criteria.
        :rtype: list[dict]
        """
        results: list[str] = []

        # Build the command to execute using the specified search parameters.
        command: list[str] = [
            self.rg_executable,
            "--case-sensitive" if case_sensitive else "--ignore-case",
            "--smart-case" if smart_case else None,
            "--follow" if follow_symlinks else None,
            "--hidden" if search_hidden else None,
            "--json",  # Output results in JSON format for easier parsing.
            "--no-stats",  # Suppress statistics to reduce output clutter.
            search,  # Add the search term.
            search_path  # Define the base directory for the search.
        ]

        # Remove any None values from the command list.
        command = [string for string in command if string is not None]

        # Start the 'rg' command as a subprocess, capturing its output line-by-line.
        find_text = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Process each line of output from the subprocess.
        while True:
            line = find_text.stdout.readline()  # Read the next line of output.
            if not line:  # If no line is returned, the search is complete.
                break

            results.append(line.rstrip())  # Strip trailing newlines and add the result to the list.

        # Return the processed JSON results containing matched entries.
        return self.process_rg_json(results)
