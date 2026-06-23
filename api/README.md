# Cookbook App API
Cookbook App API built with FastAPI and SQLAlchemy. This API allows users to create, read, update, and delete recipes.


### Installation for local development

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cookbook.git
   cd cookbook
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```bash
   pip install -e .
   ```

4. Set up the environment variables:
   ```bash
   cp .env.example .env
   # Edit .env file with your database credentials
   ```

5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```