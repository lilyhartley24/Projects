from sankey import make_sankey
from collections import defaultdict, Counter
import pandas as pd
import random as rnd
import matplotlib.pyplot as plt
import re
import os
import numpy as np
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from wordcloud import WordCloud

class Textastic:

    def __init__(self):
        """ Constructor
        datakey --> (filelabel --> datavalue)
        """
        self.data = defaultdict(dict)


    def default_parser(self, filename):
        """ Parse raw text and produce
        extracted data results in the form of a dictionary. """
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()

        # clean text, remove punctuation, make everything lowercase
        text = re.sub(r'[^\w\s]', '', text.lower())

        words = text.split()
        results = {
            'wordcount': Counter(words),
            'numwords': len(words)
        }
        return results



    def load_text(self, filename, label=None, parser=None):
        """ Register a document with the framework.
        Extract and store data to be used later by
        the visualizations """

        if parser is None:
            results = self.default_parser(filename)
        else:
            results = parser(filename)

        if label is None:
            label = filename

        for k, v in results.items():
            self.data[k][label] = v


    def load_stop_words(self, stopwords_file):
        """ Load a list of stopwords from a file. """
        with open(stopwords_file, 'r') as f:
            self.stopwords = set(f.read().splitlines())


    def preprocesser(self, filename):
        """ remove stop words """
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()

        # Tokenize the text into words
        words = text.split()

        # Remove stop words and normalize text (lowercase)
        processed_words = [word.lower() for word in words if word.lower() not in self.stopwords]

        # Rejoin the cleaned words into a string
        cleaned_text = ' '.join(processed_words)

        return cleaned_text

    def calculate_sentiments(self, text):
        """
        Calculate the sentiment of a given text related to work.
        """
        #initializing sentiment score analysis
        sia = SentimentIntensityAnalyzer()
        return sia.polarity_scores(text)

    #creates a dictionary of all sentiment scores for the sentiment score visualization
    def process_transcripts_sentiments(self):
        """
        Process all .txt files in the current working directory and calculate sentiment scores.
        """
        file_sentiments = {}
        for filename in os.listdir("."):
            if filename.endswith("_transcript.txt"):  #Processing only transcript files
                with open(filename, 'r', encoding='utf-8') as file:
                    text = file.read()
                    sentiment_scores = self.calculate_sentiments(text)
                    file_sentiments[filename] = sentiment_scores
        return file_sentiments

    #for the wordcloud
    def read_all_transcripts(self):
        """
        Reads all transcript files and combine the text into a single string.
        """
        combined_text = ""
        for filename in os.listdir("."):
            if filename.endswith("_transcript.txt"):  # Process only transcript files
                with open(filename, 'r', encoding='utf-8') as file:
                    combined_text += file.read() + " "
        return combined_text


    def sankey(self, k, set=None):
        """ Map each text to words using a Sankey diagram, where the thickness of the line is the number of times that
          word occurs in the text. List of words are the k most common words across each text file (excluding stopwords)."""

        word_counts = defaultdict(Counter)
        for label, words in self.data['wordcount'].items():
            # Filter out stopwords
            filtered_words = {word: count for word, count in words.items() if word not in self.stopwords}
            word_counts[label] = Counter(filtered_words)

        # Determine the words to include in the diagram
        if set:
            selected_words = set
        else:
            # Get the top k most common words across all texts
            combined_counts = Counter()
            for counts in word_counts.values():
                combined_counts.update(counts)
            selected_words = {word for word, _ in combined_counts.most_common(k)}

        # Prepare data for the Sankey diagram
        data = {
            "Source": [],
            "Target": [],
            "Value": []
        }

        for text_label, counts in word_counts.items():
            for word in selected_words:
                if word in counts:
                    data["Source"].append(text_label)
                    data["Target"].append(word)
                    data["Value"].append(counts[word])

        # Create a DataFrame for the Sankey diagram
        df = pd.DataFrame(data)

        # Generate the Sankey diagram using the `make_sankey` function
        make_sankey(df, src="Source", targ="Target", vals="Value")


    #visualization two: plotting sentiment scores with each file as its own subplot
    def plot_transcript_sentiments(self, sentiment_files):
        """
        Plot sentiment scores for each earnings call transcript in subplots.
        """
        num_files = len(sentiment_files)
        fig, axes = plt.subplots(num_files, 1, figsize=(12, 6 * num_files), sharex=True)

        # Ensure `axes` is always iterable
        if num_files == 1:
            axes = [axes]

        # Plot each transcript's sentiment scores
        for i, (filename, scores) in enumerate(sentiment_files.items()):
            ax = axes[i]
            sentiments = ['Positive', 'Neutral', 'Negative']
            values = [scores['pos'], scores['neu'], scores['neg']]

            ax.bar(sentiments, values, color=['green', 'blue', 'red'])
            ax.set_title(f"Sentiment Scores for {filename}")
            ax.set_ylabel("Scores")
            ax.set_ylim(0, 1)  # VADER scores are between 0 and 1
            ax.grid(axis='y')

        plt.xlabel("Sentiment Categories")
        plt.tight_layout()
        plt.show()

    #generates a wordcloud for all earnings
    def generate_word_cloud(self, text, output_file=None):
        """
        Generates and displays a word cloud for all earnings .
        """
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            colormap='viridis',
            max_words=200,
        ).generate(text)

        # Plot the word cloud
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title("Word Cloud of Earnings Call Transcripts")
        plt.show()

