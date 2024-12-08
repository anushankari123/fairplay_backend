import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy import select
from api.db.models.newsletter import Newsletter
from api.interfaces.newsletter import NewsletterSubscribe
from api.utils.exceptions import DuplicateConstraint
from .base import BaseService

class NewsletterService(BaseService):

    async def subscribe_to_newsletter(self, subscription_data: NewsletterSubscribe):
        """
        Subscribe a user to the newsletter and send a thank you email.
        """
        # Check if email already exists
        existing_query = await self.db.execute(
            select(Newsletter).where(Newsletter.email == subscription_data.email)
        )
        existing_subscription = existing_query.scalar_one_or_none()

        if existing_subscription:
            raise DuplicateConstraint("This email is already subscribed.")

        # Create a new subscription record
        new_subscription = Newsletter(email=subscription_data.email)
        self.db.add(new_subscription)
        await self.db.commit()

        # Send a thank you email
        self._send_thank_you_email(subscription_data.email)

        return {"message": "Subscription successful, a thank you email has been sent."}

    def _send_thank_you_email(self, email: str):
        """
        Send a thank you email to the subscriber.
        """
        sender_email = "fairplay202412@gmail.com"
        receiver_email = email
        password = "cqitnlgqotvhyhez"  # Make sure to use environment variables for sensitive data
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = "Welcome to FairPlay - Your Anti-Doping Companion"

        body = f"""Hi there,

Thank you for subscribing to FairPlay, your comprehensive anti-doping awareness platform!

We're excited to keep you informed about our mission to promote clean, fair, and ethical sports. FairPlay offers:

1. Supplement Verification: AI-powered safety checks ensuring WADA compliance
2. Professional Networking: Connect with athletes, coaches, and experts globally
3. Educational Resources: Interactive modules on anti-doping standards
4. TUE Guidance: Personalized support for Therapeutic Use Exemptions
5. Latest News: Curated insights from the world of clean sports

Stay committed to excellence. Stay clean. Stay FairPlay.

Best regards,
The FairPlay Team

"""
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")
