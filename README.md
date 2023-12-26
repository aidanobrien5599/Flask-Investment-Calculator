This is an investment calculator that outputs a detailed table and a graph for visualization.
In order to run the app, make sure that a virtual environment is created and that the dependencies are 
installed. Then follow the following steps.
1. Create Sqllite database: in the terminal, type the following lines:
  >>> from app import app, db
  >>> app.app_context().push()
  >>> db.create_all()
2. Now, in order to run the app:
  >> python3 app.py
