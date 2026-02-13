"""
Agent Definitions for Autonomous Policy Monitoring System

This module defines 6 specialized agents:
1. RoutingAgent: Query analysis and routing to appropriate specialist
2. PolicyClassificationAgent: Classifies policies by type, domain, and risk
3. ComplianceDetectionAgent: Detects compliance status and violations
4. ConflictAnalysisAgent: Identifies policy conflicts and inconsistencies
5. RiskAssessmentAgent: Evaluates risk levels and impact
6. RecommendationAgent: Provides actionable policy recommendations
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from typing import Dict, Any, List
import json

from ..utils.config import Config


class RoutingAgent:
    """
    Routes user queries to the appropriate specialist agent.
    Uses intent classification to determine query type.
    """
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest",
            google_api_key=Config.GEMINI_API_KEY,
            temperature=0.3
        )
        
        self.routing_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a routing agent for an autonomous policy compliance monitoring system.
            
Analyze the user's query and classify it into ONE of these categories:

1. POLICY_CLASSIFICATION: Questions about policy types, categories, domains, or organizational structure
   Examples: "What type of policy is this?", "Classify this data privacy policy", "What category does this belong to?"

2. COMPLIANCE_DETECTION: Questions about compliance status, violations, or adherence to regulations
   Examples: "Is this compliant?", "Check compliance status", "Are there any violations?", "Does this meet GDPR requirements?"

3. CONFLICT_ANALYSIS: Questions about policy conflicts, inconsistencies, or contradictions
   Examples: "Are these policies conflicting?", "Find policy conflicts", "Do these rules contradict?", "Check for inconsistencies"

4. RISK_ASSESSMENT: Questions about risk levels, impact analysis, or security assessment
   Examples: "What's the risk level?", "Assess the impact", "How severe is this?", "Calculate risk score"

5. RECOMMENDATION: Questions asking for suggestions, improvements, or remediation actions
   Examples: "What should we do?", "How to fix this?", "Recommend improvements", "Suggest policy changes"

6. GENERAL: General queries that don't fit above categories
   Examples: "What is this system?", "How does policy monitoring work?", "Tell me about regulations"

Respond with ONLY the category name (e.g., COMPLIANCE_DETECTION).
Do not add explanations or additional text."""),
            ("human", "{query}")
        ])
    
    def route(self, query: str) -> str:
        """
        Routes the query to appropriate agent based on intent.
        
        Returns:
            Agent category name (e.g., 'COMPLIANCE_DETECTION')
        """
        try:
            response = self.llm.invoke(
                self.routing_prompt.format_messages(query=query)
            )
            category = response.content.strip().upper()
            
            valid_categories = [
                "POLICY_CLASSIFICATION",
                "COMPLIANCE_DETECTION", 
                "CONFLICT_ANALYSIS",
                "RISK_ASSESSMENT",
                "RECOMMENDATION",
                "GENERAL"
            ]
            
            if category in valid_categories:
                return category
            else:
                return "GENERAL"
                
        except Exception as e:
            print(f"Routing error: {e}")
            return "GENERAL"


class PolicyClassificationAgent:
    """
    Classifies policies by type, domain, risk level, and organizational hierarchy.
    Uses knowledge graph to understand policy taxonomy.
    """
    
    def __init__(self, kg_client=None, kb_client=None):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest",
            google_api_key=Config.GEMINI_API_KEY,
            temperature=0.4
        )
        self.kg = kg_client
        self.kb = kb_client
        
        self.classification_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert policy classification agent for an autonomous compliance monitoring system.

Your role is to:
1. Analyze policy documents and classify them by type, category, and domain
2. Determine organizational hierarchy and ownership
3. Assess initial risk levels based on policy scope and impact
4. Extract key metadata like effective dates, version, status

Classification Framework:

POLICY TYPES:
- Corporate Policies: Internal organizational rules
- Regulatory Policies: Government/industry regulations
- Data Policies: Privacy, security, data governance
- HR Policies: Employee-related policies
- Financial Policies: Accounting, budgeting, procurement
- Operational Policies: Business processes, SOPs
- Compliance Policies: Audit, regulatory adherence
- Security Policies: Information security, access control

