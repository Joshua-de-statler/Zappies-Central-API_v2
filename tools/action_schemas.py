# --- ADD THESE CLASSES TO THE END OF tools/action_schemas.py ---
from pydantic import EmailStr
from typing import Optional

# --- Schemas for Voice Agent Endpoints ---

class VoiceBookingRequest(BaseModel):
    """
    Schema for the /book-appointment endpoint (from voice agent).
    Note: 'email' is Pydantic's EmailStr for validation.
    """
    name: str
    email: EmailStr
    start_time: str
    goal: str = "Not provided"
    monthly_budget: float = 0.0
    company_name: str = "Not provided"
    client_number: Optional[str] = None
    call_duration_seconds: Optional[int] = 0

class CallLogRequest(BaseModel):
    """
    Schema for the /log-call endpoint (from voice agent).
    Logs calls that did *not* result in a meeting.
    """
    full_name: Optional[str] = "Not provided"
    email: Optional[EmailStr] = None
    company_name: Optional[str] = "Not provided"
    goal: Optional[str] = "Not provided"
    monthly_budget: Optional[float] = 0.0
    resulted_in_meeting: bool = False
    disqualification_reason: Optional[str] = None
    client_number: Optional[str] = None
    call_duration_seconds: Optional[int] = 0