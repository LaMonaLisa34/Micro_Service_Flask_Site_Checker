from app import create_app

# Construction du point d'entrée de l'application Flask
app = create_app()

if __name__ == "__main__":
    #app run -> demarre un serveur 
    app.run(host="0.0.0.0", port=5000, debug=True)