RISK LEVELS:
- CRITICAL: Affects core operations, high legal/financial impact
- HIGH: Significant organizational impact
- MEDIUM: Moderate impact, departmental scope
- LOW: Minimal impact, limited scope

POLICY STATUS:
- Active: Currently enforced
- Draft: Under development
- Deprecated: No longer in use
- Under Review: Being evaluated/updated

Use the knowledge graph context to understand existing policy relationships.
Use the knowledge base context to find similar policies for classification reference.

Provide detailed classification with reasoning."""),
            ("human", """Query: {query}

Knowledge Graph Context:
{kg_context}

Knowledge Base Context:
{kb_context}

Classify the policy and provide:
1. Policy Type (from the framework above)
2. Category/Domain
3. Risk Level with justification
4. Organizational ownership
5. Key metadata (effective date, status, version if available)
6. Classification confidence (High/Medium/Low) with reasoning""")
        ])
    
    def process(self, query: str, kg_context: str = "", kb_context: str = "") -> Dict[str, Any]:
        """
        Classifies the policy based on query and context.
        
        Returns:
            Dictionary with classification results
        """
        try:
            response = self.llm.invoke(
                self.classification_prompt.format_messages(
                    query=query,
                    kg_context=kg_context or "No graph context available",
                    kb_context=kb_context or "No knowledge base context available"
                )
            )
            
            return {
                "agent": "PolicyClassificationAgent",
                "response": response.content,
                "metadata": {
                    "kg_context_used": bool(kg_context),
                    "kb_context_used": bool(kb_context)
                }
            }
        except Exception as e:
            return {
                "agent": "PolicyClassificationAgent",
                "error": str(e),
                "response": "Error during policy classification. Please try again."
            }


class ComplianceDetectionAgent:
    """
    Detects compliance status against regulations and identifies violations.
    Uses knowledge graph to track compliance relationships.
    """
    
    def __init__(self, kg_client=None, kb_client=None):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest",
            google_api_key=Config.GEMINI_API_KEY,
            temperature=0.2
        )
        self.kg = kg_client
        self.kb = kb_client
        
        self.compliance_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert compliance detection agent for autonomous policy monitoring.

Your role is to:
1. Assess policy compliance against relevant regulations and standards
2. Identify specific violations or non-compliance issues
3. Evaluate severity of compliance gaps
4. Track compliance history and trends
5. Generate compliance scores and reports

Compliance Frameworks to Consider:
- GDPR (Data Privacy)
- HIPAA (Healthcare)
- SOX (Financial)
- ISO 27001 (Information Security)
- PCI DSS (Payment Card)
- Industry-specific regulations

Violation Severity:
- CRITICAL: Legal violations, immediate action required
- HIGH: Serious non-compliance, potential legal/financial risk
- MEDIUM: Compliance gaps needing attention
- LOW: Minor deviations, recommendations for improvement

Compliance Status:
- COMPLIANT: Fully meets requirements
- PARTIAL: Meets some requirements, gaps exist
- NON_COMPLIANT: Does not meet requirements
- UNKNOWN: Insufficient information to determine

Use knowledge graph to:
- Find regulatory requirements linked to policies
- Check for existing violation records
- Calculate compliance scores

Use knowledge base to:
- Search for compliance guidelines
- Find similar compliance cases
- Reference regulatory documents

Provide specific, actionable compliance findings with evidence."""),
            ("human", """Query: {query}

Knowledge Graph Context:
{kg_context}

Knowledge Base Context:
{kb_context}

Provide compliance analysis:
1. Compliance Status (COMPLIANT/PARTIAL/NON_COMPLIANT/UNKNOWN)
2. Applicable regulations and standards
3. Specific violations or gaps identified
4. Severity level for each finding
5. Compliance score (0-100) with calculation methodology
6. Evidence and reasoning for assessment""")
        ])
    
    def process(self, query: str, kg_context: str = "", kb_context: str = "") -> Dict[str, Any]:
        """
        Detects compliance status and violations.
        
        Returns:
            Dictionary with compliance analysis
        """
        try:
            response = self.llm.invoke(
                self.compliance_prompt.format_messages(
                    query=query,
                    kg_context=kg_context or "No graph context available",
                    kb_context=kb_context or "No knowledge base context available"
                )
            )
            
            return {
                "agent": "ComplianceDetectionAgent",
                "response": response.content,
                "metadata": {
                    "kg_context_used": bool(kg_context),
                    "kb_context_used": bool(kb_context)
                }
            }
        except Exception as e:
            return {
                "agent": "ComplianceDetectionAgent",
                "error": str(e),
                "response": "Error during compliance detection. Please try again."
            }


