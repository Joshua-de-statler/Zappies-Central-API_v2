# config/settings.py
import os
from dotenv import load_dotenv

# Load environment variables from a .env file at the project root
load_dotenv()

class Settings:
    """
    Centralized application settings, loaded from environment variables.
    """
    # --- Email Configuration ---
    HANDOVER_EMAIL: str = os.getenv("HANDOVER_EMAIL")
    SENDER_EMAIL: str = os.getenv("SENDER_EMAIL")
    SENDER_APP_PASSWORD: str = os.getenv("SENDER_APP_PASSWORD")

    # The public base URL of your API for confirmation links
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

    # --- Google Calendar ---
    GOOGLE_CALENDAR_ID: str = os.getenv("GOOGLE_CALENDAR_ID", "primary")
    # File-based (original)
    SERVICE_ACCOUNT_FILE: str = "service_account.json"
    # String-based (from voice agent, better for deployment)
    GOOGLE_CREDENTIALS_STR: str = os.getenv("GOOGLE_CREDENTIALS_JSON")

    # --- API and Security ---
    API_SECRET_KEY: str = os.getenv("API_SECRET_KEY", "DEFAULT_SECRET_KEY")
    API_TITLE: str = "Zappies-AI Bot API"
    API_DESCRIPTION: str = "A dynamic, reusable AI agent API."
    API_VERSION: str = "1.0.0"
    CONCURRENCY_LIMIT: int = int(os.getenv("CONCURRENCY_LIMIT", 5))

    # --- LLM and Embeddings ---
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")
    GENERATIVE_MODEL: str = "gemini-2.5-flash"
    EMBEDDING_MODEL: str = "models/embedding-001"
    AGENT_TEMPERATURE: float = 0.1
    AGENT_MAX_ITERATIONS: int = 10

    # --- Vector Database (Supabase) ---
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_SERVICE_KEY: str = os.getenv("SUPABASE_SERVICE_KEY")

    # --- Graph Database (Neo4j) ---
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USERNAME: str = os.getenv("NEO4J_USERNAME", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD")

    # --- Data Ingestion ---
    SOURCE_DIRECTORY_PATH: str = "data/"
    DB_INGESTION_LOG_TABLE: str = "ingestion_log"
    DB_VECTOR_TABLE: str = "documents"
    DB_VECTOR_QUERY_NAME: str = "match_documents"
    DB_CONVERSATION_HISTORY_TABLE: str = "conversation_history"

    # --- Graph Generation (Optional Customization) ---
    GRAPH_ALLOWED_NODES: list[str] = [
        "Policy", "Rule", "Membership", "Party", "Guest", "Item",
        "Payment", "Action", "Condition", "Location"
    ]
    GRAPH_ALLOWED_RELATIONSHIPS: list[str] = [
        "APPLIES_TO", "CONCERNS", "PROHIBITS", "REQUIRES", "INCLUDES",
        "HAS_CONDITION", "MUST_PERFORM", "HAS_FEE"
    ]

    # --- Voice Agent Business Logic ---
    # Nested class to group voice agent settings
    class VOICE_AGENT_CONFIG:
        TIMEZONE: str = 'Africa/Johannesburg'
        BUSINESS_HOURS_START: int = 8  # 8 AM
        BUSINESS_HOURS_END: int = 16  # 4 PM
        APPOINTMENT_DURATION_MINUTES: int = 60
        SEARCH_WINDOW_DAYS: int = 14
        SUGGESTION_COUNT: int = 5


# Instantiate settings for easy import across the application
settings = Settings()