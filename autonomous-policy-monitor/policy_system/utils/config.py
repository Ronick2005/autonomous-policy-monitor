"""
Configuration module for Autonomous Policy Compliance Monitoring System
Loads environment variables and provides global configuration
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

# Neo4j Knowledge Graph Configuration
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

# MongoDB Knowledge Base Configuration
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "policy_compliance_kb")

# LangSmith Configuration (for research tracing)
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "true")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "autonomous-policy-monitor")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")

# Enable LangSmith tracing for research
if LANGSMITH_API_KEY:
    os.environ["LANGCHAIN_TRACING_V2"] = LANGCHAIN_TRACING_V2
    os.environ["LANGCHAIN_API_KEY"] = LANGSMITH_API_KEY
    os.environ["LANGCHAIN_PROJECT"] = LANGCHAIN_PROJECT
    os.environ["LANGCHAIN_ENDPOINT"] = LANGCHAIN_ENDPOINT
    print(f"[OK] LangSmith tracing enabled for project: {LANGCHAIN_PROJECT}")
else:
    print("[WARNING] LangSmith API key not found. Tracing disabled.")

# Validate critical configurations
if not GEMINI_API_KEY:
    print("[WARNING] GEMINI_API_KEY not set. AI features will not work.")

if NEO4J_URI == "bolt://localhost:7687":
    print("[WARNING] Using default Neo4j URI. Update for production.")

if MONGODB_URI == "mongodb://localhost:27017/":
    print("[WARNING] Using default MongoDB URI. Update for production.")


class Config:
    """Configuration class for easy access to all settings"""
    # Google Gemini Configuration
    GEMINI_API_KEY = GEMINI_API_KEY
    GEMINI_MODEL = GEMINI_MODEL
    
    # Neo4j Knowledge Graph Configuration
    NEO4J_URI = NEO4J_URI
    NEO4J_USERNAME = NEO4J_USERNAME
    NEO4J_PASSWORD = NEO4J_PASSWORD
    
    # MongoDB Knowledge Base Configuration
    MONGODB_URI = MONGODB_URI
    MONGODB_DB_NAME = MONGODB_DB_NAME
    
    # LangSmith Configuration
    LANGSMITH_API_KEY = LANGSMITH_API_KEY
    LANGCHAIN_TRACING_V2 = LANGCHAIN_TRACING_V2
    LANGCHAIN_PROJECT = LANGCHAIN_PROJECT
    LANGCHAIN_ENDPOINT = LANGCHAIN_ENDPOINT