class ConflictAnalysisAgent:
    """
    Identifies conflicts, contradictions, and inconsistencies between policies.
    Uses knowledge graph to detect conflicting relationships.
    """
    
    def __init__(self, kg_client=None, kb_client=None):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest",
            google_api_key=Config.GEMINI_API_KEY,
            temperature=0.3
        )
        self.kg = kg_client
        self.kb = kb_client
        
        self.conflict_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert conflict analysis agent for policy compliance monitoring.

Your role is to:
1. Identify conflicts and contradictions between policies
2. Detect inconsistencies in policy language or requirements
3. Find overlapping or redundant policy provisions
4. Assess impact of policy conflicts on operations
5. Prioritize conflicts by severity

Conflict Types:

DIRECT CONFLICT:
- Policies have explicitly contradictory requirements
- One policy requires X, another prohibits X
- Severity: CRITICAL

PARTIAL CONFLICT:
- Policies have overlapping but inconsistent requirements
- Different interpretations of same area
- Severity: HIGH

IMPLICIT CONFLICT:
- Policies have different assumptions or approaches
- May conflict in certain scenarios
- Severity: MEDIUM

SEMANTIC CONFLICT:
- Similar terminology used with different meanings
- Ambiguous language causing confusion
- Severity: MEDIUM

TEMPORAL CONFLICT:
- Newer policy doesn't explicitly supersede older one
- Version conflicts
- Severity: LOW to MEDIUM

Use knowledge graph to:
- Find existing CONFLICTS_WITH relationships
- Check policy dependencies
- Identify policy hierarchies

Use knowledge base to:
- Search similar policy language
- Find historical conflict resolutions
- Reference conflict resolution guidelines

Provide specific conflict analysis with evidence and impact assessment."""),
            ("human", """Query: {query}

Knowledge Graph Context:
{kg_context}

Knowledge Base Context:
{kb_context}

