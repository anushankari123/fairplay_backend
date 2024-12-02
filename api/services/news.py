import requests
from typing import List

class NewsService:
    BASE_URL = "https://newsapi.org/v2/everything"
    API_KEY = "8a546bb93cd1429c96fa3c5bd075809b"
    ITEMS_PER_PAGE = 20  # Increased to 20 articles per page

    @classmethod
    def fetch_news(cls, page: int = 1) -> List[dict]:
        try:
            # Query focused on sports, doping, and anti-doping
            query = "(doping OR anti-doping) AND sports"
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
            
            # Filter articles to include only those with images and ensure topic relevance
            articles = data.get("articles", [])
            filtered_articles = [
                article for article in articles 
                if article.get("urlToImage") is not None
                and any(keyword in article.get("title", "").lower() or article.get("description", "").lower()
                        for keyword in ["doping", "anti-doping", "sports"])
            ]
            
            return filtered_articles
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error fetching news: {str(e)}")