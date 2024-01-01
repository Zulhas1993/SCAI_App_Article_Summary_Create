import nltk
from newspaper import Article
from docx import Document
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag
import random

def generate_unique_article(summary, user_title_keywords, user_request_keywords, target_word_count=150):
    # Tokenize the summary into sentences
    sentences = sent_tokenize(summary)

    # Perform part-of-speech tagging on each sentence
    tagged_sentences = [pos_tag(word_tokenize(sentence)) for sentence in sentences]

    # Create a new article content by generating sentences with similar parts of speech
    new_article_content = []
    word_count = 0

    while word_count < target_word_count:
        for tagged_sentence in tagged_sentences:
            new_sentence = generate_sentence_with_similar_pos(tagged_sentence, user_title_keywords, user_request_keywords)
            if new_sentence:  # Check if a valid sentence is generated
                new_article_content.append(new_sentence)
                word_count += len(word_tokenize(new_sentence))

    return " ".join(new_article_content)

def generate_sentence_with_similar_pos(tagged_sentence, user_title_keywords, user_request_keywords):
    # Identify nouns, verbs, and adjectives in the sentence
    nouns = [word for word, pos in tagged_sentence if pos.startswith('N') and word.lower() not in user_request_keywords]
    verbs = [word for word, pos in tagged_sentence if pos.startswith('V') and word.lower() not in user_request_keywords]
    adjectives = [word for word, pos in tagged_sentence if pos.startswith('JJ') and word.lower() not in user_request_keywords]

    # Check if any of the lists are non-empty
    if not nouns or not verbs or not adjectives:
        return None

    # Shuffle the order of word categories to create variation
    random.shuffle(nouns)
    random.shuffle(verbs)
    random.shuffle(adjectives)

    # Generate a new sentence with predefined sentence templates
    sentence_templates = [
        "In {}, {}. {} {} {} {}.",
        "While {}, {}. {} {} {} {}.",
        "Exploring {}, {}. {} {} {} {}.",
    ]

    new_sentence_template = random.choice(sentence_templates)
    new_sentence = new_sentence_template.format(
        random.choice(list(user_title_keywords)),
        random.choice(list(user_request_keywords)),
        random.choice(nouns),
        random.choice(verbs),
        random.choice(adjectives),
        random.choice(list(user_request_keywords)),
    )

    return new_sentence


def analyze_and_summarize(article_url, user_title, user_request, output_file="summarized_article.docx", new_article_output_file="new_article.docx"):
    # Download and parse the article
    article = Article(article_url)
    article.download()
    article.parse()

    # Perform natural language processing
    nltk.download('punkt')
    article.nlp()

    # Extract article title, top image, and summary
    title = article.title
    summary = article.summary

    # Extract user interest keywords
    user_title_keywords = set(user_title.lower().split())
    user_request_keywords = set(user_request.lower().split())

    # Check if any user interest keyword is present in both the article title and request
    title_matched = any(keyword in title.lower() for keyword in user_title_keywords)
    request_matched = any(keyword in summary.lower() for keyword in user_request_keywords)

    # Create a Document object for the summary
    doc = Document()

    # Add title to the document
    doc.add_heading(title, level=1)

    # Add user interest information to the document
    doc.add_heading("User Interest Analysis", level=2)
    doc.add_paragraph(f"User Title Keywords: {', '.join(user_title_keywords)}")
    doc.add_paragraph(f"User Request Keywords: {', '.join(user_request_keywords)}")
    doc.add_paragraph(f"Title Matched: {'Yes' if title_matched else 'No'}")
    doc.add_paragraph(f"Request Matched: {'Yes' if request_matched else 'No'}")

    # Add summary to the document
    doc.add_heading("Summary", level=2)
    doc.add_paragraph(summary)

    # Save the document to the specified output file
    doc.save(output_file)
    print(f"The analyzed and summarized article has been saved to '{output_file}'.")

    # Generate a unique article from the dynamic summary
    new_article_content = generate_unique_article(summary, user_title_keywords, user_request_keywords)

    # Create a Document object for the new article
    new_article_doc = Document()

    # Add title to the new article document
    new_article_doc.add_heading(f"Unique Article based on '{title}'", level=1)

    # Add generated content to the new article document
    new_article_doc.add_paragraph(new_article_content)

    # Save the new article document to a separate file
    new_article_doc.save(new_article_output_file)
    print(f"The unique article has been saved to '{new_article_output_file}'.")

if __name__ == "__main__":
    # Example usage: Replace the URL with the one you want to analyze and summarize
    article_url = "https://www.thedailystar.net/news/bangladesh/news/bangladesh-india-joint-water-measurement-padma-ganges-begins-3508056"

    user_title = input("Enter user title: ")
    user_request = input("Enter user request: ")

    analyze_and_summarize(article_url, user_title, user_request)
