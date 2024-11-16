import requests
from typing import List

class NewsService:
    BASE_URL = "https://newsapi.org/v2/everything"
    API_KEY = "8a546bb93cd1429c96fa3c5bd075809b"
    ITEMS_PER_PAGE = 20  # Increased to 20 articles per page

    @classmethod
    def fetch_news(cls, page: int = 1) -> List[dict]:
        try:
            query = "doping OR anti-doping"
            params = {
                "q": query,
                "apiKey": cls.API_KEY,
                "sortBy": "publishedAt",
                "pageSize": cls.ITEMS_PER_PAGE,
                "page": page,
                "language": "en"
            }

            response = requests.get(cls.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Add error handling for API response
            if data.get("status") == "error":
                raise Exception(data.get("message", "Failed to fetch news"))
                
            return data.get("articles", [])
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error fetching news: {str(e)}")