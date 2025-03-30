from app import create_app
import os

# Asegúrate de que la carpeta instance exista
os.makedirs('instance', exist_ok=True)

# Configura la ruta de la base de datos
app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/development.db'

if __name__ == '__main__':
    app.run(debug=True)