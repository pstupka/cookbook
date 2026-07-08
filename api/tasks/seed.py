from init_admin import init_admin
from sqlalchemy import text

from app.db.schema import Base, SessionLocal, engine
from app.services.recipe_service import RecipeService

db = SessionLocal()

try:
    db.execute(text("DROP SCHEMA public CASCADE; CREATE SCHEMA public;"))
    db.commit()
    Base.metadata.create_all(engine)

    user = init_admin()

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

    recipe_service.create_recipe(
        name="Secret Chili Oil Noodles",
        description="Spicy pantry noodles for a quick late-night meal",
        ingredients=[
            {"name": "Noodles", "quantity": "200", "unit": "g"},
            {"name": "Chili Oil", "quantity": "2", "unit": "tbsp"},
            {"name": "Soy Sauce", "quantity": "1", "unit": "tbsp"},
            {"name": "Garlic", "quantity": "2", "unit": "cloves"},
        ],
        instructions=[
            {"order": 1, "text": "Cook noodles according to package instructions"},
            {"order": 2, "text": "Mix chili oil, soy sauce, and minced garlic"},
            {"order": 3, "text": "Toss hot noodles with the sauce and serve"},
        ],
        tags=["quick", "spicy", "noodles"],
        prep_time=5,
        cook_time=10,
        meal_type="dinner",
        owner_id=user.id,
        visibility="private",
    )

    recipe_service.create_recipe(
        name="Members-Only Tiramisu Cups",
        description="No-bake espresso dessert for community members",
        ingredients=[
            {"name": "Ladyfingers", "quantity": "12", "unit": "pieces"},
            {"name": "Mascarpone", "quantity": "250", "unit": "g"},
            {"name": "Espresso", "quantity": "120", "unit": "ml"},
            {"name": "Cocoa Powder", "quantity": "1", "unit": "tbsp"},
        ],
        instructions=[
            {"order": 1, "text": "Whisk mascarpone until smooth"},
            {"order": 2, "text": "Dip ladyfingers briefly in espresso"},
            {"order": 3, "text": "Layer ladyfingers and mascarpone in cups"},
            {"order": 4, "text": "Dust with cocoa powder and chill before serving"},
        ],
        tags=["dessert", "coffee", "no-bake"],
        prep_time=15,
        cook_time=0,
        meal_type="dessert",
        owner_id=user.id,
        visibility="members",
    )

    print("Seed complete.")
finally:
    db.close()
