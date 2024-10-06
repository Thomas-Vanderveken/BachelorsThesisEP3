import spacy

# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")

# Example text
text = """
Apple is looking at buying U.K. startup for $1 billion. Microsoft is also interested in acquiring tech companies.
The startup, located in London, specializes in artificial intelligence and machine learning.
"""

# Process the text with SpaCy
doc = nlp(text)

# Extract named entities
entities = [(ent.text, ent.label_) for ent in doc.ents]

# Print out the named entities
print("Named Entities, Phrases, and Concepts:")
for entity in entities:
    print(f"{entity[0]} ({entity[1]})")

# Keyword Matching Example
keywords = ["Apple", "Microsoft", "startup", "artificial intelligence", "machine learning"]

print("\nMatching Keywords:")
for token in doc:
    if token.text in keywords:
        print(f"Found keyword: {token.text}")

# Example of simple information retrieval
# Find sentences mentioning "startup"
print("\nSentences mentioning 'startup':")
for sent in doc.sents:
    if "startup" in sent.text:
        print(sent.text)
