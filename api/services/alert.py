from uuid import UUID
from datetime import datetime
from sqlmodel import col
from api.db.models.alert import Alert
from api.interfaces.utils import List
from api.interfaces.alert import AlertCreate, AlertRead
from api.utils.exceptions import NotFoundError
from .base import BaseService


class AlertService(BaseService):
    async def get_alert(self, alert_id: UUID) -> AlertRead:
        """
        Retrieve a specific alert by its UUID.

        Args:
        - alert_id (UUID): The UUID of the alert to retrieve.

        Returns:
        - AlertRead: Details of the retrieved alert.

        Raises:
        - NotFoundError: Raised if the alert is not found.
        """
        res = await Alert.get(db=self.db, filters=[Alert.id == alert_id, ~col(Alert.is_deleted)])
        alert = res.one_or_none()
        if alert is None:
            raise NotFoundError("Alert not found")
        return alert

    async def get_alerts_for_user(self, user_id: UUID) -> List[AlertRead]:
        """
        Retrieve a list of alerts for a specific user.

        Args:
        - user_id (UUID): The UUID of the user.

        Returns:
        - List[AlertRead]: List of alerts for the user.
        """
        res = await Alert.get(db=self.db, filters=[Alert.user_id == user_id, ~col(Alert.is_deleted)])
        return {"data": res.all()}

    async def get_upcoming_alerts(self, current_time: datetime) -> List[AlertRead]:
        """
        Retrieve alerts scheduled to trigger at or after the current time.

        Args:
        - current_time (datetime): The current time.

        Returns:
        - List[AlertRead]: List of upcoming alerts.
        """
        res = await Alert.get(
            db=self.db,
            filters=[Alert.alert_datetime <= current_time, ~col(Alert.is_deleted)]
        )
        return {"data": res.all()}

    async def create_alert(self, data: AlertCreate, user_id: UUID) -> AlertRead:
        """
        Create a new alert.

        Args:
        - data (AlertCreate): Information to create the alert.
        - user_id (UUID): The ID of the user who is creating the alert.

        Returns:
        - AlertRead: Details of the created alert.
        """
        new_alert = Alert(**data.model_dump(), user_id=user_id)
        await new_alert.save(self.db)
        return new_alert

    async def delete_alert(self, alert_id: UUID):
        """
        Mark an alert as deleted.

        Args:
        - alert_id (UUID): The UUID of the alert to delete.
        """
        alert = await self.get_alert(alert_id)
        alert.is_deleted = True
        await alert.save(self.db)
