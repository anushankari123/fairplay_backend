from uuid import UUID
from fastapi import APIRouter, Depends, status
from api.services import AlertService
from api.interfaces.utils import List
from api.interfaces.alert import AlertRead, AlertCreate
from datetime import datetime
import pytz  # To handle timezone conversion

alert_router = APIRouter(prefix="/alerts")

# Dependency for AlertService
def get_alert_service(service: AlertService = Depends()) -> AlertService:
    return service

# Endpoint to get a specific alert by ID
@alert_router.get("/{alert_id}", response_model=AlertRead)
async def get_alert(alert_id: UUID, service: AlertService = Depends(get_alert_service)):
    """
    Endpoint to get alert details
    """
    return await service.get_alert(alert_id)

# Endpoint to get all alerts for a specific user
@alert_router.get("", response_model=List[AlertRead])
async def get_alerts(user_id: UUID, service: AlertService = Depends(get_alert_service)):
    """
    Endpoint to get a list of alerts for a specific user
    """
    return await service.get_alerts_for_user(user_id)

# Endpoint to create a new alert
@alert_router.post("", status_code=status.HTTP_201_CREATED, response_model=AlertRead)
async def create_alert(info: AlertCreate, user_id: UUID, service: AlertService = Depends(get_alert_service)):
    """
    Endpoint to create a new alert
    """
    # Ensure alert_datetime is naive (remove timezone info)
    alert_datetime = info.alert_datetime  # Assuming info has alert_datetime
    if alert_datetime.tzinfo is not None:
        alert_datetime = alert_datetime.astimezone(pytz.UTC)  # Convert to UTC
        alert_datetime = alert_datetime.replace(tzinfo=None)  # Make naive (remove timezone info)

    # Create the alert using the adjusted datetime
    return await service.create_alert(info.copy(update={"alert_datetime": alert_datetime}), user_id=user_id)

# Endpoint to get upcoming alerts that are scheduled to be displayed
@alert_router.get("/upcoming", response_model=List[AlertRead])
async def get_upcoming_alerts(
    current_time: datetime = datetime.now(), service: AlertService = Depends(get_alert_service)
):
    """
    Endpoint to get alerts that are scheduled for the current time or later
    """
    # Ensure current_time is naive
    if current_time.tzinfo is not None:
        current_time = current_time.astimezone(pytz.UTC)  # Convert to UTC
        current_time = current_time.replace(tzinfo=None)  # Make naive (remove timezone info)

    return await service.get_upcoming_alerts(current_time)
