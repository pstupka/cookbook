from app.db.schema import SessionLocal
from app.services.recipe_service import RecipeService
from app.services.user_service import UserService

db = SessionLocal()

try:
    user = UserService(db).create_user(
        username="admin",
        password="secret",
        email="admin@example.com",
        full_name="Admin User",
    )

    recipe_service = RecipeService(db)

    recipe_service.create_recipe(
        name="Pasta Carbonara",
        description="Classic Roman pasta with eggs and guanciale",
        ingredients=[
            {"name": "Spaghetti", "quantity": "200", "unit": "g"},
            {"name": "Guanciale", "quantity": "100", "unit": "g"},
            {"name": "Eggs", "quantity": "2"},
            {"name": "Pecorino Romano", "quantity": "50", "unit": "g"},
        ],
        instructions=[
            {"order": 1, "text": "Cook spaghetti in salted boiling water until al dente"},
            {"order": 2, "text": "Fry guanciale until crispy"},
            {"order": 3, "text": "Whisk eggs with grated pecorino"},
            {"order": 4, "text": "Combine pasta with guanciale off heat, add egg mixture and toss"},
        ],
        tags=["italian", "pasta"],
        prep_time=10,
        cook_time=20,
        meal_type="dinner",
        owner_id=user.id,
        visibility="public",
    )

    recipe_service.create_recipe(
        name="Avocado Toast",
        description="Simple and healthy breakfast",
        ingredients=[
            {"name": "Sourdough Bread", "quantity": "2", "unit": "slices"},
            {"name": "Avocado", "quantity": "1"},
            {"name": "Lemon Juice", "quantity": "1", "unit": "tsp"},
            {"name": "Salt", "quantity": "1", "unit": "pinch"},
        ],
        instructions=[
            {"order": 1, "text": "Toast the bread"},
            {"order": 2, "text": "Mash avocado with lemon juice and salt"},
            {"order": 3, "text": "Spread on toast"},
        ],
        tags=["breakfast", "healthy"],
        prep_time=5,
        cook_time=5,
        meal_type="breakfast",
        diet_type="vegan",
        owner_id=user.id,
        visibility="public",
    )

    print("Seed complete.")
finally:
    db.close()
