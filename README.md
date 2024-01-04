#Installation#
1. **Clone the repository**


   git clone https://github.com/sanjana0503/Django_Sneakers_Website.git

3. **Set up Virtual Environment**


   python -m venv env


   source env/bin/activate

3.**change directory to ec**

    cd ec


4. **Install Dependencies**

   
     ```pip install -r requirements.txt```




*Before migrations , If you are using sql check database settings add your db name , username, password, host, port etc*



6. **Run Migrations**




   ```python manage.py makemigrations```




    ```python manage.py migrate```

8. **Create Superuser**





 	```python manage.py createsuperuser```


 
10. **Start the Server**   



	``` python manage.py runserver```









   
 
