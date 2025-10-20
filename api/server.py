# api/server.py
import asyncio
import logging
import datetime
import pytz
import json

from fastapi import FastAPI, HTTPException, Depends, Header, status
from pydantic import BaseModel
from supabase.client import Client, create_client
from config.settings import settings
from agent.agent_factory import create_agent_executor
from langchain.memory import ConversationBufferMemory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, messages_from_dict, messages_to_dict
from collections import defaultdict
from fastapi.responses import HTMLResponse
from tools.google_calendar import create_calendar_event

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION
)

async def verify_api_key(x_api_key: str = Header()):
    if not settings.API_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API Secret Key not configured on the server."
        )
    if x_api_key != settings.API_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key."
        )

agent_semaphore = asyncio.Semaphore(settings.CONCURRENCY_LIMIT)
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)

conversation_locks = defaultdict(asyncio.Lock)

class SupabaseChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id: str, table_name: str):
        self.session_id = session_id
        self.table_name = table_name

    @property
    def messages(self):
        """Retrieve and clean messages from Supabase."""
        response = supabase.table(self.table_name).select("history").eq("conversation_id", self.session_id).execute()
        
        if not response.data or not response.data[0].get('history'):
            return []

        history_data = response.data[0]['history']

        # --- THIS IS THE FIX ---
        # Iterate through the history and fix any malformed tool_calls before validation
        for message_data in history_data:
            if message_data.get("type") == "ai":
                ai_data = message_data.get("data", {})
                tool_calls = ai_data.get("tool_calls")
                if tool_calls and isinstance(tool_calls, list):
                    for tool_call in tool_calls:
                        # If args is a string, attempt to convert it to a dict
                        if "args" in tool_call and isinstance(tool_call["args"], str):
                            try:
                                # First, try to parse it as JSON
                                tool_call["args"] = json.loads(tool_call["args"])
                            except json.JSONDecodeError:
                                # If it's not JSON, wrap it in a dict
                                tool_call["args"] = {"query": tool_call["args"]}
        
        return messages_from_dict(history_data)


    def add_messages(self, messages: list[BaseMessage]) -> None:
        """Save messages to Supabase, correctly formatting tool calls."""
        current_history_dicts = messages_to_dict(self.messages)
        
        new_history_dicts = []
        for message in messages:
            message_dict = messages_to_dict([message])[0]
            if isinstance(message, AIMessage) and hasattr(message, 'tool_calls') and message.tool_calls:
                # Ensure the tool_calls are in the correct format before saving
                message_dict['data']['tool_calls'] = message.tool_calls
            new_history_dicts.append(message_dict)

        updated_history = current_history_dicts + new_history_dicts
        
        supabase.table(self.table_name).upsert({
            "conversation_id": self.session_id, 
            "history": updated_history,
            "status": "active"
        }).execute()

    def clear(self) -> None:
        supabase.table(self.table_name).delete().eq("conversation_id", self.session_id).execute()

class ChatRequest(BaseModel):
    conversation_id: str
    query: str

@app.post("/chat", dependencies=[Depends(verify_api_key)])
async def chat_with_agent(request: ChatRequest):
    lock = conversation_locks[request.conversation_id]

    async with lock:
        try:
            # --- THIS IS A FIX ---
            # Removed .single() to prevent errors on the first turn of a conversation.
            status_response = supabase.table("conversation_history").select("status").eq("conversation_id", request.conversation_id).execute()
            
            if status_response.data and status_response.data[0].get('status') == 'handover':
                logger.info(f"Conversation {request.conversation_id} is in handover. Bypassing agent.")
                message_history = SupabaseChatMessageHistory(session_id=request.conversation_id, table_name=settings.DB_CONVERSATION_HISTORY_TABLE)
                message_history.add_messages([HumanMessage(content=request.query)])
                return {"response": "A human agent will be with you shortly. Thank you for your patience."}
        except Exception:
            pass
        
        async with agent_semaphore:
            try:
                message_history = SupabaseChatMessageHistory(
                    session_id=request.conversation_id,
                    table_name=settings.DB_CONVERSATION_HISTORY_TABLE
                )
                
                memory = ConversationBufferMemory(
                    memory_key="history",
                    chat_memory=message_history,
                    return_messages=True,
                    input_key="input"
                )

                agent_executor, tool_callback = create_agent_executor(memory, conversation_id=request.conversation_id)

                sast_tz = pytz.timezone("Africa/Johannesburg")
                current_time_sast = datetime.datetime.now(sast_tz).strftime('%A, %Y-%m-%d %H:%M:%S %Z')

                agent_input = {
                    "input": request.query,
                    "current_time": current_time_sast,
                    "conversation_id": request.conversation_id
                }
                logger.info(f"--- AGENT INPUT FOR CONVO ID: {request.conversation_id} ---")
                logger.info(agent_input)
                logger.info("----------------------------------------------------")
                
                response = await agent_executor.ainvoke(agent_input)

                agent_output = response.get("output")
                
                tool_calls = tool_callback.tool_calls
                ai_message = AIMessage(content=agent_output)
                if tool_calls:
                    ai_message.tool_calls = tool_calls

                # message_history.add_messages([
                #     HumanMessage(content=request.query),
                #     ai_message
                # ])

                if not agent_output or not agent_output.strip():
                    logger.warning(f"Agent for convo ID {request.conversation_id} generated an empty response. Sending a default message.")
                    agent_output = "I'm sorry, I seem to have lost my train of thought. Could you please tell me a little more about what you're looking for?"

                return {"response": agent_output}
            except Exception as e:
                logger.error(f"Error in /chat for conversation_id {request.conversation_id}: {e}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/confirm-meeting/{meeting_id}", response_class=HTMLResponse)
async def confirm_meeting(meeting_id: str):
    """Endpoint to confirm a meeting, create a calendar event, and update the DB."""
    try:
        response = supabase.table("meetings").select("*").eq("id", meeting_id).single().execute()
        
        if not response.data:
            return "<h1>Meeting Not Found</h1><p>This confirmation link is invalid or has expired.</p>"
        
        meeting_details = response.data
        
        if meeting_details['status'] == 'confirmed':
            return "<h1>Meeting Already Confirmed</h1><p>Your spot was already secured. We look forward to seeing you!</p>"

        summary = f"Onboard Call with {meeting_details['company_name']} | Zappies AI"
        description = (
            f"Onboarding call with {meeting_details['full_name']} from {meeting_details['company_name']} to discuss the 'Project Pipeline AI'.\n\n"
            f"Stated Goal: {meeting_details['goal']}\n"
            f"Stated Budget: R{meeting_details['monthly_budget']}/month"
        )
        
        created_event = create_calendar_event(
            start_time=meeting_details['start_time'],
            summary=summary,
            description=description,
            attendees=[meeting_details['email']]
        )
        
        supabase.table("meetings").update({
            "status": "confirmed",
            "google_calendar_event_id": created_event.get('id')
        }).eq("id", meeting_id).execute()
        
        logger.info(f"Meeting {meeting_id} confirmed and calendar event created successfully.")
        return "<h1>Thank You!</h1><p>Your meeting has been successfully confirmed. We've added it to our calendar and look forward to speaking with you!</p>"

    except Exception as e:
        logger.error(f"Error confirming meeting {meeting_id}: {e}", exc_info=True)
        return "<h1>Error</h1><p>Sorry, something went wrong while confirming your meeting. Please try again later.</p>"