"""
AI services for case management (mock implementations).

This module provides mock AI functionality including:
- Case triage with keyword detection
- Case summary generation
- Precedent search with text matching

Validates: Requirements FR3.1-FR3.5
"""

from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from models.case import Case


# Mock precedent data
MOCK_PRECEDENTS = [
    {
        "id": "prec-001",
        "title": "Property Boundary Dispute Resolution",
        "summary": "Established legal precedent for resolving property boundary disputes between adjacent landowners",
        "keywords": ["property", "boundary", "dispute", "land", "ownership"]
    },
    {
        "id": "prec-002",
        "title": "Assault and Battery Case Law",
        "summary": "Comprehensive ruling on assault and battery charges with sentencing guidelines",
        "keywords": ["assault", "battery", "violence", "injury", "criminal"]
    },
    {
        "id": "prec-003",
        "title": "Contract Breach Remedies",
        "summary": "Legal framework for determining damages in contract breach cases",
        "keywords": ["contract", "breach", "damages", "agreement", "liability"]
    },
    {
        "id": "prec-004",
        "title": "Emergency Injunction Standards",
        "summary": "Standards for granting emergency injunctions in urgent legal matters",
        "keywords": ["emergency", "injunction", "urgent", "immediate", "relief"]
    },
    {
        "id": "prec-005",
        "title": "Inheritance and Estate Disputes",
        "summary": "Precedent for resolving disputes over wills and estate distribution",
        "keywords": ["inheritance", "estate", "will", "distribution", "family"]
    },
    {
        "id": "prec-006",
        "title": "Employment Discrimination Law",
        "summary": "Legal standards for employment discrimination cases",
        "keywords": ["employment", "discrimination", "workplace", "rights", "harassment"]
    },
    {
        "id": "prec-007",
        "title": "Medical Malpractice Standards",
        "summary": "Standards for proving medical malpractice and determining damages",
        "keywords": ["medical", "malpractice", "doctor", "negligence", "injury"]
    },
    {
        "id": "prec-008",
        "title": "Tenant Rights and Eviction",
        "summary": "Legal framework for tenant rights and eviction procedures",
        "keywords": ["tenant", "eviction", "landlord", "rent", "housing"]
    },
    {
        "id": "prec-009",
        "title": "Intellectual Property Infringement",
        "summary": "Standards for proving intellectual property infringement and damages",
        "keywords": ["intellectual", "property", "patent", "copyright", "infringement"]
    },
    {
        "id": "prec-010",
        "title": "Traffic Accident Liability",
        "summary": "Legal standards for determining liability in traffic accidents",
        "keywords": ["traffic", "accident", "vehicle", "liability", "insurance"]
    },
]

# Urgent keywords for triage
URGENT_KEYWORDS = ["urgent", "assault", "emergency", "immediate", "critical", "violence", "injury"]


class AIService:
    """
    AI service providing mock implementations of AI functionality.
    """
    
    @staticmethod
    def triage_case(case_id: UUID, description: str, db: Session) -> Case:
        """
        Triage a case by detecting urgent keywords.
        
        Implements:
        - FR3.1: Triage cases based on keywords
        - FR3.2: Set priority to HIGH for urgent cases
        - FR3.3: Set priority to REGULAR for non-urgent cases
        
        Args:
            case_id: UUID of the case to triage
            description: Case description to analyze
            db: Database session
            
        Returns:
            Updated Case object with priority set
            
        Example:
            >>> case = AIService.triage_case(case_id, description, db)
            >>> print(case.priority)
            HIGH
        """
        # Query case
        case = db.query(Case).filter(Case.id == case_id).first()
        if not case:
            return None
        
        # Convert description to lowercase for case-insensitive matching
        description_lower = description.lower()
        
        # Check for urgent keywords
        is_urgent = any(keyword in description_lower for keyword in URGENT_KEYWORDS)
        
        # Set priority based on urgency
        case.priority = "HIGH" if is_urgent else "REGULAR"
        
        db.commit()
        db.refresh(case)
        
        return case
    
    @staticmethod
    def generate_summary(case_id: UUID, description: str, db: Session) -> Case:
        """
        Generate a mock AI summary of a case.
        
        Implements:
        - FR3.4: Generate case summaries
        - FR3.5: Append "[AI Generated Summary]" suffix
        
        Creates a summary by truncating the description to 200 characters
        and appending the AI marker.
        
        Args:
            case_id: UUID of the case to summarize
            description: Case description to summarize
            db: Database session
            
        Returns:
            Updated Case object with ai_summary set
            
        Example:
            >>> case = AIService.generate_summary(case_id, description, db)
            >>> print(case.ai_summary)
            "This is a case about property dispute between two neighbors..."
        """
        # Query case
        case = db.query(Case).filter(Case.id == case_id).first()
        if not case:
            return None
        
        # Create summary by truncating to 200 characters
        summary = description[:200]
        if len(description) > 200:
            summary += "..."
        
        # Append AI marker
        summary += " [AI Generated Summary]"
        
        # Store summary
        case.ai_summary = summary
        
        db.commit()
        db.refresh(case)
        
        return case
    
    @staticmethod
    def search_precedents(query: str) -> List[dict]:
        """
        Search for relevant precedents using text matching.
        
        Implements:
        - FR3.6: Search precedents by keywords
        - FR3.7: Return results ranked by relevance
        
        Performs keyword-based relevance scoring:
        - Each keyword match in title: +3 points
        - Each keyword match in summary: +1 point
        - Each keyword match in keywords list: +2 points
        
        Args:
            query: Search query string
            
        Returns:
            List of precedents ranked by relevance score (highest first)
            
        Example:
            >>> results = AIService.search_precedents("property dispute")
            >>> print(len(results))
            3
            >>> print(results[0]["title"])
            "Property Boundary Dispute Resolution"
        """
        # Convert query to lowercase and split into keywords
        query_lower = query.lower()
        query_keywords = query_lower.split()
        
        # Score each precedent
        scored_precedents = []
        
        for precedent in MOCK_PRECEDENTS:
            score = 0
            
            # Score title matches (highest weight)
            title_lower = precedent["title"].lower()
            for keyword in query_keywords:
                if keyword in title_lower:
                    score += 3
            
            # Score summary matches (medium weight)
            summary_lower = precedent["summary"].lower()
            for keyword in query_keywords:
                if keyword in summary_lower:
                    score += 1
            
            # Score keyword list matches (medium weight)
            for keyword in query_keywords:
                if keyword in precedent["keywords"]:
                    score += 2
            
            # Only include precedents with at least one match
            if score > 0:
                scored_precedents.append({
                    **precedent,
                    "relevance_score": score
                })
        
        # Sort by relevance score (descending)
        scored_precedents.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        return scored_precedents
