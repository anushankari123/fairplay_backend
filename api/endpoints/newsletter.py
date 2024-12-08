from fastapi import APIRouter, Depends, status
from api.services import NewsletterService
from api.interfaces.newsletter import NewsletterSubscribe

# Create the router instance
newsletter_router = APIRouter(prefix="/newsletter")

@newsletter_router.post("/subscribe", status_code=status.HTTP_201_CREATED)
async def subscribe(subscription_data: NewsletterSubscribe, service: NewsletterService = Depends(NewsletterService)):
    """
    Endpoint for subscribing to the newsletter.
    """
    return await service.subscribe_to_newsletter(subscription_data)