Provide conflict analysis:
1. Conflicts identified (list each conflict)
2. Conflict type for each (Direct/Partial/Implicit/Semantic/Temporal)
3. Severity level (CRITICAL/HIGH/MEDIUM/LOW)
4. Policies involved in each conflict
5. Specific contradictory provisions with quotes/references
6. Operational impact of conflicts
7. Priority ranking for resolution""")
        ])
    
    def process(self, query: str, kg_context: str = "", kb_context: str = "") -> Dict[str, Any]:
        """
        Analyzes policy conflicts and inconsistencies.
        
        Returns:
            Dictionary with conflict analysis
        """
        try:
            response = self.llm.invoke(
                self.conflict_prompt.format_messages(
                    query=query,
                    kg_context=kg_context or "No graph context available",
                    kb_context=kb_context or "No knowledge base context available"
                )
            )
            
            return {
                "agent": "ConflictAnalysisAgent",
                "response": response.content,
                "metadata": {
                    "kg_context_used": bool(kg_context),
                    "kb_context_used": bool(kb_context)
                }
            }
        except Exception as e:
            return {
                "agent": "ConflictAnalysisAgent",
                "error": str(e),
                "response": "Error during conflict analysis. Please try again."
            }


class RiskAssessmentAgent:
    """
    Evaluates risk levels, impact analysis, and security vulnerabilities.
    Uses knowledge graph for holistic risk assessment.
    """
    
    def __init__(self, kg_client=None, kb_client=None):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest",
            google_api_key=Config.GEMINI_API_KEY,
            temperature=0.3
        )
        self.kg = kg_client
        self.kb = kb_client
        
        self.risk_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert risk assessment agent for policy compliance monitoring.

Your role is to:
1. Evaluate risk levels for policies and policy violations
2. Conduct impact analysis for policy changes
3. Assess security vulnerabilities in policy frameworks
4. Calculate comprehensive risk scores
5. Provide risk mitigation priorities

Risk Assessment Framework:

RISK DIMENSIONS:
- Legal Risk: Regulatory violations, lawsuits, penalties
- Financial Risk: Monetary losses, fines, revenue impact
- Operational Risk: Business disruption, inefficiency
- Reputational Risk: Brand damage, public trust
- Security Risk: Data breaches, unauthorized access
- Compliance Risk: Audit failures, certification loss

RISK LEVELS:
- CRITICAL (9-10): Immediate threat, severe consequences
- HIGH (7-8): Significant risk, urgent attention needed
- MEDIUM (4-6): Moderate risk, monitoring required
- LOW (1-3): Minimal risk, standard precautions

IMPACT ASSESSMENT:
- Scope: How many departments/users affected?
- Duration: Short-term or long-term impact?
- Reversibility: Can impact be mitigated?
- Cascading Effects: Will risk spread to other areas?

Risk Score Calculation:
Risk Score = (Probability × Impact × Severity) / Mitigation Factors

Use knowledge graph to:
- Find violation history and patterns
- Check policy dependencies for cascading risks
- Analyze network effects of policy changes

Use knowledge base to:
- Search historical risk incidents
- Find risk mitigation best practices
- Reference risk assessment guidelines

Provide quantitative and qualitative risk analysis with clear metrics."""),
            ("human", """Query: {query}

Knowledge Graph Context:
{kg_context}

Knowledge Base Context:
{kb_context}

Provide risk assessment:
1. Risk Level (CRITICAL/HIGH/MEDIUM/LOW) with numerical score (1-10)
2. Risk dimensions affected (Legal/Financial/Operational/Reputational/Security/Compliance)
3. Probability of risk materializing (percentage)
4. Potential impact if risk occurs (quantify where possible)
5. Affected stakeholders/departments
6. Cascading or secondary risks
7. Risk score calculation with formula breakdown
8. Time sensitivity (immediate/short-term/long-term)""")
        ])
    
    def process(self, query: str, kg_context: str = "", kb_context: str = "") -> Dict[str, Any]:
        """
        Assesses risk levels and impact.
        
        Returns:
            Dictionary with risk assessment
        """
        try:
            response = self.llm.invoke(
                self.risk_prompt.format_messages(
                    query=query,
                    kg_context=kg_context or "No graph context available",
                    kb_context=kb_context or "No knowledge base context available"
                )
            )
            
            return {
                "agent": "RiskAssessmentAgent",
                "response": response.content,
                "metadata": {
                    "kg_context_used": bool(kg_context),
                    "kb_context_used": bool(kb_context)
                }
            }
        except Exception as e:
            return {
                "agent": "RiskAssessmentAgent",
                "error": str(e),
                "response": "Error during risk assessment. Please try again."
            }


class RecommendationAgent:
    """
    Provides actionable recommendations for policy improvements and remediation.
    Uses knowledge base to suggest best practices.
    """
    
    def __init__(self, kg_client=None, kb_client=None):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest",
            google_api_key=Config.GEMINI_API_KEY,
            temperature=0.5
        )
        self.kg = kg_client
        self.kb = kb_client
        
        self.recommendation_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert recommendation agent for policy compliance monitoring.

Your role is to:
1. Provide actionable recommendations for policy improvements
2. Suggest remediation actions for violations and conflicts
3. Recommend process improvements for compliance
4. Propose policy updates to address gaps
5. Prioritize recommendations by impact and feasibility

Recommendation Framework:

RECOMMENDATION TYPES:

1. IMMEDIATE ACTIONS (Critical/High priority):
   - Fix regulatory violations
   - Resolve critical conflicts
   - Address security vulnerabilities
   - Remediate non-compliance

2. SHORT-TERM IMPROVEMENTS (1-3 months):
   - Update outdated policies
   - Implement missing controls
   - Enhance documentation
   - Train staff on compliance

3. LONG-TERM ENHANCEMENTS (3-12 months):
   - Redesign policy framework
   - Implement automation tools
   - Establish governance structures
   - Build compliance culture

RECOMMENDATION STRUCTURE:
For each recommendation provide:
- Title: Clear, actionable title
- Priority: CRITICAL/HIGH/MEDIUM/LOW
- Effort: High/Medium/Low (implementation complexity)
- Impact: High/Medium/Low (expected benefit)
- Timeline: Specific timeframe
- Stakeholders: Who should implement
- Steps: Detailed action steps
- Success Metrics: How to measure effectiveness
- Dependencies: Prerequisites or related recommendations

