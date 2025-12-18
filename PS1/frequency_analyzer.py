import re
import pandas as pd
from collections import Counter

class TextAnalyzer:
    """
    Calculates basic text metrics like line count, word count, character count.
    """
    def __init__(self, content):
        self.content = content if content else ""
        # Remove special characters for word analysis, keep for char count? 
        # Requirements say "Remove special characters for analysis", likely for word counting.
        self.clean_text = self._clean_text(self.content)

    def _clean_text(self, text):
        """Removes special characters and lowercases text."""
        # Remove non-alphanumeric characters except spaces
        text = re.sub(r'[^\w\s]', '', text)
        return text.lower()

    def count_lines(self):
        """Counts total lines."""
        if not self.content:
            return 0
        return len(self.content.splitlines())

    def count_words(self):
        """Counts total words."""
        if not self.clean_text:
            return 0
        return len(self.clean_text.split())

    def count_characters(self):
        """Counts total characters (including spaces/punctuation from original)."""
        return len(self.content)

    def count_unique_words(self):
        """Counts unique words."""
        if not self.clean_text:
            return 0
        words = self.clean_text.split()
        return len(set(words))
    
    def avg_word_length(self):
        """Calculates average word length."""
        words = self.clean_text.split()
        if not words:
            return 0
        total_len = sum(len(word) for word in words)
        return round(total_len / len(words), 1)


class WordFrequency:
    """
    Analyzes word frequency using Pandas.
    """
    def __init__(self, content):
        self.content = content if content else ""
        self.words = self._process_text()
        self.df = None

    def _process_text(self):
        """Cleans text and returns list of words."""
        # Reuse cleaning logic or implement similar
        text = re.sub(r'[^\w\s]', '', self.content.lower())
        return text.split()

    def get_frequency_dist(self):
        """Calculates frequency distribution and returns a DataFrame."""
        if not self.words:
            self.df = pd.DataFrame(columns=['Word', 'Frequency'])
            return self.df
        
        counter = Counter(self.words)
        self.df = pd.DataFrame(counter.items(), columns=['Word', 'Frequency'])
        self.df = self.df.sort_values(by='Frequency', ascending=False).reset_index(drop=True)
        return self.df

    def get_top_10(self):
        """Returns top 10 most common words."""
        if self.df is None:
            self.get_frequency_dist()
        return self.df.head(10)

    def filter_words(self, filter_func):
        """Filters words based on a lambda function."""
        if self.df is None:
            self.get_frequency_dist()
        if self.df.empty:
            return self.df
        
        # Apply lambda to 'Word' column
        return self.df[self.df['Word'].apply(filter_func)]
