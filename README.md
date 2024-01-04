#Installation#
1. **Clone the repository**
   git clone https://github.com/yourusername/your-repo.git

2. **Set up Virtual Environment**
   python -m venv env
   source env/bin/activate

3.**change directory to ec**
  cd ec

4. **Install Dependencies**
  pip install -r requirements.txt


*Before migrations , If you are using sql check database settings add your db name , username, password, host, port etc*



6. **Run Migrations**
   python manage.py makemigrations
   python manage.py migrate

7. **Create Superuser**
    python manage.py createsuperuser

8. **Start the Server**   
    python manage.py runserver
 
