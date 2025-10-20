from pydantic import BaseModel, Field

class CheckAvailabilityArgs(BaseModel):
    """Schema for checking available time slots on a given date."""
    date: str = Field(description="The date to check for available slots, in YYYY-MM-DD format.")

class BookOnboardingCallArgs(BaseModel):
    """Schema for booking an official onboarding call with the Zappies AI team."""
    full_name: str = Field(description="The full name of the renovation company owner or decision-maker.")
    email: str = Field(description="The business email address where the calendar invite should be sent.")
    company_name: str = Field(description="The name of their renovation company.")
    start_time: str = Field(description="The start time for the meeting in ISO 8601 format (e.g., '2023-10-27T09:00:00').")
    goal: str = Field(description="The user's primary goal or what they hope to achieve with the 'Project Pipeline AI'.")
    monthly_budget: float = Field(description="The user's approximate monthly budget in Rands for this type of solution.")
    conversation_id: str = Field(description="The unique identifier for the current user's conversation session. This is ALWAYS available to you.")

class CancelAppointmentArgs(BaseModel):
    """Schema for canceling an existing onboarding call."""
    email: str = Field(description="The email address used to book the original appointment.")
    original_start_time: str = Field(description="The original start time of the appointment to be canceled, in ISO 8601 format.")

class RescheduleAppointmentArgs(BaseModel):
    """Schema for rescheduling an existing onboarding call."""
    email: str = Field(description="The email address used to book the original appointment.")
    original_start_time: str = Field(description="The original start time of the appointment to be rescheduled, in ISO 8601 format.")
    new_start_time: str = Field(description="The new desired start time for the appointment, in ISO 8601 format.")

class RequestHumanHandoverArgs(BaseModel):
    """Schema for requesting a human handover."""
    conversation_id: str = Field(description="The unique identifier for the current user's conversation session. This is ALWAYS available to you.")