"""
Knowledge Base Population Script for Autonomous Policy Monitoring System

Populates MongoDB with sample documents:
- Policy documents
- Regulatory texts
- Compliance guidelines
- Best practice documents
"""

from policy_system.kb.mongodb_kb import MongoPolicyKB
from policy_system.utils.config import Config


def populate_knowledge_base():
    """Populate the knowledge base with sample policy documents."""
    
    print("🚀 Starting Knowledge Base Population...")
    
    # Initialize knowledge base
    kb = MongoPolicyKB()
    
    try:
        # 1. Add Policy Documents
        print("\n📋 Adding Policy Documents...")
        
        policy_documents = [
            {
                "title": "Data Privacy and Protection Policy - TechCorp Global",
                "content": """
                DATA PRIVACY AND PROTECTION POLICY
                
                Policy ID: POL-TC-001
                Version: 2.1
                Effective Date: January 1, 2024
                Organization: TechCorp Global
                
                1. PURPOSE
                This policy establishes the framework for protecting personal data and ensuring compliance
                with data protection regulations including GDPR and CCPA.
                
                2. SCOPE
                This policy applies to all employees, contractors, and third parties who process personal
                data on behalf of TechCorp Global.
                
                3. DATA PROTECTION PRINCIPLES
                - Lawfulness, fairness, and transparency
                - Purpose limitation
                - Data minimization
                - Accuracy
                - Storage limitation
                - Integrity and confidentiality
                
                4. DATA SUBJECT RIGHTS
                TechCorp Global respects and facilitates the following rights:
                - Right to access
                - Right to rectification
                - Right to erasure (right to be forgotten)
                - Right to restrict processing
                - Right to data portability
                - Right to object
                
                5. DATA RETENTION
                Personal data shall be retained only for as long as necessary for the purposes for which
                it was collected. Standard retention periods:
                - Customer data: 7 years after last transaction
                - Employee data: 10 years after termination
                - Marketing data: Until consent is withdrawn
                
                6. DATA SECURITY
                Technical and organizational measures include:
                - Encryption at rest and in transit
                - Access controls and authentication
                - Regular security assessments
                - Incident response procedures
                
                7. DATA BREACH NOTIFICATION
                In the event of a data breach affecting personal data, TechCorp Global will notify
                affected individuals and relevant authorities within 72 hours.
                
                8. INTERNATIONAL DATA TRANSFERS
                Transfers to countries outside the EU/EEA will be subject to appropriate safeguards
                such as Standard Contractual Clauses or adequacy decisions.
                
                9. COMPLIANCE AND REVIEW
                This policy will be reviewed annually and updated as necessary to reflect changes in
                regulations and best practices.
                """,
                "category": "Data Privacy",
                "organization": "TechCorp Global",
                "effective_date": "2024-01-01",
                "version": "2.1",
                "tags": ["gdpr", "privacy", "data protection", "compliance"]
            },
            {
                "title": "Information Security Policy - TechCorp Global",
                "content": """
                INFORMATION SECURITY POLICY
                
                Policy ID: POL-TC-002
                Version: 3.0
                Effective Date: June 15, 2023
                Organization: TechCorp Global
                
                1. OBJECTIVE
                To protect TechCorp Global's information assets from threats, whether internal, external,
                deliberate, or accidental.
                
                2. INFORMATION SECURITY PRINCIPLES
                - Confidentiality: Information is accessible only to authorized individuals
                - Integrity: Information is accurate and complete
                - Availability: Information is accessible when needed by authorized users
                
                3. ACCESS CONTROL
                - User authentication through multi-factor authentication (MFA)
                - Role-based access control (RBAC)
                - Principle of least privilege
                - Regular access reviews
                
                4. NETWORK SECURITY
                - Firewall protection on all network boundaries
                - Intrusion detection and prevention systems
                - Secure Wi-Fi with WPA3 encryption
                - Network segmentation for sensitive systems
                
                5. ENDPOINT SECURITY
                - Mandatory antivirus and anti-malware software
                - Regular security patches and updates
                - Full disk encryption on all devices
                - Mobile device management (MDM) for company devices
                
                6. PASSWORD REQUIREMENTS
                - Minimum 12 characters
                - Combination of uppercase, lowercase, numbers, and symbols
                - Password expiration every 90 days
                - No password reuse for last 10 passwords
                
                7. INCIDENT RESPONSE
                Security incidents must be reported immediately to the Security Operations Center (SOC).
                Incident response procedures include:
                - Detection and analysis
                - Containment
                - Eradication
                - Recovery
                - Post-incident review
                
                8. SECURITY AWARENESS TRAINING
                All employees must complete security awareness training annually, covering:
                - Phishing and social engineering
                - Safe browsing practices
                - Data handling procedures
                - Incident reporting
                
                9. THIRD-PARTY SECURITY
                Vendors and partners must demonstrate compliance with TechCorp's security requirements
                through security assessments and contractual obligations.
                """,
                "category": "Security",
                "organization": "TechCorp Global",
                "effective_date": "2023-06-15",
                "version": "3.0",
                "tags": ["security", "iso27001", "access control", "cyber security"]
            },
            {
                "title": "Anti-Money Laundering Policy - FinanceSecure Inc",
                "content": """
                ANTI-MONEY LAUNDERING POLICY
                
                Policy ID: POL-FS-001
                Version: 4.2
                Effective Date: January 1, 2024
                Organization: FinanceSecure Inc
                
                1. INTRODUCTION
                This policy establishes FinanceSecure Inc's commitment to preventing money laundering
                and terrorist financing in accordance with applicable laws and regulations.
                
                2. REGULATORY FRAMEWORK
                This policy ensures compliance with:
                - Bank Secrecy Act (BSA)
                - USA PATRIOT Act
                - Financial Crimes Enforcement Network (FinCEN) regulations
                - International AML standards
                
                3. CUSTOMER DUE DILIGENCE (CDD)
                All customers must undergo appropriate due diligence before onboarding:
                - Identity verification
                - Business purpose assessment
                - Source of funds evaluation
                - Beneficial ownership identification
                
                4. ENHANCED DUE DILIGENCE (EDD)
                High-risk customers require enhanced scrutiny:
                - Politically Exposed Persons (PEPs)
                - Customers from high-risk jurisdictions
                - Cash-intensive businesses
                - Customers with complex ownership structures
                
                5. TRANSACTION MONITORING
                Automated systems monitor transactions for suspicious patterns:
                - Large cash transactions
                - Structuring (smurfing)
                - Unusual transaction patterns
                - Transactions with high-risk jurisdictions
                
                6. SUSPICIOUS ACTIVITY REPORTING (SAR)
                Suspicious activities must be reported to:
                - Internal AML Compliance Officer (within 24 hours)
                - FinCEN (within 30 days of detection)
                
                7. RECORD KEEPING
                Records must be maintained for:
                - Customer identification: Minimum 5 years after account closure
                - Transaction records: Minimum 5 years
                - SAR documentation: Minimum 5 years
                
                8. TRAINING
                Annual AML training is mandatory for all employees, with specialized training for:
                - Front-line staff
                - Compliance officers
                - Senior management
                
                9. INDEPENDENT TESTING
                An independent audit of the AML program will be conducted annually by internal audit
                or external auditors.
                """,
                "category": "Financial Compliance",
                "organization": "FinanceSecure Inc",
                "effective_date": "2024-01-01",
                "version": "4.2",
                "tags": ["aml", "compliance", "financial crime", "regulatory"]
            },
            {
                "title": "Patient Data Privacy Policy - HealthData Systems",
                "content": """
                PATIENT DATA PRIVACY POLICY
                
                Policy ID: POL-HD-001
                Version: 3.1
                Effective Date: February 1, 2024
                Organization: HealthData Systems
                
                1. PURPOSE
                To protect the privacy and confidentiality of patient health information in compliance
                with HIPAA, GDPR, and other applicable regulations.
                
                2. SCOPE
                This policy applies to all Protected Health Information (PHI) in any form (electronic,
                paper, oral) and all employees, contractors, and business associates.
                
                3. MINIMUM NECESSARY STANDARD
                Access to PHI should be limited to the minimum necessary to accomplish the intended purpose.
                
                4. PATIENT RIGHTS
                Patients have the right to:
                - Access their medical records
                - Request amendments to their records
                - Receive an accounting of disclosures
                - Request restrictions on uses and disclosures
                - Request confidential communications
                - Receive notice of privacy practices
                
                5. PERMITTED USES AND DISCLOSURES
                PHI may be used/disclosed without authorization for:
                - Treatment
                - Payment
                - Healthcare operations
                - Required by law
                - Public health activities
                
                6. AUTHORIZATION REQUIREMENTS
                Written patient authorization is required for:
                - Marketing purposes
                - Sale of PHI
                - Psychotherapy notes (with exceptions)
                - Other non-routine disclosures
                
                7. SECURITY SAFEGUARDS
                Electronic PHI (ePHI) must be protected through:
                - Access controls and user authentication
                - Encryption of data at rest and in transit
                - Audit logging and monitoring
                - Secure data backup and disaster recovery
                
                8. BREACH NOTIFICATION
                In the event of a breach affecting 500 or more individuals:
                - Notify affected individuals without unreasonable delay
                - Notify HHS Secretary
                - Notify prominent media outlets (if breach affects >500 in a jurisdiction)
                
                9. BUSINESS ASSOCIATE AGREEMENTS
                All vendors with PHI access must sign Business Associate Agreements (BAA) ensuring
                compliance with HIPAA requirements.
                
                10. TRAINING AND AWARENESS
                All workforce members must complete HIPAA privacy training upon hire and annually
                thereafter.
                """,
                "category": "Healthcare Privacy",
                "organization": "HealthData Systems",
                "effective_date": "2024-02-01",
                "version": "3.1",
                "tags": ["hipaa", "healthcare", "privacy", "phi", "patient data"]
            }
        ]
        
        for doc in policy_documents:
            kb.add_policy_document(
                title=doc["title"],
                content=doc["content"],
                category=doc["category"],
                organization=doc["organization"],
                effective_date=doc["effective_date"],
                version=doc["version"],
                tags=doc["tags"]
            )
            print(f"  ✓ Added policy: {doc['title']}")
        
        # 2. Add Regulations
        print("\n⚖️ Adding Regulatory Documents...")
        
        regulations = [
            {
                "regulation_id": "REG-GDPR",
                "title": "General Data Protection Regulation (GDPR) - Overview",
                "summary": """
                The GDPR is a comprehensive data protection law that came into effect on May 25, 2018.
                
                KEY PRINCIPLES:
                1. Lawfulness, fairness, and transparency
                2. Purpose limitation
                3. Data minimization
                4. Accuracy
                5. Storage limitation
                6. Integrity and confidentiality
                7. Accountability
                
                DATA SUBJECT RIGHTS:
                - Right to access
                - Right to rectification
                - Right to erasure
                - Right to restrict processing
                - Right to data portability
                - Right to object
                - Rights related to automated decision-making
                
                REQUIREMENTS FOR ORGANIZATIONS:
                - Legal basis for processing
                - Data Protection Impact Assessments (DPIA)
                - Data Protection Officer (DPO) for certain organizations
                - Breach notification within 72 hours
                - Privacy by design and by default
                - Records of processing activities
                
                PENALTIES:
                - Tier 1: Up to €10 million or 2% of global annual turnover
                - Tier 2: Up to €20 million or 4% of global annual turnover
                
                GEOGRAPHICAL SCOPE:
                Applies to organizations processing data of EU/EEA residents, regardless of org location.
                """,
                "jurisdiction": "European Union",
                "requirements": [
                    "Data Protection Officer appointment (for certain entities)",
                    "Privacy Impact Assessments for high-risk processing",
                    "Breach notification within 72 hours",
                    "Consent management mechanisms",
                    "Data portability capabilities",
                    "Right to erasure implementation"
                ]
            },
            {
                "regulation_id": "REG-HIPAA",
                "title": "Health Insurance Portability and Accountability Act (HIPAA) - Overview",
                "summary": """
                HIPAA establishes national standards for protecting health information.
                
                KEY RULES:
                
                1. PRIVACY RULE:
                - Protects Protected Health Information (PHI)
                - Establishes permitted uses and disclosures
                - Grants patient rights
                
                2. SECURITY RULE:
                - Protects electronic PHI (ePHI)
                - Requires administrative, physical, and technical safeguards
                
                3. BREACH NOTIFICATION RULE:
                - Requires notification of breaches affecting PHI
                - Timelines: Without unreasonable delay, max 60 days
                
                COVERED ENTITIES:
                - Healthcare providers
                - Health plans
                - Healthcare clearinghouses
                
                BUSINESS ASSOCIATES:
                - Vendors with PHI access
                - Must sign Business Associate Agreements (BAA)
                
                SECURITY SAFEGUARDS:
                Administrative:
                - Risk analysis and management
                - Workforce security
                - Information access management
                
                Physical:
                - Facility access controls
                - Workstation security
                - Device and media controls
                
                Technical:
                - Access control
                - Audit controls
                - Integrity controls
                - Transmission security
                
                PENALTIES:
                - Tier 1: $100-$50,000 per violation (unknowing)
                - Tier 2: $1,000-$50,000 per violation (reasonable cause)
                - Tier 3: $10,000-$50,000 per violation (willful neglect, corrected)
                - Tier 4: $50,000+ per violation (willful neglect, not corrected)
                Annual maximum: $1.5 million per violation type
                """,
                "jurisdiction": "United States",
                "requirements": [
                    "Privacy and security policies",
                    "Risk assessments",
                    "Business Associate Agreements",
                    "Breach notification procedures",
                    "Access controls and audit logging",
                    "Workforce training"
                ]
            }
        ]
        
        for reg in regulations:
            kb.add_regulation(
                regulation_id=reg["regulation_id"],
                title=reg["title"],
                summary=reg["summary"],
                jurisdiction=reg["jurisdiction"],
                requirements=reg["requirements"]
            )
            print(f"  ✓ Added regulation: {reg['title']}")
        
        # 3. Add Guidelines
        print("\n📖 Adding Compliance Guidelines...")
        
        guidelines = [
            {
                "title": "Data Privacy Best Practices",
                "content": """
                BEST PRACTICES FOR DATA PRIVACY COMPLIANCE
                
                1. DATA INVENTORY AND MAPPING
                   - Conduct comprehensive data inventory
                   - Map data flows across systems
                   - Identify data categories and sensitivity levels
                   - Document data processing activities
                
                2. PRIVACY BY DESIGN
                   - Integrate privacy into system design
                   - Implement default privacy settings
                   - Minimize data collection
                   - Use pseudonymization and anonymization
                
                3. CONSENT MANAGEMENT
                   - Obtain clear, affirmative consent
                   - Provide granular consent options
                   - Enable easy consent withdrawal
                   - Maintain consent records
                
                4. DATA SUBJECT REQUEST HANDLING
                   - Establish clear DSR procedures
                   - Respond within regulatory timeframes
                   - Verify requester identity
                   - Document all requests and responses
                
                5. VENDOR MANAGEMENT
                   - Conduct vendor security assessments
                   - Include data protection clauses in contracts
                   - Monitor vendor compliance regularly
                   - Maintain vendor inventory
                
                6. TRAINING AND AWARENESS
                   - Provide regular privacy training
                   - Create role-specific training modules
                   - Test understanding through assessments
                   - Update training for regulatory changes
                
                7. INCIDENT RESPONSE
                   - Develop breach response plan
                   - Define incident severity levels
                   - Establish notification procedures
                   - Conduct regular tabletop exercises
                
                8. PRIVACY METRICS
                   - Track consent rates
                   - Monitor DSR response times
                   - Measure training completion
                   - Report privacy incidents
                """,
                "category": "Data Privacy",
                "applicable_regulations": ["GDPR", "CCPA"]
            },
            {
                "title": "Policy Conflict Resolution Framework",
                "content": """
                FRAMEWORK FOR RESOLVING POLICY CONFLICTS
                
                1. CONFLICT IDENTIFICATION
                   - Regular policy audits
                   - Automated conflict detection
                   - Stakeholder feedback
                   - Incident-driven discovery
                
                2. CONFLICT CLASSIFICATION
                   DIRECT CONFLICTS:
                   - Explicitly contradictory requirements
                   - Priority: Critical
                   
                   PARTIAL CONFLICTS:
                   - Overlapping but inconsistent provisions
                   - Priority: High
                   
                   IMPLICIT CONFLICTS:
                   - Different underlying assumptions
                   - Priority: Medium
                   
                   TEMPORAL CONFLICTS:
                   - Version control issues
                   - Priority: Low to Medium
                
                3. RESOLUTION HIERARCHY
                   Level 1: Regulatory requirements (highest)
                   Level 2: Legal obligations
                   Level 3: Industry standards
                   Level 4: Corporate policies
                   Level 5: Departmental procedures
                
                4. RESOLUTION PROCESS
                   Step 1: Document the conflict
                   Step 2: Analyze impact and scope
                   Step 3: Consult stakeholders
                   Step 4: Determine appropriate resolution
                   Step 5: Update policies
                   Step 6: Communicate changes
                   Step 7: Monitor implementation
                
                5. PREVENTIVE MEASURES
                   - Centralized policy repository
                   - Version control and change management
                   - Regular policy reviews
                   - Cross-functional policy approval
                   - Conflict detection automation
                
                6. DOCUMENTATION
                   - Maintain conflict log
                   - Record resolution decisions
                   - Track implementation status
                   - Audit resolution effectiveness
                """,
                "category": "Policy Management",
                "applicable_regulations": ["GDPR", "SOX", "HIPAA"]
            }
        ]
        
        for guide in guidelines:
            kb.add_guideline(
                title=guide["title"],
                content=guide["content"],
                category=guide["category"],
                applicable_regulations=guide["applicable_regulations"]
            )
            print(f"  ✓ Added guideline: {guide['title']}")
        
        print("\n✅ Knowledge Base Population Complete!")
        print(f"\nTotal documents added:")
        print(f"  Policies: {len(policy_documents)}")
        print(f"  Regulations: {len(regulations)}")
        print(f"  Guidelines: {len(guidelines)}")
        
    except Exception as e:
        print(f"\n❌ Error during population: {e}")
        raise
    finally:
        kb.close()


if __name__ == "__main__":
    populate_knowledge_base()
