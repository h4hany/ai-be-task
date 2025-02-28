import os
import groq
import re


class GroqService:
    def __init__(self):
        self.client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))

    def analyze_book(self, book_content: str):
        """Handle the prompt to so later i can split them into my structure character analysis, sentiment analysis, language detection, and plot summarization."""

        book_excerpt = book_content[:3000]  # Limit input

        prompt = f"""
        You are an AI book analyzer. Analyze the following book content and return a structured response.
        Respond in the following format:

        Key Characters:
        - Character 1
        - Character 2

        Sentiment Analysis:
        - Sentiment 1
        - Sentiment 2

        Language Detection:
        - Language

        Plot Summary:
        - Summary Point 1
        - Summary Point 2

        Book Content:
        {book_excerpt}
        """

        response = self.client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "system", "content": prompt}],
        )

        # Extract response and format as structured JSON
        raw_text = response.choices[0].message.content
        return self.parse_analysis(raw_text)

    def parse_analysis(self, text: str):
        """Parses Groq's response into a structured dictionary."""

        sections = {
            "characters": [],
            "sentiment": [],
            "language": "",
            "plot_summary": []
        }

        # Extracting Key Characters
        match = re.search(r"Key Characters:\n(.*?)(?=\n\n|$)", text, re.DOTALL)
        if match:
            sections["characters"] = [line.strip("- ").strip() for line in match.group(1).split("\n") if line.strip()]

        # Extracting Sentiment Analysis
        match = re.search(r"Sentiment Analysis:\n(.*?)(?=\n\n|$)", text, re.DOTALL)
        if match:
            sections["sentiment"] = [line.strip("- ").strip() for line in match.group(1).split("\n") if line.strip()]

        # Extracting Language Detection
        match = re.search(r"Language Detection:\n- (.*?)\n", text)
        if match:
            sections["language"] = match.group(1).strip()

        # Extracting Plot Summary
        match = re.search(r"Plot Summary:\n(.*?)(?=\n\n|$)", text, re.DOTALL)
        if match:
            sections["plot_summary"] = [line.strip("- ").strip() for line in match.group(1).split("\n") if line.strip()]

        return sections
