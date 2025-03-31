from app import create_app
import initial_data

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)