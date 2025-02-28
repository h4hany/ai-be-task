from langdetect import detect
from textblob import TextBlob
import spacy
import re

class TextAnalysisService:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def clean_gutenberg_text(self, text: str) -> str:
        """Remove Gutenberg header and footer, and clean the text."""
        # Find the start of the actual content
        start_markers = [
            "*** START OF THE PROJECT GUTENBERG",
            "*** START OF THIS PROJECT GUTENBERG",
            "*END*THE SMALL PRINT",
            "MY FRIEND DOGGIE",  # Add the actual title as a start marker
        ]
        end_markers = [
            "*** END OF THE PROJECT GUTENBERG",
            "*** END OF THIS PROJECT GUTENBERG",
            "End of the Project Gutenberg",
        ]

        # Remove transcriber's note
        text = re.sub(r"Transcriber's Note.*?(?=MY FRIEND DOGGIE)", "", text, flags=re.DOTALL)

        # Find the start of the actual content
        start_pos = 0
        for marker in start_markers:
            pos = text.find(marker)
            if pos != -1:
                start_pos = text.find("\n", pos) + 1
                break

        # Find the end of the actual content
        end_pos = len(text)
        for marker in end_markers:
            pos = text.find(marker)
            if pos != -1:
                end_pos = pos
                break

        # Extract the main content
        content = text[start_pos:end_pos].strip()

        # Clean up the text
        content = re.sub(r'\r\n', '\n', content)  # Normalize line endings
        content = re.sub(r'\n{3,}', '\n\n', content)  # Remove excessive newlines
        content = re.sub(r'_', '', content)  # Remove underscores used for italics
        content = re.sub(r'\s+', ' ', content)  # Normalize whitespace
        
        # Remove any remaining metadata or title pages
        content = re.sub(r'^(MY FRIEND DOGGIE|or|AN ONLY CHILD)[\s\n]*', '', content)
        
        return content.strip()

    def get_summary(self, text: str, num_sentences: int = 5) -> str:
        """Generate a summary of the text."""
        # Use spaCy for better sentence splitting
        doc = self.nlp(text[:20000])  # Increased limit for better context
        
        # Get all sentences
        sentences = list(doc.sents)
        
        # Filter out short sentences and those that might be part of formatting
        valid_sentences = [
            sent.text.strip() 
            for sent in sentences 
            if len(sent.text.strip()) > 30  # Minimum length for a valid sentence
            and not any(marker in sent.text for marker in ["Chapter", "CHAPTER", "* * *"])
        ]
        
        # Get the first few valid sentences for the summary
        summary = ' '.join(valid_sentences[:num_sentences])
        return summary

    def get_key_characters(self, text: str, max_chars: int = 10) -> list:
        """Extract key characters from the text."""
        doc = self.nlp(text[:50000])  # Increased limit for better character detection
        
        # Count person entities
        person_counts = {}
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                name = ent.text.strip()
                # Filter out common false positives and metadata
                if not any(x in name for x in ["Note", "Transcriber", "Chapter", "CHAPTER"]):
                    person_counts[name] = person_counts.get(name, 0) + 1
        
        # Sort by frequency and get top characters
        characters = sorted(person_counts.items(), key=lambda x: x[1], reverse=True)
        return [char[0] for char in characters[:max_chars]]

    def analyze_text(self, text: str):
        # Clean the text first
        cleaned_text = self.clean_gutenberg_text(text)

        # Language detection
        try:
            language = detect(cleaned_text)
        except:
            language = "unknown"

        # Sentiment analysis
        blob = TextBlob(cleaned_text)
        sentiment = blob.sentiment.polarity

        # Get key characters
        characters = self.get_key_characters(cleaned_text)

        # Generate summary
        summary = self.get_summary(cleaned_text)

        return {
            "language": language,
            "sentiment": sentiment,
            "key_characters": characters,
            "summary": summary
        } 