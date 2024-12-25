from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Pour permettre les requêtes cross-origin

# Configuration de la base de données
db_config = {
    'host': 'dpg-ctm5t2a3esus739ncb1g-a',
    'user': 'solidarite_user',
    'password': 'i8fkp1uF6C8XUbnWLDcoVT637n1wS5kn',  # Remplacez par votre mot de passe MySQL
    'database': 'solidarite'
}

# Connexion à la base de données
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Route pour récupérer toutes les entités de solidarité
@app.route('/entites', methods=['GET'])
def get_entites():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM entites_solidarite")
    entites = cursor.fetchall()
    conn.close()
    return jsonify(entites)

# Route pour ajouter une nouvelle entité
@app.route('/entites', methods=['POST'])
def add_entite():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO entites_solidarite (nom, solidarite_id) VALUES (%s, %s)",
                   (data['nom'], data['solidarite_id']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Entité ajoutée avec succès!"}), 201

# Route pour récupérer tous les membres
@app.route('/membres', methods=['GET'])
def get_membres():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM membres_entites")
    membres = cursor.fetchall()
    conn.close()
    return jsonify(membres)


from flask import jsonify, request
import mysql.connector

# Route pour ajouter un membre
@app.route('/membres', methods=['POST'])
def add_membre():
    try:
        data = request.json

        # Valider les données d'entrée
        required_fields = ['nom', 'profession', 'age', 'genre', 'telephone', 'lieu_travail', 
                           'niveau_academique', 'carte_adhesion', 'entite_id', 'role_id']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Le champ '{field}' est requis."}), 400

        # Connexion à la base de données
        conn = get_db_connection()
        cursor = conn.cursor()

        # Ajouter le nouveau membre
        cursor.execute("""
            INSERT INTO membres_entites 
            (nom, profession, age, genre, telephone, lieu_travail, niveau_academique, carte_adhesion, entite_id, role_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (data['nom'], data['profession'], data['age'], data['genre'], data['telephone'], 
              data['lieu_travail'], data['niveau_academique'], data['carte_adhesion'], data['entite_id'], data['role_id']))
        
        conn.commit()

        # Récupérer l'ID du membre ajouté
        membre_id = cursor.lastrowid

        # Créer automatiquement une carte d'adhésion pour ce membre
        cursor.execute("""
            INSERT INTO cartes_adhesion (membre_id, date_delivrance, statut, montant, date_statut) 
            VALUES (%s, CURDATE(), 'Délivrée', 100.00, CURDATE())
        """, (membre_id,))
        
        conn.commit()

        # Fermer la connexion
        cursor.close()
        conn.close()

        return jsonify({"message": "Membre et carte ajoutés avec succès!"}), 201

    except mysql.connector.Error as err:
        # Gestion des erreurs SQL
        if conn:
            conn.rollback()
        return jsonify({"error": f"Erreur de base de données: {str(err)}"}), 500

    except Exception as e:
        # Gestion des erreurs générales
        return jsonify({"error": f"Erreur serveur: {str(e)}"}), 500



# Route pour récupérer un membre par ID
@app.route('/membres/<int:id>', methods=['GET'])
def get_membre_by_id(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM membres_entites WHERE id = %s", (id,))
    membre = cursor.fetchone()
    conn.close()
    if membre:
        return jsonify(membre)
    else:
        return jsonify({"error": "Membre non trouvé"}), 404

# Route pour mettre à jour un membre
@app.route('/membres/<int:id>', methods=['PUT'])
def update_membre(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""UPDATE membres_entites 
                      SET nom=%s, profession=%s, age=%s, genre=%s, telephone=%s, lieu_travail=%s, niveau_academique=%s, carte_adhesion=%s, entite_id=%s, role_id=%s 
                      WHERE id=%s""",
                   (data['nom'], data['profession'], data['age'], data['genre'], data['telephone'],
                    data['lieu_travail'], data['niveau_academique'], data['carte_adhesion'], data['entite_id'], data['role_id'], id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Membre mis à jour avec succès!"})

# Route pour supprimer un membre
@app.route('/membres/<int:id>', methods=['DELETE'])
def delete_membre(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM membres_entites WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Membre supprimé avec succès!"})

# Route pour récupérer toutes les cartes d'adhésion
@app.route('/cartes', methods=['GET'])
def get_cartes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cartes_adhesion")
    cartes = cursor.fetchall()
    conn.close()
    return jsonify(cartes)

# Lancer le serveur Flask
if __name__ == '__main__':
    app.run(debug=True)
