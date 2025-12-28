from openai import OpenAI
from uuid import UUID
from sqlalchemy.orm import Session
from decimal import Decimal
import json

from app.config import get_settings
from app.repositories.category_repository import CategoryRepository
from app.repositories.expense_repository import ExpenseRepository

settings = get_settings()


class AIService:
    def __init__(self):
        """Initialize OpenAI client"""
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not configured")
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def categorize_expense(
        self,
        db: Session,
        description: str,
        amount: Decimal,
        user_id: UUID
    ) -> tuple[UUID | None, float]:
        """
        Use GPT-4o-mini to suggest a category for an expense by learning from user's past expenses.

        Args:
            db: Database session
            description: Expense description
            amount: Expense amount
            user_id: User ID

        Returns:
            Tuple of (suggested_category_id, confidence_score)
        """
        # Get available categories
        categories = CategoryRepository.get_all(db, user_id=user_id, skip=0, limit=100)
        if not categories:
            return None, 0.0

        # Get user's recent expenses to learn from their patterns
        recent_expenses, _ = ExpenseRepository.get_all(db, user_id=user_id, skip=0, limit=50)

        # Build examples from user's past expenses
        examples = []
        for expense in recent_expenses:
            if expense.category:
                examples.append({
                    "description": expense.description,
                    "amount": float(expense.amount),
                    "category": expense.category.name
                })

        # Build category list
        category_names = [cat.name for cat in categories]
        category_details = {
            cat.name: cat.description or "No description"
            for cat in categories
        }

        # Create enriched prompt with learning examples
        examples_text = ""
        if examples:
            examples_text = "\n\nPast expenses from this user:\n" + "\n".join([
                f"- \"{ex['description']}\" (${ex['amount']:.2f}) → {ex['category']}"
                for ex in examples[:20]  # Limit to 20 most recent
            ])

        categories_text = "\n".join([
            f"- {name}: {category_details[name]}"
            for name in category_names
        ])

        prompt = f"""You are categorizing an expense for a user. Learn from their past categorization patterns.

Available categories:
{categories_text}
{examples_text}

New expense to categorize:
- Description: {description}
- Amount: ${float(amount):.2f}

Based on the user's past categorization patterns and the expense details, which category fits best?

Respond ONLY with a JSON object in this exact format:
{{"category": "exact category name", "confidence": 0.95}}

The category must be one from the available categories list. Confidence should be 0.0-1.0."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that categorizes expenses. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=150
            )

            response_text = response.choices[0].message.content.strip()

            # Extract JSON from response
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            result = json.loads(response_text)
            suggested_name = result.get("category", "").strip()
            confidence = float(result.get("confidence", 0.0))

            # Find matching category
            for category in categories:
                if category.name.lower() == suggested_name.lower():
                    return category.id, confidence

            return None, 0.0

        except Exception as e:
            print(f"AI categorization error: {e}")
            import traceback
            traceback.print_exc()
            return None, 0.0
