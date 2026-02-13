"""
  Quick Start Guide
  Autonomous Policy Monitoring System
"""

## 🚀 5-Minute Quick Start

Get the system running before your review with these steps.

### Prerequisites

- Python 3.9+
- Neo4j Database (local or cloud)
- MongoDB Database (local or cloud)
- Google Gemini API Key

### Step 1: Install Dependencies (2 minutes)

```bash
cd autonomous-policy-monitor

# Activate virtual environment
c:\Users\Ronick\Documents\fin_project\.venv\Scripts\Activate.ps1

# Install all packages (uses Python 3.11)
pip install -r requirements.txt
```

**✅ Installation successful if you see:**
```
Successfully installed langchain-google-genai-0.0.1 google-generativeai-0.3.2 ...
```

**⚠️ Important:** The system uses specific package versions for compatibility:
- `langchain-google-genai==0.0.1` (NOT latest version)
- `google-generativeai==0.3.2`
- `langchain-core==0.3.17`

### Step 2: Configure Environment (1 minute)

Create `.env` file in the project root:

```bash
# Copy from template
cp .env.example .env
```

Edit `.env` with your credentials:

```
# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# Neo4j Database
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# MongoDB Database
MONGODB_URI=mongodb://localhost:27017/

# LangSmith (for research tracing)
LANGSMITH_API_KEY=your_langsmith_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=autonomous-policy-monitoring
```

**Where to get API keys:**
- Gemini API: https://makersuite.google.com/app/apikey
- LangSmith: https://smith.langchain.com/ (sign up → API Keys)

### Step 3: Initialize Databases (30 seconds)

```bash
# Populate Knowledge Graph (Neo4j)
python populate_knowledge_graph.py

# Populate Knowledge Base (MongoDB)
python populate_knowledge_base.py
```

You should see:
```
✅ Knowledge Graph Population Complete!
  Organizations: 4
  Policies: 12
  Regulations: 6
  Violations: 4

✅ Knowledge Base Population Complete!
  Total documents added:
  Policies: 4
  Regulations: 2
  Guidelines: 2
```

### Step 4: Launch Dashboard (30 seconds)

```bash
streamlit run streamlit_app.py
```

The dashboard will open at: `http://localhost:8501`

**Login with demo credentials:**
- Username: `researcher`
- Password: `research123`

---

## 🎯 Quick Demo Queries

Once logged in, try these queries:

### 1. Policy Classification
```
Classify the data privacy policy for our organization
```

### 2. Compliance Detection
```
Is our data retention policy compliant with GDPR?
```

### 3. Conflict Analysis
```
Are there any conflicts between our security and privacy policies?
```

### 4. Risk Assessment
```
What is the risk level of our current access control policy?
```

### 5. Recommendations
```
Recommend improvements to our compliance framework
```

---

## 🔍 Verify LangSmith Tracing

1. Go to [LangSmith Dashboard](https://smith.langchain.com/)
2. Select your project: `autonomous-policy-monitoring`
3. View execution traces for each query
4. Show this during your review to demonstrate research traceability!

---

## 📊 Review Preparation Checklist

Before your review, verify these work:

- [ ] Dashboard loads successfully
- [ ] Can login with demo credentials
- [ ] Sample queries return responses
- [ ] Agent metadata shows in execution details
- [ ] LangSmith traces are visible (if configured)
- [ ] Knowledge graph statistics display correctly
- [ ] All 6 agents are listed in sidebar

---

## 🐛 Quick Troubleshooting

**Problem: "No module named 'policy_system'"**
- Solution: Run `pip install -e .` in project root, or ensure you're in the correct directory

**Problem: "Neo4j connection failed"**
- Check Neo4j is running: `neo4j status` (or check Neo4j Desktop)
- Verify URI and credentials in `.env`
- Test connection: Try opening Neo4j Browser

**Problem: "MongoDB connection failed"**
- Check MongoDB is running: `mongod --version`
- Verify connection string in `.env`
- For MongoDB Atlas, check IP whitelist

**Problem: "Gemini API error"**
- Verify API key is correct in `.env`
- Check API is enabled in Google Cloud Console
- Ensure API quota hasn't been exceeded

**Problem: "No data showing in dashboard"**
- Re-run population scripts
- Check console for errors during population
- Verify database connections

---

## 🎓 Research Paper Tips

**For your review, emphasize:**

1. **Multi-Agent Architecture**: 5 specialized agents (Classification, Compliance, Conflict, Risk, Recommendation) + routing agent
2. **Knowledge Graph Integration**: Neo4j models policy relationships, conflicts, and dependencies
3. **Vector Database**: MongoDB with semantic search for policy documents
4. **Research Traceability**: LangSmith integration for explainable AI
5. **Novel Contribution**: Autonomous detection of policy conflicts using graph-based reasoning

**Demo Flow:**
1. Show dashboard with system overview
2. Run a conflict analysis query
3. Display execution metadata (agents used, KG/KB context)
4. Show LangSmith trace (if configured)
5. Explain how this enables automated policy compliance monitoring

---

## 📚 Architecture Overview (For Quick Reference)

```
User Query
    ↓
Routing Agent (Intent Classification)
    ↓
Context Retrieval
    ├── Knowledge Graph (Neo4j): Policy relationships, conflicts
    └── Knowledge Base (MongoDB): Semantic document search
    ↓
Specialist Agent Execution
    ├── PolicyClassificationAgent
    ├── ComplianceDetectionAgent
    ├── ConflictAnalysisAgent
    ├── RiskAssessmentAgent
    └── RecommendationAgent
    ↓
Response Generation
    ↓
LangSmith Tracing (Research Audit Trail)
```

---

## 🆘 Need Help?

- Check `README.md` for complete documentation
- Review `RESEARCH_PAPER_OUTLINE.md` for paper structure
- Examine agent code in `policy_system/agents/agent_definitions.py`
- Look at orchestrator flow in `policy_system/agents/orchestrator.py`

---

**Good luck with your review tomorrow! 🎉**
