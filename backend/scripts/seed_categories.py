"""
Seed script to populate default categories in the database.
Run with: python -m scripts.seed_categories
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.category import Category

# Default categories for expense tracking
DEFAULT_CATEGORIES = [
    {
        "name": "Food & Dining",
        "description": "Restaurants, groceries, food delivery",
        "color": "#FF6B6B",
        "icon": "utensils"
    },
    {
        "name": "Transportation",
        "description": "Gas, public transport, ride-sharing, car maintenance",
        "color": "#4ECDC4",
        "icon": "car"
    },
    {
        "name": "Shopping",
        "description": "Clothing, electronics, general shopping",
        "color": "#95E1D3",
        "icon": "shopping-bag"
    },
    {
        "name": "Entertainment",
        "description": "Movies, concerts, games, hobbies",
        "color": "#F38181",
        "icon": "film"
    },
    {
        "name": "Bills & Utilities",
        "description": "Rent, electricity, water, internet, phone",
        "color": "#AA96DA",
        "icon": "file-text"
    },
    {
        "name": "Healthcare",
        "description": "Doctor visits, pharmacy, medical expenses",
        "color": "#FCBAD3",
        "icon": "heart"
    },
    {
        "name": "Travel",
        "description": "Flights, hotels, vacation expenses",
        "color": "#A8D8EA",
        "icon": "plane"
    },
    {
        "name": "Education",
        "description": "Courses, books, school supplies",
        "color": "#FFD93D",
        "icon": "book"
    },
    {
        "name": "Personal Care",
        "description": "Haircuts, gym, beauty products",
        "color": "#6BCB77",
        "icon": "user"
    },
    {
        "name": "Other",
        "description": "Miscellaneous expenses",
        "color": "#95A5A6",
        "icon": "more-horizontal"
    }
]


def seed_categories(db: Session):
    """Create default categories if they don't exist"""

    print("Checking for existing default categories...")

    # Check if default categories already exist
    existing = db.query(Category).filter(Category.is_default == True).count()

    if existing > 0:
        print(f"Found {existing} default categories. Skipping seed.")
        return

    print("Creating default categories...")

    for cat_data in DEFAULT_CATEGORIES:
        category = Category(
            name=cat_data["name"],
            description=cat_data["description"],
            color=cat_data["color"],
            icon=cat_data["icon"],
            user_id=None,  # Default categories have no user
            is_default=True
        )
        db.add(category)

    db.commit()
    print(f"✓ Created {len(DEFAULT_CATEGORIES)} default categories")


def main():
    """Main function to run the seed script"""
    print("=== Seeding Default Categories ===\n")

    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # Create session
    db = SessionLocal()

    try:
        seed_categories(db)
        print("\n✓ Seed completed successfully!")
    except Exception as e:
        print(f"\n✗ Error during seed: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
