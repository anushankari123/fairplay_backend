import google.generativeai as genai
import asyncio

class GeminiService:
    API_KEY = "AIzaSyAhxzEJkRiX-rb1VAvxJdERhKpkkA2U1tI"
    MODEL = "gemini-1.5-flash"

    @classmethod
    async def get_response(cls, prompt: str) -> str:
        try:
            # Asynchronously configure the Gemini API with the API key
            genai.configure(api_key=cls.API_KEY)
            
            # Create a GenerativeModel instance and use it to generate content
            model = genai.GenerativeModel(cls.MODEL)
            
            # Asynchronously generate content based on the provided prompt
            response = await asyncio.to_thread(model.generate_content, prompt)
            
            # Return the response text
            return response.text
        
        except Exception as e:
            raise Exception(f"Error fetching response: {str(e)}")
