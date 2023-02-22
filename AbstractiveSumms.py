import os
import sys
from transformers import pipeline

def generate_summary(text, max_length=50):
    # Load the summarization pipeline
    summarizer = pipeline("summarization")

    # Generate the summary using the pipeline
    summary = summarizer(text, max_length=max_length)[0]['summary_text']
    
    return summary

with open(os.path.join(sys.path[0], "Test.txt"), 'r') as file:
    text = file.read()
print(generate_summary(text, 100))
