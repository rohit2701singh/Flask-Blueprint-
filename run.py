from myapp import create_app  # import from __init__.py file

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
