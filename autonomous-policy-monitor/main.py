"""
Main Launcher for Autonomous Policy Monitoring System

This script provides a simple CLI to run system components.
"""

import sys
import os


def display_menu():
    """Display the main menu."""
    print("\n" + "="*60)
    print("  AUTONOMOUS POLICY MONITORING SYSTEM")
    print("  Research Dashboard for Policy Compliance Detection")
    print("="*60)
    print("\nSelect an option:")
    print("\n[Setup & Data]")
    print("1. Populate Knowledge Graph (Neo4j)")
    print("2. Populate Knowledge Base (MongoDB)")
    print("3. Run Both Population Scripts")
    print("\n[Launch System]")
    print("4. Start Streamlit Dashboard")
    print("\n[Utilities]")
    print("5. Check System Status")
    print("6. View Configuration")
    print("\n0. Exit")
    print("\n" + "-"*60)


def populate_knowledge_graph():
    """Run knowledge graph population script."""
    print("\n🚀 Populating Knowledge Graph (Neo4j)...\n")
    from populate_knowledge_graph import populate_knowledge_graph as populate
    try:
        populate()
        print("\n✅ Knowledge Graph population complete!")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def populate_knowledge_base():
    """Run knowledge base population script."""
    print("\n🚀 Populating Knowledge Base (MongoDB)...\n")
    from populate_knowledge_base import populate_knowledge_base as populate
    try:
        populate()
        print("\n✅ Knowledge Base population complete!")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def populate_all():
    """Run both population scripts."""
    populate_knowledge_graph()
    print("\n" + "-"*60 + "\n")
    populate_knowledge_base()


def start_dashboard():
    """Start Streamlit dashboard."""
    print("\n🚀 Starting Streamlit Dashboard...\n")
    print("Dashboard will open at: http://localhost:8501")
    print("Login with: researcher / research123\n")
    os.system("streamlit run streamlit_app.py")


def check_status():
    """Check system configuration and database status."""
    print("\n📊 System Status Check\n")
    print("-" * 60)
    
    # Check environment variables
    print("\n[Environment Configuration]")
    from policy_system.utils.config import Config
    
    print(f"✓ GEMINI_API_KEY: {'Configured' if Config.GEMINI_API_KEY else '❌ Not set'}")
    print(f"✓ NEO4J_URI: {Config.NEO4J_URI or '❌ Not set'}")
    print(f"✓ MONGODB_URI: {Config.MONGODB_URI or '❌ Not set'}")
    
    langsmith_key = os.getenv("LANGSMITH_API_KEY")
    langsmith_tracing = os.getenv("LANGCHAIN_TRACING_V2", "false")
    print(f"✓ LANGSMITH_API_KEY: {'Configured' if langsmith_key else '❌ Not set'}")
    print(f"✓ LANGCHAIN_TRACING_V2: {langsmith_tracing}")
    
    # Test Neo4j connection
    print("\n[Neo4j Connection]")
    try:
        from policy_system.kg.neo4j_kg import Neo4jPolicyGraph
        kg = Neo4jPolicyGraph(
            uri=Config.NEO4J_URI,
            user=Config.NEO4J_USERNAME,
            password=Config.NEO4J_PASSWORD
        )
        stats = kg.get_network_statistics()
        if stats:
            print("✅ Connected successfully")
            print(f"   Organizations: {stats.get('total_organizations', 0)}")
            print(f"   Policies: {stats.get('total_policies', 0)}")
            print(f"   Regulations: {stats.get('total_regulations', 0)}")
            print(f"   Violations: {stats.get('total_violations', 0)}")
        else:
            print("⚠️  Connected but no data found (run population script)")
        kg.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")
    
    # Test MongoDB connection
    print("\n[MongoDB Connection]")
    try:
        from policy_system.kb.mongodb_kb import MongoPolicyKB
        kb = MongoPolicyKB()
        print("✅ Connected successfully")
        kb.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")
    
    print("\n" + "-" * 60 + "\n")


def view_config():
    """Display current configuration."""
    print("\n⚙️  System Configuration\n")
    print("-" * 60)
    
    from policy_system.utils.config import Config
    
    print(f"\n[API Keys]")
    print(f"GEMINI_API_KEY: {'*' * 20 if Config.GEMINI_API_KEY else 'Not set'}")
    
    print(f"\n[Neo4j Database]")
    print(f"URI: {Config.NEO4J_URI}")
    print(f"User: {Config.NEO4J_USERNAME}")
    print(f"Password: {'*' * 10 if Config.NEO4J_PASSWORD else 'Not set'}")
    
    print(f"\n[MongoDB Database]")
    print(f"URI: {Config.MONGODB_URI}")
    
    print(f"\n[LangSmith (Research Tracing)]")
    langsmith_key = os.getenv("LANGSMITH_API_KEY")
    langsmith_project = os.getenv("LANGCHAIN_PROJECT", "policy-monitoring")
    langsmith_tracing = os.getenv("LANGCHAIN_TRACING_V2", "false")
    print(f"API Key: {'*' * 20 if langsmith_key else 'Not set'}")
    print(f"Project: {langsmith_project}")
    print(f"Tracing Enabled: {langsmith_tracing}")
    
    print(f"\n[System Info]")
    import platform
    print(f"Python: {platform.python_version()}")
    print(f"Platform: {platform.system()} {platform.release()}")
    
    print("\n" + "-" * 60 + "\n")


def main():
    """Main entry point."""
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()
        
        if choice == "0":
            print("\n👋 Exiting... Goodbye!\n")
            sys.exit(0)
        elif choice == "1":
            populate_knowledge_graph()
        elif choice == "2":
            populate_knowledge_base()
        elif choice == "3":
            populate_all()
        elif choice == "4":
            start_dashboard()
        elif choice == "5":
            check_status()
        elif choice == "6":
            view_config()
        else:
            print("\n❌ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    # Check if .env exists
    if not os.path.exists(".env"):
        print("\n⚠️  WARNING: .env file not found!")
        print("Please create .env file from .env.example and configure your credentials.")
        print("\nRun: cp .env.example .env")
        print("Then edit .env with your API keys and database credentials.\n")
        response = input("Continue anyway? (y/n): ").strip().lower()
        if response != 'y':
            sys.exit(1)
    
    main()
