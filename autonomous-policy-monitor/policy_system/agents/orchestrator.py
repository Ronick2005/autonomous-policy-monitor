"""
LangGraph Orchestrator for Autonomous Policy Monitoring System

This orchestrator:
1. Routes queries to appropriate specialist agents
2. Retrieves context from Knowledge Graph (Neo4j) and Knowledge Base (MongoDB)
3. Manages multi-agent workflow with state machine
4. Integrates LangSmith for research traceability and explainability
"""

from typing import TypedDict, Annotated, List, Dict, Any
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
import json

from .agent_definitions import (
    RoutingAgent,
    PolicyClassificationAgent,
    ComplianceDetectionAgent,
    ConflictAnalysisAgent,
    RiskAssessmentAgent,
    RecommendationAgent,
    BasicQueryAgent
)
from ..kg.neo4j_kg import Neo4jPolicyGraph
from ..kb.mongodb_kb import MongoPolicyKB


class PolicyMonitoringState(TypedDict):
    """
    State schema for the policy monitoring workflow.
    
    Tracks:
    - User query and intent
    - Knowledge graph and knowledge base context
    - Agent routing decisions
    - Intermediate and final responses
    - Metadata for research tracing
    """
    query: str
    intent: str
    kg_context: str
    kb_context: str
    agent_route: str
    intermediate_results: List[Dict[str, Any]]
    final_response: str
    metadata: Dict[str, Any]