Use knowledge graph to:
- Identify gaps and missing relationships
- Find high-risk areas needing attention
- Understand policy dependencies for change impact

Use knowledge base to:
- Search for best practices
- Find successful remediation examples
- Reference compliance standards

Provide practical, prioritized recommendations with clear implementation guidance."""),
            ("human", """Query: {query}

Knowledge Graph Context:
{kg_context}

Knowledge Base Context:
{kb_context}

Provide recommendations:
1. List of recommendations (minimum 3, maximum 7)
2. For each recommendation include:
   - Title and description
   - Priority level (CRITICAL/HIGH/MEDIUM/LOW)
   - Effort required (High/Medium/Low)
   - Expected impact (High/Medium/Low)
   - Implementation timeline
   - Responsible stakeholders
   - Step-by-step action plan
   - Success metrics
   - Dependencies or prerequisites
3. Overall priority ranking
4. Quick wins (low effort, high impact items)
5. Summary with recommended action sequence""")
        ])
    
    def process(self, query: str, kg_context: str = "", kb_context: str = "") -> Dict[str, Any]:
        """
        Generates actionable recommendations.
        
        Returns:
            Dictionary with recommendations
        """
        try:
            response = self.llm.invoke(
                self.recommendation_prompt.format_messages(
                    query=query,
                    kg_context=kg_context or "No graph context available",
                    kb_context=kb_context or "No knowledge base context available"
                )
            )
            
            return {
                "agent": "RecommendationAgent",
                "response": response.content,
                "metadata": {
                    "kg_context_used": bool(kg_context),
                    "kb_context_used": bool(kb_context)
                }
            }
        except Exception as e:
            return {
                "agent": "RecommendationAgent",
                "error": str(e),
                "response": "Error generating recommendations. Please try again."
            }


class BasicQueryAgent:
    """
    Handles general queries about the system, policies, and compliance monitoring.
    Provides educational responses and system information.
    """
    
    def __init__(self, kg_client=None, kb_client=None):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest",
            google_api_key=Config.GEMINI_API_KEY,
            temperature=0.6
        )
        self.kg = kg_client
        self.kb = kb_client
        
        self.general_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful assistant for an Autonomous Policy Compliance Monitoring System.

This system uses:
- Multi-agent architecture with 5 specialized agents
- Neo4j knowledge graph to model policy relationships
- MongoDB vector database for semantic document search
- LangGraph for agent orchestration
- LangSmith for research traceability

Capabilities:
1. Policy Classification: Categorize policies by type, domain, and risk
2. Compliance Detection: Identify violations and compliance status
3. Conflict Analysis: Find policy conflicts and contradictions
4. Risk Assessment: Evaluate risk levels and impact
5. Recommendations: Suggest improvements and remediation actions

The system is designed for:
- Corporate policy management
- Regulatory compliance monitoring
- Policy portfolio optimization
- Risk-based compliance prioritization
- Autonomous compliance detection

Answer general questions helpfully and provide guidance on system usage.
If the query involves specific policy analysis, suggest the user rephrase to trigger specialist agents."""),
            ("human", """Query: {query}

Knowledge Graph Context:
{kg_context}

Knowledge Base Context:
{kb_context}

Provide a helpful response.""")
        ])
    
    def process(self, query: str, kg_context: str = "", kb_context: str = "") -> Dict[str, Any]:
        """
        Handles general queries.
        
        Returns:
            Dictionary with general response
        """
        try:
            response = self.llm.invoke(
                self.general_prompt.format_messages(
                    query=query,
                    kg_context=kg_context or "No specific context available",
                    kb_context=kb_context or "No specific context available"
                )
            )
            
            return {
                "agent": "BasicQueryAgent",
                "response": response.content,
                "metadata": {
                    "kg_context_used": bool(kg_context),
                    "kb_context_used": bool(kb_context)
                }
            }
        except Exception as e:
            return {
                "agent": "BasicQueryAgent",
                "error": str(e),
                "response": "I'm having trouble processing your query. Please try again or rephrase your question."
            }
