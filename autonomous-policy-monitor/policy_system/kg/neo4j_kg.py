"""
Neo4j Knowledge Graph for Policy Compliance Monitoring
Models relationships between policies, regulations, organizations, and requirements
"""
from typing import Dict, List, Optional, Any
import sys
import os
from neo4j import GraphDatabase

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

class Neo4jPolicyGraph:
    """Neo4j-based knowledge graph for policy compliance monitoring"""
    
    def __init__(self):
        self.driver = GraphDatabase.driver(
            NEO4J_URI, 
            auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
        )
        self._init_schema()
        
    def _init_schema(self):
        """Initialize Neo4j schema with constraints and indexes"""
        with self.driver.session() as session:
            # Create constraints for uniqueness
            session.run("""
                CREATE CONSTRAINT org_name IF NOT EXISTS
                FOR (o:Organization) REQUIRE o.name IS UNIQUE
            """)
            
            session.run("""
                CREATE CONSTRAINT policy_id IF NOT EXISTS
                FOR (p:Policy) REQUIRE p.id IS UNIQUE
            """)
            
            session.run("""
                CREATE CONSTRAINT regulation_id IF NOT EXISTS
                FOR (r:Regulation) REQUIRE r.id IS UNIQUE
            """)
            
            session.run("""
                CREATE CONSTRAINT dept_id IF NOT EXISTS
                FOR (d:Department) REQUIRE d.id IS UNIQUE
            """)
            
            # Create indexes for performance
            session.run("""
                CREATE INDEX policy_category IF NOT EXISTS
                FOR (p:Policy) ON (p.category)
            """)
            
            session.run("""
                CREATE INDEX policy_status IF NOT EXISTS
                FOR (p:Policy) ON (p.status)
            """)
            
    def close(self):
        """Close Neo4j connection"""
        self.driver.close()
    
    # ========== Organization Management ==========
    
    def add_organization(self, name: str, industry: str, size: int,
                        compliance_score: float = None, country: str = "USA") -> bool:
        """Add or update an organization in the knowledge graph"""
        with self.driver.session() as session:
            session.run("""
                MERGE (o:Organization {name: $name})
                SET o.industry = $industry,
                    o.size = $size,
                    o.compliance_score = $compliance_score,
                    o.country = $country
            """, name=name, industry=industry, size=size,
                 compliance_score=compliance_score, country=country)
            return True
    
    def get_organization_info(self, org_name: str) -> Optional[Dict]:
        """Get comprehensive organization information"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (o:Organization {name: $name})
                OPTIONAL MATCH (o)-[:HAS_POLICY]->(p:Policy)
                OPTIONAL MATCH (o)-[:MUST_COMPLY]->(r:Regulation)
                RETURN o.name as name,
                       o.industry as industry,
                       o.size as size,
                       o.compliance_score as compliance_score,
                       o.country as country,
                       count(DISTINCT p) as policy_count,
                       count(DISTINCT r) as regulation_count
            """, name=org_name)
            
            record = result.single()
            return dict(record) if record else None
    
    # ========== Policy Management ==========
    
    def add_policy(self, policy_id: str, title: str, organization: str,
                  category: str, effective_date: str, status: str = "active",
                  risk_level: str = "medium", description: str = "", 
                  version: str = "1.0") -> bool:
        """Add a policy to the knowledge graph"""
        with self.driver.session() as session:
            session.run("""
                MERGE (p:Policy {id: $policy_id})
                SET p.title = $title,
                    p.category = $category,
                    p.effective_date = $effective_date,
                    p.status = $status,
                    p.risk_level = $risk_level,
                    p.description = $description,
                    p.version = $version
                WITH p
                MATCH (o:Organization {name: $organization})
                MERGE (o)-[:HAS_POLICY]->(p)
            """, policy_id=policy_id, title=title, organization=organization,
                 category=category, effective_date=effective_date, status=status,
                 risk_level=risk_level, description=description, version=version)
            return True
    
    def get_policies_by_category(self, organization: str, category: str = None) -> List[Dict]:
        """Get policies by category for an organization"""
        with self.driver.session() as session:
            query = """
                MATCH (o:Organization {name: $organization})-[:HAS_POLICY]->(p:Policy)
                WHERE p.status = 'active'
            """
            params = {"organization": organization}
            
            if category:
                query += " AND p.category = $category"
                params["category"] = category
            
            query += """
                RETURN p.id AS id, p.title AS title, p.category AS category,
                       p.effective_date AS effective_date, p.risk_level AS risk_level
                ORDER BY p.effective_date DESC
            """
            
            result = session.run(query, **params)
            return [dict(record) for record in result]
    
    # ========== Regulation Management ==========
    
    def add_regulation(self, regulation_id: str = None, reg_id: str = None, 
                      name: str = "", authority: str = "",
                      jurisdiction: str = "", category: str = "", 
                      requirements: List[str] = None, effective_date: str = None,
                      **kwargs) -> bool:
        """Add a regulation to the knowledge graph"""
        # Handle both regulation_id and reg_id parameter names
        final_reg_id = regulation_id or reg_id
        if not final_reg_id:
            raise ValueError("Either regulation_id or reg_id must be provided")
        
        if requirements is None:
            requirements = []
        
        with self.driver.session() as session:
            query_params = {
                "reg_id": final_reg_id,
                "name": name,
                "authority": authority,
                "jurisdiction": jurisdiction,
                "category": category,
                "requirements": requirements
            }
            
            # Optionally add effective_date if provided
            if effective_date:
                query_params["effective_date"] = effective_date
                set_clause = """
                    SET r.name = $name,
                        r.authority = $authority,
                        r.jurisdiction = $jurisdiction,
                        r.category = $category,
                        r.requirements = $requirements,
                        r.effective_date = $effective_date
                """
            else:
                set_clause = """
                    SET r.name = $name,
                        r.authority = $authority,
                        r.jurisdiction = $jurisdiction,
                        r.category = $category,
                        r.requirements = $requirements
                """
            
            session.run(f"""
                MERGE (r:Regulation {{id: $reg_id}})
                {set_clause}
            """, **query_params)
            return True
    
    def link_policy_to_regulation(self, policy_id: str, regulation_id: str, 
                                  compliance_status: str = "implements") -> bool:
        """Create relationship between policy and regulation"""
        with self.driver.session() as session:
            session.run("""
                MATCH (p:Policy {id: $policy_id})
                MATCH (r:Regulation {id: $regulation_id})
                MERGE (p)-[rel:IMPLEMENTS]->(r)
                SET rel.compliance_status = $compliance_status
            """, policy_id=policy_id, regulation_id=regulation_id, 
                 compliance_status=compliance_status)
            return True
    
    def get_applicable_regulations(self, organization: str) -> List[Dict]:
        """Get all regulations applicable to an organization"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (o:Organization {name: $organization})-[:MUST_COMPLY]->(r:Regulation)
                RETURN r.id AS id, r.name AS name, r.authority AS authority,
                       r.jurisdiction AS jurisdiction, r.category AS category
            """, organization=organization)
            return [dict(record) for record in result]
    
    # ========== Policy Dependencies and Conflicts ==========
    
    def add_policy_dependency(self, policy_id: str, depends_on_id: str, 
                             dependency_type: str = "requires") -> bool:
        """Add dependency between policies"""
        with self.driver.session() as session:
            session.run("""
                MATCH (p1:Policy {id: $policy_id})
                MATCH (p2:Policy {id: $depends_on_id})
                MERGE (p1)-[:DEPENDS_ON {type: $dependency_type}]->(p2)
            """, policy_id=policy_id, depends_on_id=depends_on_id, dependency_type=dependency_type)
            return True
    
    def add_policy_conflict(self, policy_id1: str, policy_id2: str,
                           conflict_description: str, severity: str = "medium") -> bool:
        """Mark two policies as conflicting"""
        with self.driver.session() as session:
            session.run("""
                MATCH (p1:Policy {id: $policy_id1})
                MATCH (p2:Policy {id: $policy_id2})
                MERGE (p1)-[c:CONFLICTS_WITH]->(p2)
                SET c.description = $conflict_description,
                    c.severity = $severity
            """, policy_id1=policy_id1, policy_id2=policy_id2,
                 conflict_description=conflict_description, severity=severity)
            return True
    
    def find_policy_conflicts(self, organization: Optional[str] = None,
                              limit: int = 50) -> List[Dict]:
        """Find policy conflicts, optionally filtered by organization"""
        with self.driver.session() as session:
            if organization:
                result = session.run("""
                    MATCH (o:Organization {name: $organization})-[:HAS_POLICY]->(p1:Policy)
                    MATCH (p1)-[c:CONFLICTS_WITH]->(p2:Policy)
                    RETURN p1.id AS policy1_id, p1.title AS policy1_title,
                           p2.id AS policy2_id, p2.title AS policy2_title,
                           c.description AS conflict_description,
                           c.severity AS severity,
                           o.name AS organization
                    LIMIT $limit
                """, organization=organization, limit=limit)
            else:
                result = session.run("""
                    MATCH (p1:Policy)-[c:CONFLICTS_WITH]->(p2:Policy)
                    OPTIONAL MATCH (o:Organization)-[:HAS_POLICY]->(p1)
                    RETURN p1.id AS policy1_id, p1.title AS policy1_title,
                           p2.id AS policy2_id, p2.title AS policy2_title,
                           c.description AS conflict_description,
                           c.severity AS severity,
                           o.name AS organization
                    LIMIT $limit
                """, limit=limit)
            return [dict(record) for record in result]
    
    def get_policy_dependencies(self, policy_id: str) -> List[Dict]:
        """Get all dependencies for a policy"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Policy {id: $policy_id})-[d:DEPENDS_ON]->(dep:Policy)
                RETURN dep.id AS dependency_id, dep.title AS dependency_title,
                       d.type AS dependency_type
            """, policy_id=policy_id)
            return [dict(record) for record in result]
    
    # ========== Compliance Analysis ==========
    
    def calculate_compliance_score(self, organization: str) -> Dict:
        """Calculate overall compliance score for an organization"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (o:Organization {name: $organization})
                OPTIONAL MATCH (o)-[:HAS_POLICY]->(p:Policy)
                WHERE p.status = 'active'
                OPTIONAL MATCH (o)-[:HAS_VIOLATION]->(v:Violation)
                WHERE v.resolved = false
                RETURN count(DISTINCT p) as active_policies,
                       count(DISTINCT v) as open_violations,
                       o.compliance_score as current_score
            """, organization=organization)
            
            record = result.single()
            if record:
                data = dict(record)
                # Calculate score (simplified)
                active_policies = data.get('active_policies', 0)
                open_violations = data.get('open_violations', 0)
                if active_policies > 0:
                    data['calculated_score'] = max(0, (active_policies - open_violations * 2) / active_policies * 100)
                else:
                    data['calculated_score'] = 0
                return data
            return {}
    
    def add_violation(self, policy_id: str, violation_type: str = "", 
                     description: str = "", severity: str = "medium", 
                     date: str = None, detected_date: str = None,
                     status: str = "Open", violation_id: str = None,
                     organization: str = None) -> bool:
        """Add a policy violation"""
        # Generate violation_id if not provided
        if not violation_id:
            import uuid
            violation_id = f"VIO-{uuid.uuid4().hex[:8].upper()}"
        
        # Use date or detected_date
        final_date = date or detected_date or ""
        
        # Convert status to resolved boolean
        resolved = status.lower() in ["resolved", "closed"]
        
        with self.driver.session() as session:
            # First, get the organization from the policy if not provided
            if not organization:
                result = session.run("""
                    MATCH (o:Organization)-[:HAS_POLICY]->(p:Policy {id: $policy_id})
                    RETURN o.name as org_name
                    LIMIT 1
                """, policy_id=policy_id)
                record = result.single()
                organization = record["org_name"] if record else "Unknown"
            
            session.run("""
                MERGE (v:Violation {id: $violation_id})
                SET v.violation_type = $violation_type,
                    v.description = $description,
                    v.severity = $severity,
                    v.detected_date = $detected_date,
                    v.status = $status,
                    v.resolved = $resolved
                WITH v
                MATCH (p:Policy {id: $policy_id})
                MATCH (o:Organization {name: $organization})
                MERGE (p)-[:HAS_VIOLATION]->(v)
                MERGE (o)-[:HAS_VIOLATION]->(v)
            """, violation_id=violation_id, policy_id=policy_id, organization=organization,
                 violation_type=violation_type, description=description, 
                 severity=severity, detected_date=final_date, status=status, resolved=resolved)
            return True
    
    def get_violations(self, organization: str, resolved: bool = False) -> List[Dict]:
        """Get violations for an organization"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (o:Organization {name: $organization})-[:HAS_VIOLATION]->(v:Violation)
                WHERE v.resolved = $resolved
                MATCH (p:Policy)-[:HAS_VIOLATION]->(v)
                RETURN v.id AS violation_id, v.description AS description,
                       v.severity AS severity, v.detected_date AS detected_date,
                       p.title AS policy_title, p.id AS policy_id
                ORDER BY v.detected_date DESC
            """, organization=organization, resolved=resolved)
            return [dict(record) for record in result]
    
    # ========== Department Management ==========
    
    def add_department(self, organization: str, name: str, function: str = "",
                      head: str = "", policy_count: int = 0) -> bool:
        """Add a department to an organization"""
        dept_id = f"DEPT-{organization[:3].upper()}-{name.replace(' ', '')}"
        
        with self.driver.session() as session:
            session.run("""
                MERGE (d:Department {id: $dept_id})
                SET d.name = $name,
                    d.function = $function,
                    d.head = $head,
                    d.policy_count = $policy_count
                WITH d
                MATCH (o:Organization {name: $organization})
                MERGE (o)-[:HAS_DEPARTMENT]->(d)
            """, dept_id=dept_id, name=name, function=function, organization=organization,
                 head=head, policy_count=policy_count)
            return True
    
    def link_policy_to_department(self, policy_id: str, dept_id: str) -> bool:
        """Link a policy to a department"""
        with self.driver.session() as session:
            session.run("""
                MATCH (p:Policy {id: $policy_id})
                MATCH (d:Department {id: $dept_id})
                MERGE (p)-[:APPLIES_TO]->(d)
            """, policy_id=policy_id, dept_id=dept_id)
            return True
    
    # ========== Graph Analytics ==========
    
    def get_network_statistics(self) -> Dict:
        """Get overall knowledge graph statistics"""
        with self.driver.session() as session:
            result = session.run("""
                CALL {
                    MATCH (o:Organization)
                    RETURN count(o) AS organizations
                }
                CALL {
                    MATCH (p:Policy)
                    RETURN count(p) AS policies
                }
                CALL {
                    MATCH (r:Regulation)
                    RETURN count(r) AS regulations
                }
                CALL {
                    MATCH (d:Department)
                    RETURN count(d) AS departments
                }
                CALL {
                    MATCH (v:Violation)
                    RETURN count(v) AS violations
                }
                CALL {
                    MATCH (:Policy)-[c:CONFLICTS_WITH]->(:Policy)
                    RETURN count(c) AS conflicts
                }
                RETURN organizations,
                       policies,
                       regulations,
                       departments,
                       violations,
                       conflicts,
                       organizations AS total_organizations,
                       policies AS total_policies,
                       regulations AS total_regulations,
                       departments AS total_departments,
                       violations AS total_violations,
                       conflicts AS total_conflicts
            """)
            return dict(result.single())
    
    def find_policy_gaps(self, organization: str, regulation_category: str) -> List[Dict]:
        """Find regulatory gaps in policy coverage"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (o:Organization {name: $organization})-[:MUST_COMPLY]->(r:Regulation)
                WHERE r.category = $category
                OPTIONAL MATCH (o)-[:HAS_POLICY]->(p:Policy)-[:IMPLEMENTS]->(r)
                WITH r, collect(p) as implementing_policies
                WHERE size(implementing_policies) = 0
                RETURN r.id AS regulation_id, r.name AS regulation_name,
                       r.requirements AS missing_requirements
            """, organization=organization, category=regulation_category)
            return [dict(record) for record in result]
    
    def get_high_risk_policies(self, organization: Optional[str] = None,
                               limit: int = 10) -> List[Dict]:
        """Get high-risk policies, optionally filtered by organization"""
        with self.driver.session() as session:
            if organization:
                result = session.run("""
                    MATCH (o:Organization {name: $organization})-[:HAS_POLICY]->(p:Policy)
                    WHERE p.risk_level IN ['high', 'critical'] AND p.status = 'active'
                    OPTIONAL MATCH (p)-[:HAS_VIOLATION]->(v:Violation)
                    WHERE v.resolved = false
                    RETURN p.id AS policy_id, p.title AS title,
                           p.category AS category, p.risk_level AS risk_level,
                           p.effective_date AS effective_date,
                           count(v) AS open_violations,
                           o.name AS organization
                    ORDER BY open_violations DESC, effective_date DESC
                    LIMIT $limit
                """, organization=organization, limit=limit)
            else:
                result = session.run("""
                    MATCH (o:Organization)-[:HAS_POLICY]->(p:Policy)
                    WHERE p.risk_level IN ['high', 'critical'] AND p.status = 'active'
                    OPTIONAL MATCH (p)-[:HAS_VIOLATION]->(v:Violation)
                    WHERE v.resolved = false
                    RETURN p.id AS policy_id, p.title AS title,
                           p.category AS category, p.risk_level AS risk_level,
                           p.effective_date AS effective_date,
                           count(v) AS open_violations,
                           o.name AS organization
                    ORDER BY open_violations DESC, effective_date DESC
                    LIMIT $limit
                """, limit=limit)
            return [dict(record) for record in result]
