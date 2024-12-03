import requests
from typing import List, Dict

class JournalService:
    BASE_URL = "https://api.crossref.org/works"
    ITEMS_PER_PAGE = 20  # Number of results per page

    @classmethod
    def fetch_journals(cls, page: int = 1) -> List[dict]:
        """
        Fetch scientific journals related to doping practices,
        sorted by relevance first and then by publication date (latest first).
        
        :param page: Page number for pagination
        :return: List of sorted journal articles
        """
        try:
            # Construct search query
            params = {
                "query": "Doping practices athletes OR performance enhancement OR banned substances OR drug testing",
                "rows": cls.ITEMS_PER_PAGE,
                "offset": (page - 1) * cls.ITEMS_PER_PAGE,
                "filter": "type:journal-article"
            }
            
            # Make API request
            headers = {
                'User-Agent': 'YourAppName/1.0 (your_email@example.com)'
            }
            
            response = requests.get(
                cls.BASE_URL, 
                params=params, 
                headers=headers
            )
            
            # Handle errors
            if response.status_code != 200:
                raise Exception(f"API Error: {response.status_code} - {response.text}")
            
            # Parse response
            data = response.json()
            articles = data.get("message", {}).get("items", [])
            
            # Process and transform journal articles
            processed_journals = []
            for item in articles:
                processed_journal = {
                    "title": cls._extract_title(item),
                    "authors": cls._extract_authors(item),
                    "journal": cls._extract_journal_name(item),
                    "published_date": cls._extract_publication_date(item),
                    "doi": item.get("DOI", ""),
                    "url": cls._extract_url(item)
                }
                processed_journals.append(processed_journal)
            
            # Sort by latest publication date
            processed_journals.sort(
                key=lambda x: x["published_date"], reverse=True
            )
            
            return processed_journals
        
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            print(f"General Error: {e}")
            raise Exception(f"Error fetching journals: {str(e)}")
    
    @staticmethod
    def _extract_title(item: Dict) -> str:
        """Extract title from journal item"""
        return item.get("title", ["Unknown Title"])[0] if item.get("title") else "Unknown Title"
    
    @staticmethod
    def _extract_authors(item: Dict) -> List[str]:
        """Extract authors from journal item"""
        return [
            f"{author.get('given', '')} {author.get('family', '')}".strip()
            for author in item.get("author", [])
        ] or ["Unknown Author"]
    
    @staticmethod
    def _extract_journal_name(item: Dict) -> str:
        """Extract journal name from item"""
        return item.get("container-title", ["Unknown Journal"])[0] if item.get("container-title") else "Unknown Journal"
    
    @staticmethod
    def _extract_publication_date(item: Dict) -> str:
        """Extract publication date from item"""
        date_parts = item.get("published-print", {}).get("date-parts", [[None]])
        if not date_parts[0][0]:
            date_parts = item.get("published-online", {}).get("date-parts", [[None]])
        return "-".join(map(str, date_parts[0])) if date_parts[0][0] else "Unknown Date"
    
    @staticmethod
    def _extract_url(item: Dict) -> str:
        """Extract URL from journal item"""
        return item.get("URL") or f"https://doi.org/{item.get('DOI', '')}"

# Optional: Debug method
def debug_journal_service():
    try:
        journals = JournalService.fetch_journals(page=1)
        print(f"Fetched {len(journals)} journals")
        for journal in journals:
            print("\n--- Journal ---")
            print(f"Title: {journal['title']}")
            print(f"Authors: {', '.join(journal['authors'])}")
            print(f"Journal: {journal['journal']}")
            print(f"Published: {journal['published_date']}")
            print(f"DOI: {journal['doi']}")
            print(f"URL: {journal['url']}")
    except Exception as e:
        print(f"Debug failed: {e}")
