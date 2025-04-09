# If you have a fresh project or have deleted your database, 
# you need to run the setup_db.py script to create the database and tables.

# this is a good approach for development when setting up a fresh database.
# but if you later add or modify columns, you’ll need to manually delete/recreate the database.
# However, for a production-ready approach, Flask-Migrate (flask db migrate) is preferred
# Flask-Migrate allows incremental updates without data loss.


from myapp import create_app, db

app = create_app()

with app.app_context():     
    db.create_all()
    print("Database schema successfully initialized.")
    

# After running setup_db.py once and creating the database and tables, you do not need to run it again 
# unless you delete the database or make changes to the database structure (e.g., adding new tables or adding custom validators).

# bash command run: python setup_db.py