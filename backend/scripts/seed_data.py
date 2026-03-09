"""
Seed Data Script for Nyaysetu Case Management System

This script populates the database with sample data for testing and development.
It creates:
- Sample users (citizens and judges)
- Sample cases with various statuses and priorities
- AI-generated summaries for some cases

Usage:
    python scripts/seed_data.py

Note: This will clear existing data. Use with caution!
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from models.user import User
from models.case import Case
from services.password import hash_password
import uuid


def clear_data(db: Session):
    """Clear all existing data from the database."""
    print("Clearing existing data...")
    db.query(Case).delete()
    db.query(User).delete()
    db.commit()
    print("✓ Data cleared")


def create_users(db: Session):
    """Create sample users (citizens and judges)."""
    print("\nCreating sample users...")
    
    users = []
    
    # Create citizens
    citizens = [
        {"email": "citizen1@example.com", "password": "password123", "role": "CITIZEN"},
        {"email": "citizen2@example.com", "password": "password123", "role": "CITIZEN"},
        {"email": "citizen3@example.com", "password": "password123", "role": "CITIZEN"},
        {"email": "john.doe@example.com", "password": "password123", "role": "CITIZEN"},
        {"email": "jane.smith@example.com", "password": "password123", "role": "CITIZEN"},
    ]
    
    # Create judges
    judges = [
        {"email": "judge1@example.com", "password": "password123", "role": "JUDGE"},
        {"email": "judge2@example.com", "password": "password123", "role": "JUDGE"},
        {"email": "justice.sharma@example.com", "password": "password123", "role": "JUDGE"},
    ]
    
    all_users = citizens + judges
    
    for user_data in all_users:
        user = User(
            id=uuid.uuid4(),
            email=user_data["email"],
            password_hash=hash_password(user_data["password"]),
            role=user_data["role"]
        )
        db.add(user)
        users.append(user)
        print(f"  ✓ Created {user_data['role'].lower()}: {user_data['email']}")
    
    db.commit()
    print(f"✓ Created {len(users)} users")
    return users


def create_cases(db: Session, users: list):
    """Create sample cases with various statuses and priorities."""
    print("\nCreating sample cases...")
    
    # Get citizens and judges
    citizens = [u for u in users if u.role == "CITIZEN"]
    judges = [u for u in users if u.role == "JUDGE"]
    
    # Sample case data
    case_templates = [
        {
            "title": "Property Boundary Dispute",
            "description": "Urgent matter regarding property boundary dispute with neighbor. The neighbor has encroached on my land by approximately 10 feet and refuses to acknowledge the survey results.",
            "priority": "HIGH"
        },
        {
            "title": "Contract Breach - Business Agreement",
            "description": "The defendant failed to deliver goods as per the signed contract dated January 15, 2024. Despite multiple reminders, no action has been taken.",
            "priority": "REGULAR"
        },
        {
            "title": "Assault Case - Immediate Action Required",
            "description": "Emergency situation involving physical assault. Medical reports and witness statements are available. Seeking immediate legal protection.",
            "priority": "HIGH"
        },
        {
            "title": "Tenant Eviction Notice",
            "description": "Tenant has not paid rent for the last 6 months despite multiple notices. Seeking legal eviction process.",
            "priority": "REGULAR"
        },
        {
            "title": "Consumer Rights Violation",
            "description": "Purchased a defective product and the company refuses to provide refund or replacement despite warranty coverage.",
            "priority": "REGULAR"
        },
        {
            "title": "Employment Termination Dispute",
            "description": "Wrongful termination from employment without proper notice or severance pay. Have documentation of employment contract.",
            "priority": "REGULAR"
        },
        {
            "title": "Critical Medical Negligence Case",
            "description": "Critical case of medical negligence resulting in serious health complications. Immediate legal intervention required.",
            "priority": "HIGH"
        },
        {
            "title": "Inheritance Dispute",
            "description": "Dispute over property inheritance among family members. Will document is being contested.",
            "priority": "REGULAR"
        },
        {
            "title": "Traffic Accident Compensation",
            "description": "Seeking compensation for injuries sustained in traffic accident. Police report and medical records available.",
            "priority": "REGULAR"
        },
        {
            "title": "Domestic Violence - Urgent Protection Needed",
            "description": "Urgent case requiring immediate protection order. Evidence of ongoing domestic violence with police complaints filed.",
            "priority": "HIGH"
        },
        {
            "title": "Intellectual Property Infringement",
            "description": "Copyright infringement of original creative work. Seeking legal action against the infringing party.",
            "priority": "REGULAR"
        },
        {
            "title": "Loan Recovery Case",
            "description": "Borrower has defaulted on loan repayment. Have signed loan agreement and payment records.",
            "priority": "REGULAR"
        },
    ]
    
    statuses = ["FILED", "IN_REVIEW", "HEARING_SCHEDULED"]
    cases = []
    
    for i, template in enumerate(case_templates):
        # Assign to random citizen
        citizen = random.choice(citizens)
        
        # Determine status (more recent cases are more likely to be FILED)
        if i < 4:
            status = "FILED"
            judge_id = None
        elif i < 8:
            status = "IN_REVIEW"
            judge_id = random.choice(judges).id
        else:
            status = random.choice(statuses)
            judge_id = random.choice(judges).id if status != "FILED" else None
        
        # Create case with backdated created_at
        days_ago = len(case_templates) - i
        created_at = datetime.utcnow() - timedelta(days=days_ago)
        
        # Generate AI summary for some cases
        ai_summary = None
        if status in ["IN_REVIEW", "HEARING_SCHEDULED"] and random.random() > 0.3:
            ai_summary = template["description"][:200] + "... [AI Generated Summary]"
        
        case = Case(
            id=uuid.uuid4(),
            title=template["title"],
            description=template["description"],
            status=status,
            user_id=citizen.id,
            judge_id=judge_id,
            priority=template["priority"],
            ai_summary=ai_summary,
            created_at=created_at
        )
        
        db.add(case)
        cases.append(case)
        print(f"  ✓ Created case: {template['title'][:50]}... (Status: {status}, Priority: {template['priority']})")
    
    db.commit()
    print(f"✓ Created {len(cases)} cases")
    return cases


def print_summary(users: list, cases: list):
    """Print summary of seeded data."""
    print("\n" + "="*70)
    print("SEED DATA SUMMARY")
    print("="*70)
    
    citizens = [u for u in users if u.role == "CITIZEN"]
    judges = [u for u in users if u.role == "JUDGE"]
    
    print(f"\nUsers Created: {len(users)}")
    print(f"  - Citizens: {len(citizens)}")
    print(f"  - Judges: {len(judges)}")
    
    print(f"\nCases Created: {len(cases)}")
    filed = len([c for c in cases if c.status == "FILED"])
    in_review = len([c for c in cases if c.status == "IN_REVIEW"])
    hearing = len([c for c in cases if c.status == "HEARING_SCHEDULED"])
    print(f"  - Filed: {filed}")
    print(f"  - In Review: {in_review}")
    print(f"  - Hearing Scheduled: {hearing}")
    
    high_priority = len([c for c in cases if c.priority == "HIGH"])
    regular_priority = len([c for c in cases if c.priority == "REGULAR"])
    print(f"\nPriority Distribution:")
    print(f"  - High: {high_priority}")
    print(f"  - Regular: {regular_priority}")
    
    with_summary = len([c for c in cases if c.ai_summary])
    print(f"\nCases with AI Summary: {with_summary}")
    
    print("\n" + "="*70)
    print("LOGIN CREDENTIALS (All passwords: password123)")
    print("="*70)
    print("\nCitizens:")
    for citizen in citizens:
        print(f"  - {citizen.email}")
    print("\nJudges:")
    for judge in judges:
        print(f"  - {judge.email}")
    print("\n" + "="*70)


def main():
    """Main function to seed the database."""
    print("="*70)
    print("NYAYSETU CASE MANAGEMENT SYSTEM - SEED DATA SCRIPT")
    print("="*70)
    print("\nWARNING: This will clear all existing data!")
    
    response = input("\nDo you want to continue? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("Aborted.")
        return
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Clear existing data
        clear_data(db)
        
        # Create users
        users = create_users(db)
        
        # Create cases
        cases = create_cases(db, users)
        
        # Print summary
        print_summary(users, cases)
        
        print("\n✓ Database seeded successfully!")
        print("\nYou can now:")
        print("  1. Start the backend server: uvicorn app.main:app --reload")
        print("  2. Start the frontend: npm run dev")
        print("  3. Login with any of the credentials above")
        
    except Exception as e:
        print(f"\n✗ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
