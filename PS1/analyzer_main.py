
import os
import time
import pandas as pd
import matplotlib.pyplot as plt
from text_class import TextFile
from frequency_analyzer import TextAnalyzer, WordFrequency

# Decorator for status messages
def analysis_logger(func):
    def wrapper(*args, **kwargs):
        print(f"--- Starting {func.__name__.replace('_', ' ').title()} ---")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"--- Completed in {end_time - start_time:.4f} seconds ---\n")
        return result
    return wrapper

class Report:
    """
    Generates summaries and saves reports.
    """
    def __init__(self, filename, analyzer, word_freq):
        self.filename = filename
        self.analyzer = analyzer
        self.word_freq = word_freq

    def generate_text_report(self, output_file="analysis_report.txt"):
        """Generates a text report with statistics."""
        top_10 = self.word_freq.get_top_10()
        
        # Calculate derived metrics
        lines = self.analyzer.count_lines()
        words = self.analyzer.count_words()
        avg_words_per_line = round(words / lines, 1) if lines > 0 else 0
        chars = self.analyzer.count_characters()
        chars_per_line = round(chars / lines, 1) if lines > 0 else 0

        report_content = f"""TEXT FILE ANALYZER
File: {os.path.basename(self.filename)}

STATISTICS:
Total Lines: {lines}
Total Words: {words}
Total Characters: {chars}
Unique Words: {self.analyzer.count_unique_words()}
Average Word Length: {self.analyzer.avg_word_length()} characters

ANALYSIS:
Lines per page: {lines} (Assumed 1 page for single file context, or N/A)
Words per line: {avg_words_per_line}
Characters per line: {chars_per_line}

TOP 10 MOST COMMON WORDS:
"""
        rank = 1
        for index, row in top_10.iterrows():
            report_content += f"{rank}. {row['Word']} - {row['Frequency']} occurrences\n"
            rank += 1
            
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_content)
            print(f"Report saved to: {output_file}")
            print(report_content)
        except Exception as e:
            print(f"Error saving report: {e}")

    def save_frequency_csv(self, output_file="word_frequency.csv"):
        """Saves word frequency data to CSV."""
        df = self.word_freq.get_frequency_dist()
        try:
            df.to_csv(output_file, index=False)
            print(f"Word frequency data saved to: {output_file}")
        except Exception as e:
            print(f"Error saving CSV: {e}")

    def generate_chart(self, output_file="top_10_words.png"):
        """Generates a bar chart for top 10 words."""
        top_10 = self.word_freq.get_top_10()
        if top_10.empty:
            print("No data to plot.")
            return

        plt.figure(figsize=(10, 6))
        plt.bar(top_10['Word'], top_10['Frequency'], color='skyblue')
        plt.xlabel('Words')
        plt.ylabel('Frequency')
        plt.title('Top 10 Most Common Words')
        plt.xticks(rotation=45)
        plt.tight_layout()
        try:
            plt.savefig(output_file)
            print(f"Chart saved to: {output_file}")
            # plt.show() # Uncomment if interactive mode is feasible, but for script usually savefig is safer
        except Exception as e:
            print(f"Error saving chart: {e}")
        finally:
            plt.close()

@analysis_logger
def main():
    # Input file path
    file_path = input("Enter the path to the text file (default: sample_text.txt): ").strip()
    if not file_path:
        file_path = "sample_text.txt"

    # 1. File Handling
    text_file = TextFile(file_path)
    content = text_file.read_file()
    
    if content is None:
        return

    # 2. Text Analysis
    analyzer = TextAnalyzer(content)
    
    # 3. Word Frequency
    word_freq = WordFrequency(content)
    
    # Example of lambda filtering (Automation Feature)
    # Filter words longer than 3 characters
    long_words = word_freq.filter_words(lambda x: len(str(x)) > 3)
    # Just printing count to show usage
    print(f"Words longer than 3 chars: {len(long_words)}")

    # 4. Reporting
    report = Report(file_path, analyzer, word_freq)
    report.generate_text_report()
    report.save_frequency_csv()
    report.generate_chart()

if __name__ == "__main__":
    main()
