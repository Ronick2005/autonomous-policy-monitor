"""
Streamlit Research Dashboard for Autonomous Policy Monitoring System

Features:
- User authentication with role-based access
- Multi-agent policy compliance queries
- Knowledge graph visualization
- LangSmith integration for research traceability
- Agent workflow insights
- Sample queries for demonstration
"""

import streamlit as st
import json
from datetime import datetime
import os

from policy_system.agents.orchestrator import create_orchestrator
from policy_system.utils.auth import authenticate_user, get_all_users
from policy_system.utils.config import Config


# Page configuration
st.set_page_config(
    page_title="Autonomous Policy Monitoring System",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .metric-container {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'role' not in st.session_state:
        st.session_state.role = None
    if 'orchestrator' not in st.session_state:
        st.session_state.orchestrator = None
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []


def login_page():
    """Display login page."""
    st.markdown('<div class="main-header">🔐 Autonomous Policy Monitoring System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Research Dashboard for Policy Compliance Detection</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", type="primary", use_container_width=True):
            user = authenticate_user(username, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.role = user['role']
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error("Invalid credentials")
        
        st.markdown("---")
        st.markdown("### Demo Credentials")
        st.code("""
Username: researcher | Password: research123
Username: admin      | Password: admin123
Username: auditor    | Password: audit123
        """)


def initialize_orchestrator():
    """Initialize the orchestrator with database connections."""
    if st.session_state.orchestrator is None:
        try:
            orchestrator = create_orchestrator(
                neo4j_uri=Config.NEO4J_URI,
                neo4j_user=Config.NEO4J_USERNAME,
                neo4j_password=Config.NEO4J_PASSWORD,
                mongodb_uri=Config.MONGODB_URI
            )
            st.session_state.orchestrator = orchestrator
            return True
        except Exception as e:
            st.error(f"Failed to initialize orchestrator: {e}")
            return False
    return True


def sidebar():
    """Display sidebar with system information and agent details."""
    st.sidebar.title("📋 System Dashboard")
    
    # User info
    st.sidebar.markdown(f"**User:** {st.session_state.username}")
    st.sidebar.markdown(f"**Role:** {st.session_state.role.title()}")
    
    # LangSmith status
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔬 Research Tracing")
    
    langsmith_enabled = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
    if langsmith_enabled:
        st.sidebar.success("✅ LangSmith Active")
        st.sidebar.markdown(f"**Project:** {os.getenv('LANGCHAIN_PROJECT', 'policy-monitoring')}")
        if os.getenv('LANGSMITH_API_KEY'):
            st.sidebar.markdown("**API Key:** Configured ✓")
    else:
        st.sidebar.warning("⚠️ LangSmith Disabled")
        st.sidebar.markdown("Enable in .env for research tracing")
    
    # Agent information
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🤖 Available Agents")
    
    agents = [
        ("📊", "Policy Classification", "Categorizes policies by type and risk"),
        ("✅", "Compliance Detection", "Identifies violations and compliance gaps"),
        ("⚔️", "Conflict Analysis", "Detects policy conflicts and contradictions"),
        ("⚠️", "Risk Assessment", "Evaluates risk levels and impact"),
        ("💡", "Recommendation", "Suggests improvements and remediation"),
        ("❓", "General Query", "Handles general questions")
    ]
    
    for icon, name, desc in agents:
        with st.sidebar.expander(f"{icon} {name}"):
            st.markdown(f"*{desc}*")
    
    # Knowledge systems status
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💾 Knowledge Systems")
    
    try:
        if st.session_state.orchestrator:
            # Neo4j status
            stats = st.session_state.orchestrator.kg.get_network_statistics()
            if stats:
                st.sidebar.success("✅ Neo4j Connected")
                st.sidebar.markdown(f"**Policies:** {stats.get('policies', 0)}")
                st.sidebar.markdown(f"**Organizations:** {stats.get('organizations', 0)}")
            else:
                st.sidebar.info("🔄 Neo4j Empty")
            
            # MongoDB status
            st.sidebar.success("✅ MongoDB Connected")
    except Exception as e:
        st.sidebar.error("❌ Database Connection Issue")
    
    # Logout
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


def main_dashboard():
    """Main dashboard interface."""
    st.markdown('<div class="main-header">📋 Autonomous Policy Monitoring System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Policy Compliance Detection Using Multi-Agent Knowledge Graphs</div>', unsafe_allow_html=True)
    
    # Initialize orchestrator
    if not initialize_orchestrator():
        st.error("Cannot proceed without orchestrator initialization")
        return
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Total Queries", len(st.session_state.query_history))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Active Agents", "6")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        try:
            stats = st.session_state.orchestrator.kg.get_network_statistics()
            policy_count = stats.get('policies', 0) if stats else 0
        except:
            policy_count = 0
        st.metric("Policies", policy_count)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("LangSmith", "✅" if os.getenv("LANGCHAIN_TRACING_V2") == "true" else "❌")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Query interface
    st.markdown("### 🔍 Policy Compliance Query")
    
    # Sample queries
    st.markdown("#### 📝 Sample Queries")
    col1, col2, col3 = st.columns(3)
    
    sample_queries = [
        ("Classify Policy", "Classify the data privacy policy for our organization"),
        ("Check Compliance", "Is our data retention policy compliant with GDPR?"),
        ("Find Conflicts", "Are there any conflicts between our security and privacy policies?"),
        ("Assess Risk", "What is the risk level of our current access control policy?"),
        ("Get Recommendations", "Recommend improvements to our compliance framework"),
        ("General Info", "What regulations apply to financial services companies?")
    ]
    
    for i, (label, query) in enumerate(sample_queries):
        col = [col1, col2, col3][i % 3]
        with col:
            if st.button(label, key=f"sample_{i}", use_container_width=True):
                st.session_state.selected_query = query
    
    # Query input
    query = st.text_area(
        "Enter your policy compliance query:",
        value=st.session_state.get('selected_query', ''),
        height=100,
        placeholder="Example: Check if our data retention policy complies with GDPR requirements"
    )
    
    col1, col2 = st.columns([1, 5])
    with col1:
        submit_button = st.button("🚀 Submit Query", type="primary", use_container_width=True)
    with col2:
        clear_button = st.button("🗑️ Clear History", use_container_width=True)
        if clear_button:
            st.session_state.query_history = []
            st.rerun()
    
    # Process query
    if submit_button and query:
        with st.spinner("🤔 Processing query through multi-agent system..."):
            try:
                result = st.session_state.orchestrator.process_query(
                    query=query,
                    user_id=st.session_state.username
                )
                
                # Add to history
                st.session_state.query_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'query': query,
                    'result': result
                })
                
                # Display result
                if result.get('success'):
                    st.markdown('<div class="success-box">✅ Query Processed Successfully</div>', unsafe_allow_html=True)
                    
                    # Response
                    st.markdown("### 💬 Response")
                    st.markdown(result['response'])
                    
                    # Metadata
                    with st.expander("📊 Execution Metadata (Research Tracing)"):
                        metadata = result.get('metadata', {})
                        st.json(metadata)
                        
                        # LangSmith link
                        if os.getenv("LANGCHAIN_TRACING_V2") == "true":
                            st.info("🔬 Full execution trace available in LangSmith dashboard")
                else:
                    st.markdown('<div class="warning-box">⚠️ Query Processing Failed</div>', unsafe_allow_html=True)
                    st.error(result.get('response', 'Unknown error'))
                    
            except Exception as e:
                st.error(f"Error processing query: {e}")
    
    # Query history
    if st.session_state.query_history:
        st.markdown("---")
        st.markdown("### 📜 Query History")
        
        for i, item in enumerate(reversed(st.session_state.query_history[-5:]), 1):
            with st.expander(f"Query {len(st.session_state.query_history) - i + 1}: {item['query'][:60]}..."):
                st.markdown(f"**Timestamp:** {item['timestamp']}")
                st.markdown(f"**Query:** {item['query']}")
                st.markdown(f"**Response:**")
                st.markdown(item['result']['response'])


def main():
    """Main application entry point."""
    initialize_session_state()
    
    if not st.session_state.authenticated:
        login_page()
    else:
        sidebar()
        main_dashboard()


if __name__ == "__main__":
    main()
