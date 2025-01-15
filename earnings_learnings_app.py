from earnings_learnings import Textastic
from sankey import make_sankey
import os

def main():
    textastic = Textastic()

    #Loading stopwords
    stopwords_file = "stopwords.txt"
    if os.path.exists(stopwords_file):
        textastic.load_stop_words(stopwords_file)


    #Loading transcript files
    for filename in os.listdir("."):
        if filename.endswith("_transcript.txt"):
            textastic.load_text(filename)

    #Word Count Sankey diagram
    k = 10  # Number of most common words
    textastic.sankey(k)

    #Sentiment score plots
    sentiment_scores = textastic.process_transcripts_sentiments()
    textastic.plot_transcript_sentiments(sentiment_scores)

    #Word cloud plots
    combined_text = textastic.read_all_transcripts()
    textastic.generate_word_cloud(combined_text)

if __name__ == "__main__":
    main()
