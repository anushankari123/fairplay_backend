from uuid import UUID
from fastapi import APIRouter, Depends, status
from api.services import UserService
from api.interfaces.utils import List
from api.interfaces.user import UserRead, UserCreate, UserUpdate, UserLogin
from fastapi import Request
from fastapi.responses import RedirectResponse, JSONResponse
import os
import httpx



GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/users/google/callback")

user_router = APIRouter(prefix="/users")


@user_router.post("/login")
async def login(login_data: UserLogin, service: UserService = Depends(UserService)):
    """
    Endpoint for user login
    """
    return await service.login(login_data)


@user_router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: UUID, service: UserService = Depends(UserService)):
    """
    Endpoint to get a user details
    """
    return await service.get_user(user_id)


@user_router.get("", response_model=List[UserRead])
async def get_users(service: UserService = Depends(UserService)):
    """
    Endpoint to get a list of user
    """
    return await service.get_users()


@user_router.post("", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def create_user(info: UserCreate, service: UserService = Depends(UserService)):
    """
    Endpoint to create a user
    """
    return await service.create_user(info)


@user_router.delete("/{user_id}")
async def delete_user(user_id: UUID, service: UserService = Depends(UserService)):
    """
    Endpoint to delete a user
    """
    await service.delete_user(user_id)


@user_router.patch("/{user_id}", response_model=UserRead)
async def update_user(user_id: UUID, info: UserUpdate, service: UserService = Depends(UserService)):
    """
    Endpoint to update the given user details
    """
    return await service.update_user(user_id, info)

@user_router.get("/google/login")
async def google_login():
    """
    Redirects the user to Google's OAuth 2.0 authentication page.
    """
    # Debugging: Print environment variables
    print("GOOGLE_CLIENT_ID:", GOOGLE_CLIENT_ID)
    print("GOOGLE_REDIRECT_URI:", GOOGLE_REDIRECT_URI)

    google_auth_url = (
        "https://accounts.google.com/o/oauth2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        "&response_type=code"
        "&scope=openid email profile"
        "&access_type=offline"
    )
    return RedirectResponse(google_auth_url)


@user_router.get("/google/callback")
@user_router.post("/google/callback")
async def google_callback(
    request: Request,
    service: UserService = Depends(UserService)
):
    """
    Handles the callback from Google OAuth with flexible request handling
    """
    # Determine request method and parse accordingly
    if request.method == "GET":
        # For GET requests, parameters are in query params
        code = request.query_params.get("code")
        code_verifier = request.query_params.get("code_verifier")
    else:  # POST method
        try:
            # For POST, parse the request body
            body = await request.json()
            code = body.get("code")
            code_verifier = body.get("code_verifier")
        except Exception as e:
            print(f"Error parsing request body: {e}")
            return JSONResponse(
                status_code=400, 
                content={"error": "Invalid request body"}
            )

    # Validate code is present
    if not code:
        return JSONResponse(
            status_code=400, 
            content={"error": "Missing authorization code"}
        )

    try:
        # Pass both code and code_verifier to the service method
        user = await service.create_user_with_google(
            code, 
            code_verifier=code_verifier  # Explicitly pass as a keyword argument
        )
        return {
            "message": "User authenticated successfully", 
            "user": user
        }
    except Exception as e:
        print(f"Authentication error: {e}")
        return JSONResponse(
            status_code=500, 
            content={"error": str(e)}
        )
