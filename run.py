from app import create_app

# Construction du point d'entrée de l'application Flask
app = create_app()

if __name__ == "__main__":
    #app run -> demarre un serveur local sur http://127.0.0.1:5000/
    app.run(debug=True)