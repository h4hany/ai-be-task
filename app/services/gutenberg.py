import requests
from bs4 import BeautifulSoup

class GutenbergService:
    @staticmethod
    def get_book(book_id: int):
        try:
            # Try UTF-8 version first
            content_url = f"https://www.gutenberg.org/files/{book_id}/{book_id}-0.txt"
            content_response = requests.get(content_url)
            
            # If UTF-8 version fails, try plain text version
            if content_response.status_code != 200:
                content_url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
                content_response = requests.get(content_url)
                
            content_response.raise_for_status()
            content = content_response.text

            # Get metadata
            metadata_url = f"https://www.gutenberg.org/ebooks/{book_id}"
            metadata_response = requests.get(metadata_url)
            metadata_response.raise_for_status()
            
            soup = BeautifulSoup(metadata_response.text, 'html.parser')
            
            # Extract title and author
            title = soup.find('h1', itemprop='name').text.strip() if soup.find('h1', itemprop='name') else "Unknown Title"
            author_elem = soup.find('span', itemprop='author')
            author = author_elem.text.strip() if author_elem else "Unknown Author"

            return {
                "content": content,
                "metadata": {
                    "title": title,
                    "author": author,
                    "book_id": book_id
                }
            }
        except Exception as e:
            raise Exception(f"Error fetching book {book_id}: {str(e)}") 