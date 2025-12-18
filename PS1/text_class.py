import os

class TextFile:
    """
    Handles reading text files for analysis.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self._content = None
        self._lines = None

    def read_file(self):
        """
        Reads the file content. Handles FileNotFoundError and different encodings.
        Returns:
            str: The content of the file.
        """
        if not os.path.exists(self.file_path):
            print(f"Error: The file '{self.file_path}' was not found.")
            return None

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self._content = f.read()
            # Reset cursor for lines or re-read? Better to split content
            self._lines = self._content.splitlines()
            print(f"Successfully read file: {self.file_path}")
            return self._content
        except UnicodeDecodeError:
            try:
                # Fallbck to latin-1
                with open(self.file_path, 'r', encoding='latin-1') as f:
                    self._content = f.read()
                self._lines = self._content.splitlines()
                print(f"Successfully read file with latin-1 encoding: {self.file_path}")
                return self._content
            except Exception as e:
                print(f"Error reading file: {e}")
                return None
        except Exception as e:
            print(f"Error accessing file: {e}")
            return None

    def get_lines(self):
        """Returns the file content as a list of lines."""
        if self._lines is None and self._content is None:
             self.read_file()
        if self._lines is None and self._content is not None:
             self._lines = self._content.splitlines()
        return self._lines

    def get_content(self):
        """Returns the full raw content of the file."""
        if self._content is None:
            self.read_file()
        return self._content

