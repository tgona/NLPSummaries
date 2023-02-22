import wikipedia
import os
import sys
def scrapePage(title):
    # Set the Wikipedia language and the article title
    wikipedia.set_lang("en")
    article_title = title

    # Download the text of the article
    text = wikipedia.page(article_title).content

    # Save the text to a file
    with open(os.path.join(sys.path[0], "Test.txt"), "w", encoding="utf-8") as f:
        f.write(text)