import nltk
from WikipediaScraper import *
import os
import sys

nltk.download('punkt')  # Download the punkt tokenizer if necessary

from nltk.tokenize import sent_tokenize
from networkx import Graph, pagerank
from rouge import Rouge

def summarize(text, target_rouge=0.5, summary_length=100):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)

    # Initialize the summary with the first sentence of the text
    summary = sentences[0]

    # Initialize the PageRank graph
    graph = Graph()
    graph.add_node(0, weight=1.0)

    # Add nodes and edges for the remaining sentences
    for i, sentence in enumerate(sentences[1:], 1):
        graph.add_node(i, weight=1.0)
        for j in range(i):
            similarity = len(set(sentence.split()) & set(sentences[j].split())) / len(set(sentence.split()) | set(sentences[j].split()))
            graph.add_edge(i, j, weight=similarity)

    # Run the PageRank algorithm to identify the most important sentences
    scores = pagerank(graph, weight='weight')
    ranked_sentences = sorted(((i, scores[i], sentence) for i, sentence in enumerate(sentences)), key=lambda x: -x[1])

    # Add the next most important sentence to the summary until the desired summary length is reached
    while len(summary.split()) < summary_length and ranked_sentences:
        next_sentence = ranked_sentences.pop(0)[2]
        if next_sentence not in summary:
            summary += " " + next_sentence

        # Calculate the ROUGE score and break if the target score is reached
        rouge = Rouge()
        scores = rouge.get_scores(summary, text)
        rouge_score = scores[0]["rouge-1"]["f"]
        if rouge_score >= target_rouge:
            break

    return summary
scrapePage("Calculus")
# Example usage
with open(os.path.join(sys.path[0], "Test.txt"), "r", encoding="utf-8") as f:
    text = f.read()
    summary = summarize(text, target_rouge=0.5, summary_length=100)
    print(summary)
