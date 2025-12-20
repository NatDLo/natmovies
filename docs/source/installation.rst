Installation
============

To install NatMovies locally:

1. Clone the repository:
git clone https://github.com/NatDLo/natmovies.git

2. Create a virtual environment:
python -m venv venv
source venv/bin/activate # Linux/macOS
venv\Scripts\activate # Windows

3. Install dependencies:
pip install -r backend/requirements.txt

4. Set up the database and run migrations:
python manage.py migrate

5. Run the server:
python manage.py runserver