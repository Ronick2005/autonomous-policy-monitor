"""
Knowledge Graph Population Script for Autonomous Policy Monitoring System

Populates Neo4j with sample data:
- Organizations (companies, departments)
- Policies (corporate policies, regulations)
- Policy relationships (conflicts, dependencies)
- Violations and compliance records
"""

from policy_system.kg.neo4j_kg import Neo4jPolicyGraph
from policy_system.utils.config import Config
from datetime import datetime, timedelta


def populate_knowledge_graph():
    """Populate the knowledge graph with sample policy data."""
    
    print("🚀 Starting Knowledge Graph Population...")
    
    # Initialize knowledge graph
    kg = Neo4jPolicyGraph()
    
    try:
        # 1. Create Organizations
        print("\n📊 Creating Organizations...")
        
        organizations = [
            {
                "name": "TechCorp Global",
                "industry": "Technology",
                "size": "Enterprise",
                "country": "USA"
            },
            {
                "name": "FinanceSecure Inc",
                "industry": "Financial Services",
                "size": "Large",
                "country": "UK"
            },
            {
                "name": "HealthData Systems",
                "industry": "Healthcare",
                "size": "Medium",
                "country": "Germany"
            },
            {
                "name": "RetailChain Ltd",
                "industry": "Retail",
                "size": "Large",
                "country": "USA"
            }
        ]
        
        for org in organizations:
            kg.add_organization(**org)
            print(f"  ✓ Added organization: {org['name']}")
        
        # 2. Create Departments
        print("\n🏢 Creating Departments...")
        
        departments = [
            ("TechCorp Global", "Engineering", "Software Development"),
            ("TechCorp Global", "Security", "Information Security"),
            ("TechCorp Global", "Legal", "Legal and Compliance"),
            ("TechCorp Global", "HR", "Human Resources"),
            ("FinanceSecure Inc", "Risk Management", "Financial Risk"),
            ("FinanceSecure Inc", "Compliance", "Regulatory Compliance"),
            ("HealthData Systems", "Data Privacy", "Privacy and Security"),
            ("HealthData Systems", "Clinical", "Clinical Operations")
        ]
        
        for org_name, dept_name, dept_function in departments:
            kg.add_department(org_name, dept_name, dept_function)
            print(f"  ✓ Added department: {dept_name} at {org_name}")
        
        # 3. Create Policies
        print("\n📋 Creating Policies...")
        
        policies = [
            # TechCorp Global Policies
            {
                "policy_id": "POL-TC-001",
                "title": "Data Privacy and Protection Policy",
                "organization": "TechCorp Global",
                "category": "Data Privacy",
                "effective_date": "2024-01-01",
                "version": "2.1",
                "status": "Active",
                "risk_level": "CRITICAL"
            },
            {
                "policy_id": "POL-TC-002",
                "title": "Information Security Policy",
                "organization": "TechCorp Global",
                "category": "Security",
                "effective_date": "2023-06-15",
                "version": "3.0",
                "status": "Active",
                "risk_level": "CRITICAL"
            },
            {
                "policy_id": "POL-TC-003",
                "title": "Access Control Policy",
                "organization": "TechCorp Global",
                "category": "Security",
                "effective_date": "2023-09-01",
                "version": "1.5",
                "status": "Active",
                "risk_level": "HIGH"
            },
            {
                "policy_id": "POL-TC-004",
                "title": "Data Retention Policy",
                "organization": "TechCorp Global",
                "category": "Data Management",
                "effective_date": "2023-03-20",
                "version": "2.0",
                "status": "Active",
                "risk_level": "HIGH"
            },
            {
                "policy_id": "POL-TC-005",
                "title": "Remote Work Policy",
                "organization": "TechCorp Global",
                "category": "HR",
                "effective_date": "2023-01-10",
                "version": "1.0",
                "status": "Active",
                "risk_level": "MEDIUM"
            },
            
            # FinanceSecure Inc Policies
            {
                "policy_id": "POL-FS-001",
                "title": "Anti-Money Laundering Policy",
                "organization": "FinanceSecure Inc",
                "category": "Financial Compliance",
                "effective_date": "2024-01-01",
                "version": "4.2",
                "status": "Active",
                "risk_level": "CRITICAL"
            },
            {
                "policy_id": "POL-FS-002",
                "title": "Customer Data Protection Policy",
                "organization": "FinanceSecure Inc",
                "category": "Data Privacy",
                "effective_date": "2023-07-01",
                "version": "2.3",
                "status": "Active",
                "risk_level": "CRITICAL"
            },
            {
                "policy_id": "POL-FS-003",
                "title": "Transaction Monitoring Policy",
                "organization": "FinanceSecure Inc",
                "category": "Financial Compliance",
                "effective_date": "2023-11-15",
                "version": "1.8",
                "status": "Active",
                "risk_level": "HIGH"
            },
            
            # HealthData Systems Policies
            {
                "policy_id": "POL-HD-001",
                "title": "Patient Data Privacy Policy",
                "organization": "HealthData Systems",
                "category": "Healthcare Privacy",
                "effective_date": "2024-02-01",
                "version": "3.1",
                "status": "Active",
                "risk_level": "CRITICAL"
            },
            {
                "policy_id": "POL-HD-002",
                "title": "Electronic Health Records Access Policy",
                "organization": "HealthData Systems",
                "category": "Healthcare Security",
                "effective_date": "2023-08-20",
                "version": "2.5",
                "status": "Active",
                "risk_level": "CRITICAL"
            },
            
            # RetailChain Ltd Policies
            {
                "policy_id": "POL-RC-001",
                "title": "Customer Information Security Policy",
                "organization": "RetailChain Ltd",
                "category": "Data Security",
                "effective_date": "2023-10-01",
                "version": "1.4",
                "status": "Active",
                "risk_level": "HIGH"
            },
            {
                "policy_id": "POL-RC-002",
                "title": "Payment Card Data Policy",
                "organization": "RetailChain Ltd",
                "category": "Payment Security",
                "effective_date": "2024-01-15",
                "version": "2.0",
                "status": "Active",
                "risk_level": "CRITICAL"
            }
        ]
        
        for policy in policies:
            # Normalize status and risk_level to lowercase
            if 'status' in policy:
                policy['status'] = policy['status'].lower()
            if 'risk_level' in policy:
                policy['risk_level'] = policy['risk_level'].lower()
            
            kg.add_policy(**policy)
            print(f"  ✓ Added policy: {policy['title']}")
        
        # 4. Create Regulations
        print("\n⚖️ Creating Regulations...")
        
        regulations = [
            {
                "regulation_id": "REG-GDPR",
                "name": "General Data Protection Regulation",
                "jurisdiction": "European Union",
                "effective_date": "2018-05-25",
                "authority": "European Commission",
                "category": "Data Privacy"
            },
            {
                "regulation_id": "REG-CCPA",
                "name": "California Consumer Privacy Act",
                "jurisdiction": "California, USA",
                "effective_date": "2020-01-01",
                "authority": "California Attorney General",
                "category": "Data Privacy"
            },
            {
                "regulation_id": "REG-HIPAA",
                "name": "Health Insurance Portability and Accountability Act",
                "jurisdiction": "USA",
                "effective_date": "1996-08-21",
                "authority": "US Department of Health",
                "category": "Healthcare Privacy"
            },
            {
                "regulation_id": "REG-SOX",
                "name": "Sarbanes-Oxley Act",
                "jurisdiction": "USA",
                "effective_date": "2002-07-30",
                "authority": "US Congress",
                "category": "Financial Compliance"
            },
            {
                "regulation_id": "REG-PCI-DSS",
                "name": "Payment Card Industry Data Security Standard",
                "jurisdiction": "International",
                "effective_date": "2004-12-15",
                "authority": "PCI Security Standards Council",
                "category": "Payment Security"
            },
            {
                "regulation_id": "REG-ISO27001",
                "name": "ISO/IEC 27001 Information Security",
                "jurisdiction": "International",
                "effective_date": "2013-10-01",
                "authority": "ISO",
                "category": "Information Security"
            }
        ]
        
        for regulation in regulations:
            kg.add_regulation(**regulation)
            print(f"  ✓ Added regulation: {regulation['name']}")
        
        # 5. Link Policies to Regulations
        print("\n🔗 Linking Policies to Regulations...")
        
        policy_regulation_links = [
            ("POL-TC-001", "REG-GDPR", "Full Implementation"),
            ("POL-TC-001", "REG-CCPA", "Partial Compliance"),
            ("POL-TC-002", "REG-ISO27001", "Certification Requirement"),
            ("POL-TC-004", "REG-GDPR", "Data Retention Requirements"),
            ("POL-FS-001", "REG-SOX", "Financial Controls"),
            ("POL-FS-002", "REG-GDPR", "Customer Data Protection"),
            ("POL-HD-001", "REG-HIPAA", "Patient Privacy Requirements"),
            ("POL-HD-001", "REG-GDPR", "Healthcare Data Protection"),
            ("POL-HD-002", "REG-HIPAA", "Access Control Requirements"),
            ("POL-RC-002", "REG-PCI-DSS", "Payment Card Security")
        ]
        
        for policy_id, regulation_id, compliance_status in policy_regulation_links:
            kg.link_policy_to_regulation(policy_id, regulation_id, compliance_status)
            print(f"  ✓ Linked {policy_id} to {regulation_id}")
        
        # 6. Create Policy Dependencies
        print("\n🔀 Creating Policy Dependencies...")
        
        dependencies = [
            ("POL-TC-003", "POL-TC-002", "Access control depends on security policy"),
            ("POL-TC-004", "POL-TC-001", "Data retention must align with privacy policy"),
            ("POL-FS-003", "POL-FS-001", "Transaction monitoring supports AML compliance"),
            ("POL-HD-002", "POL-HD-001", "Access control implements privacy requirements")
        ]
        
        for source_id, target_id, reason in dependencies:
            kg.add_policy_dependency(source_id, target_id, reason)
            print(f"  ✓ Added dependency: {source_id} → {target_id}")
        
        # 7. Create Policy Conflicts
        print("\n⚔️ Creating Policy Conflicts...")
        
        conflicts = [
            ("POL-TC-004", "POL-TC-001", "HIGH", 
             "Data retention period conflicts with right to be forgotten"),
            ("POL-TC-005", "POL-TC-002", "MEDIUM",
             "Remote work policy may conflict with on-premises security requirements"),
            ("POL-FS-002", "POL-FS-003", "MEDIUM",
             "Data minimization conflicts with extensive transaction monitoring")
        ]
        
        for policy1_id, policy2_id, severity, description in conflicts:
            kg.add_policy_conflict(policy1_id, policy2_id, severity, description)
            print(f"  ✓ Added conflict: {policy1_id} ⚔️ {policy2_id}")
        
        # 8. Add Violations
        print("\n🚨 Adding Violations...")
        
        violations = [
            {
                "policy_id": "POL-TC-001",
                "violation_type": "Data Access Violation",
                "severity": "HIGH",
                "date": (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d"),
                "description": "Unauthorized access to customer personal data",
                "status": "Open"
            },
            {
                "policy_id": "POL-TC-002",
                "violation_type": "Security Configuration",
                "severity": "MEDIUM",
                "date": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                "description": "Weak password policy on development servers",
                "status": "Resolved"
            },
            {
                "policy_id": "POL-FS-001",
                "violation_type": "AML Monitoring Gap",
                "severity": "CRITICAL",
                "date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
                "description": "Suspicious transactions not flagged for review",
                "status": "Open"
            },
            {
                "policy_id": "POL-HD-001",
                "violation_type": "Privacy Breach",
                "severity": "CRITICAL",
                "date": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
                "description": "Patient records accessed without authorization",
                "status": "Under Investigation"
            }
        ]
        
        for violation in violations:
            # Normalize severity to lowercase
            if 'severity' in violation:
                violation['severity'] = violation['severity'].lower()
            
            kg.add_violation(**violation)
            print(f"  ✓ Added violation: {violation['violation_type']} for {violation['policy_id']}")
        
        # 9. Verify Network Statistics
        print("\n📊 Knowledge Graph Statistics:")
        stats = kg.get_network_statistics()
        if stats:
            print(f"  Organizations: {stats.get('total_organizations', 0)}")
            print(f"  Departments: {stats.get('total_departments', 0)}")
            print(f"  Policies: {stats.get('total_policies', 0)}")
            print(f"  Regulations: {stats.get('total_regulations', 0)}")
            print(f"  Violations: {stats.get('total_violations', 0)}")
            print(f"  Policy Conflicts: {stats.get('total_conflicts', 0)}")
        
        print("\n✅ Knowledge Graph Population Complete!")
        
    except Exception as e:
        print(f"\n❌ Error during population: {e}")
        raise
    finally:
        kg.close()


if __name__ == "__main__":
    populate_knowledge_graph()