class PolicyMonitoringOrchestrator:
    """
    Orchestrates multi-agent workflow for policy compliance monitoring.
    
    Workflow:
    1. Route: Classify query intent
    2. Retrieve Context: Get relevant data from KG and KB
    3. Execute Agent: Run specialist agent
    4. Return Response: Format final output
    """
    
    def __init__(self, neo4j_uri: str = None, neo4j_user: str = None, neo4j_password: str = None,
                 mongodb_uri: str = None):
        """
        Initialize orchestrator with knowledge graph and knowledge base connections.
        Note: Parameters are ignored as connections are configured via environment variables.
        """
        # Initialize knowledge systems
        self.kg = Neo4jPolicyGraph()
        self.kb = MongoPolicyKB()
        
        # Initialize agents
        self.routing_agent = RoutingAgent()
        self.policy_classification_agent = PolicyClassificationAgent(self.kg, self.kb)
        self.compliance_detection_agent = ComplianceDetectionAgent(self.kg, self.kb)
        self.conflict_analysis_agent = ConflictAnalysisAgent(self.kg, self.kb)
        self.risk_assessment_agent = RiskAssessmentAgent(self.kg, self.kb)
        self.recommendation_agent = RecommendationAgent(self.kg, self.kb)
        self.basic_query_agent = BasicQueryAgent(self.kg, self.kb)
        
        # Build workflow graph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """
        Builds the LangGraph state machine for agent orchestration.
        
        Workflow nodes:
        - route_query: Determine intent and route to agent
        - retrieve_kg_context: Get knowledge graph context
        - retrieve_kb_context: Get knowledge base context
        - execute_agent: Run specialist agent
        - format_response: Prepare final output
        """
        workflow = StateGraph(PolicyMonitoringState)
        
        # Add nodes
        workflow.add_node("route_query", self._route_query)
        workflow.add_node("retrieve_context", self._retrieve_context)
        workflow.add_node("execute_agent", self._execute_agent)
        workflow.add_node("format_response", self._format_response)
        
        # Define edges
        workflow.set_entry_point("route_query")
        workflow.add_edge("route_query", "retrieve_context")
        workflow.add_edge("retrieve_context", "execute_agent")
        workflow.add_edge("execute_agent", "format_response")
        workflow.add_edge("format_response", END)
        
        return workflow.compile()
    
    def _route_query(self, state: PolicyMonitoringState) -> PolicyMonitoringState:
        """
        Route the query to appropriate agent based on intent classification.
        """
        query = state["query"]
        
        # Use routing agent to classify intent
        intent = self.routing_agent.route(query)
        
        # Map intent to agent route
        agent_route_map = {
            "POLICY_CLASSIFICATION": "policy_classification",
            "COMPLIANCE_DETECTION": "compliance_detection",
            "CONFLICT_ANALYSIS": "conflict_analysis",
            "RISK_ASSESSMENT": "risk_assessment",
            "RECOMMENDATION": "recommendation",
            "GENERAL": "general"
        }
        
        agent_route = agent_route_map.get(intent, "general")
        
        # Update state
        state["intent"] = intent
        state["agent_route"] = agent_route
        state["metadata"] = {
            "routing_decision": intent,
            "agent_selected": agent_route,
            "query_length": len(query)
        }
        
        return state
    
    def _retrieve_context(self, state: PolicyMonitoringState) -> PolicyMonitoringState:
        """
        Retrieve relevant context from Knowledge Graph and Knowledge Base.
        """
        query = state["query"]
        intent = state["intent"]
        
        # Knowledge Graph Context
        kg_context_parts = []
        
        try:
            # Get network statistics
            stats = self.kg.get_network_statistics()
            if stats:
                kg_context_parts.append(f"Knowledge Graph Statistics:\n{json.dumps(stats, indent=2)}")
            
            # Intent-specific KG queries
            if intent == "COMPLIANCE_DETECTION":
                # Get high-risk policies and violations
                high_risk = self.kg.get_high_risk_policies(limit=5)
                if high_risk:
                    kg_context_parts.append(f"\nHigh-Risk Policies:\n{json.dumps(high_risk, indent=2)}")
                
            elif intent == "CONFLICT_ANALYSIS":
                # Get policy conflicts
                conflicts = self.kg.find_policy_conflicts()
                if conflicts:
                    kg_context_parts.append(f"\nKnown Policy Conflicts:\n{json.dumps(conflicts, indent=2)}")
            
            elif intent == "RISK_ASSESSMENT":
                # Get violations and high-risk policies
                high_risk = self.kg.get_high_risk_policies(limit=5)
                if high_risk:
                    kg_context_parts.append(f"\nHigh-Risk Policies:\n{json.dumps(high_risk, indent=2)}")
            
            kg_context = "\n".join(kg_context_parts) if kg_context_parts else "No specific graph context available"
            
        except Exception as e:
            kg_context = f"Error retrieving knowledge graph context: {str(e)}"
        
        # Knowledge Base Context (semantic search)
        kb_context = ""
        
        try:
            # Semantic search in knowledge base
            search_results = self.kb.semantic_search(query, k=3)
            
            if search_results:
                kb_context_parts = ["Relevant Documents from Knowledge Base:\n"]
                for i, doc in enumerate(search_results, 1):
                    content = doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content
                    metadata = doc.metadata
                    kb_context_parts.append(
                        f"\n{i}. {metadata.get('title', 'Untitled')}\n"
                        f"   Type: {metadata.get('type', 'Unknown')}\n"
                        f"   Content: {content}\n"
                    )
                kb_context = "".join(kb_context_parts)
            else:
                kb_context = "No relevant documents found in knowledge base"
                
        except Exception as e:
            kb_context = f"Error retrieving knowledge base context: {str(e)}"
        
        # Context quality flags (used to prevent ungrounded responses)
        has_kb_evidence = kb_context.startswith("Relevant Documents from Knowledge Base")
        has_kg_evidence = (
            "High-Risk Policies:" in kg_context or
            "Known Policy Conflicts:" in kg_context
        )

        # Update state
        state["kg_context"] = kg_context
        state["kb_context"] = kb_context
        state["metadata"]["kg_context_length"] = len(kg_context)
        state["metadata"]["kb_context_length"] = len(kb_context)
        state["metadata"]["has_kb_evidence"] = has_kb_evidence
        state["metadata"]["has_kg_evidence"] = has_kg_evidence
        state["metadata"]["is_grounded"] = has_kb_evidence or has_kg_evidence
        
        return state
    
    def _execute_agent(self, state: PolicyMonitoringState) -> PolicyMonitoringState:
        """
        Execute the specialist agent based on routing decision.
        """
        query = state["query"]
        kg_context = state["kg_context"]
        kb_context = state["kb_context"]
        agent_route = state["agent_route"]
        
        # Select agent
        agent_map = {
            "policy_classification": self.policy_classification_agent,
            "compliance_detection": self.compliance_detection_agent,
            "conflict_analysis": self.conflict_analysis_agent,
            "risk_assessment": self.risk_assessment_agent,
            "recommendation": self.recommendation_agent,
            "general": self.basic_query_agent
        }
        
        agent = agent_map.get(agent_route, self.basic_query_agent)

        # Guardrail: do not generate answers without KB/KG evidence
        if not state.get("metadata", {}).get("is_grounded", False):
            result = {
                "agent": "grounding_guard",
                "response": (
                    "I couldn't find enough supporting evidence in the Knowledge Base or "
                    "Knowledge Graph to answer reliably. Please repopulate KB/KG or refine "
                    "the query with organization/policy identifiers."
                )
            }
            state["intermediate_results"] = [result]
            state["metadata"]["agent_execution_status"] = "skipped_no_evidence"
            state["metadata"]["agent_used"] = "grounding_guard"
            return state
        
        # Execute agent
        try:
            result = agent.process(query, kg_context, kb_context)
            state["intermediate_results"] = [result]
            state["metadata"]["agent_execution_status"] = "success"
            state["metadata"]["agent_used"] = result.get("agent", agent_route)
            
        except Exception as e:
            result = {
                "agent": agent_route,
                "error": str(e),
                "response": f"Error executing {agent_route} agent. Please try again."
            }
            state["intermediate_results"] = [result]
            state["metadata"]["agent_execution_status"] = "error"
            state["metadata"]["error"] = str(e)
        
        return state
    
    def _format_response(self, state: PolicyMonitoringState) -> PolicyMonitoringState:
        """
        Format the final response for the user.
        """
        intermediate_results = state["intermediate_results"]
        
        if intermediate_results:
            result = intermediate_results[0]
            response = result.get("response", "No response generated")
            
            # Add metadata footer for research traceability
            footer = f"\n\n---\n**Agent Used:** {result.get('agent', 'Unknown')}\n"
            footer += f"**Intent Detected:** {state['intent']}\n"
            footer += f"**KG Context:** {'Yes' if state.get('metadata', {}).get('has_kg_evidence', False) else 'No'}\n"
            footer += f"**KB Context:** {'Yes' if state.get('metadata', {}).get('has_kb_evidence', False) else 'No'}\n"
            footer += f"**Grounded Response:** {'Yes' if state.get('metadata', {}).get('is_grounded', False) else 'No'}\n"
            
            final_response = response + footer
        else:
            final_response = "No response generated. Please try again."
        
        state["final_response"] = final_response
        state["metadata"]["response_length"] = len(final_response)
        
        return state
    
    def process_query(self, query: str, user_id: str = None) -> Dict[str, Any]:
        """
        Process a user query through the multi-agent workflow.
        
        Args:
            query: User's policy compliance query
            user_id: Optional user identifier for research tracing
        
        Returns:
            Dictionary with response and metadata
        """
        # Initialize state
        initial_state = {
            "query": query,
            "intent": "",
            "kg_context": "",
            "kb_context": "",
            "agent_route": "",
            "intermediate_results": [],
            "final_response": "",
            "metadata": {
                "user_id": user_id,
                "query": query
            }
        }
        
        # Run workflow
        try:
            final_state = self.graph.invoke(initial_state)
            
            return {
                "response": final_state["final_response"],
                "metadata": final_state["metadata"],
                "success": True
            }
            
        except Exception as e:
            return {
                "response": f"Error processing query: {str(e)}",
                "metadata": {
                    "error": str(e),
                    "user_id": user_id
                },
                "success": False
            }
    
    def close(self):
        """
        Close database connections.
        """
        try:
            self.kg.close()
            print("Knowledge graph connection closed")
        except Exception as e:
            print(f"Error closing knowledge graph: {e}")
        
        try:
            self.kb.close()
            print("Knowledge base connection closed")
        except Exception as e:
            print(f"Error closing knowledge base: {e}")


def create_orchestrator(neo4j_uri: str = None, neo4j_user: str = None, 
                       neo4j_password: str = None, mongodb_uri: str = None) -> PolicyMonitoringOrchestrator:
    """
    Factory function to create and initialize the orchestrator.
    
    Args:
        neo4j_uri: Neo4j database URI
        neo4j_user: Neo4j username
        neo4j_password: Neo4j password
        mongodb_uri: MongoDB connection URI
    
    Returns:
        Initialized PolicyMonitoringOrchestrator
    """
    return PolicyMonitoringOrchestrator(
        neo4j_uri=neo4j_uri,
        neo4j_user=neo4j_user, 
        neo4j_password=neo4j_password,
        mongodb_uri=mongodb_uri
    )
