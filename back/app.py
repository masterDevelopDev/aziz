from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Pour permettre les requêtes cross-origin

# Configuration de la base de données
db_config = {
    'host': 'dpg-ctm5t2a3esus739ncb1g-a.oregon-postgres.render.com',
    'database': 'solidarite',
    'user': 'solidarite_user',
    'password': 'i8fkp1uF6C8XUbnWLDcoVT637n1wS5kn',
    'port': 5432
}

# Connexion à la base de données
def get_db_connection():
    conn = psycopg2.connect(
        host=db_config['host'],
        database=db_config['database'],
        user=db_config['user'],
        password=db_config['password'],
        port=db_config['port'],
        cursor_factory=RealDictCursor
    )
    return conn

# Route pour récupérer toutes les entités de solidarité
@app.route('/entites', methods=['GET'])
def get_entites():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM entites_solidarite")
        entites = cursor.fetchall()
        conn.close()
        return jsonify(entites)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour ajouter une nouvelle entité
@app.route('/entites', methods=['POST'])
def add_entite():
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO entites_solidarite (nom, solidarite_id) VALUES (%s, %s)",
                       (data['nom'], data['solidarite_id']))
        conn.commit()
        conn.close()
        return jsonify({"message": "Entité ajoutée avec succès!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour récupérer tous les membres
@app.route('/membres', methods=['GET'])
def get_membres():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM membres_entites")
        membres = cursor.fetchall()
        conn.close()
        return jsonify(membres)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour ajouter un membre
@app.route('/membres', methods=['POST'])
def add_membre():
    try:
        data = request.json
        required_fields = ['nom', 'profession', 'age', 'genre', 'telephone', 
                           'lieu_travail', 'niveau_academique', 'carte_adhesion', 
                           'entite_id', 'role_id']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Le champ '{field}' est requis."}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Ajouter le membre
        cursor.execute("""
            INSERT INTO membres_entites 
            (nom, profession, age, genre, telephone, lieu_travail, 
            niveau_academique, carte_adhesion, entite_id, role_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        """, (data['nom'], data['profession'], data['age'], data['genre'], 
              data['telephone'], data['lieu_travail'], data['niveau_academique'], 
              data['carte_adhesion'], data['entite_id'], data['role_id']))
        
        membre_id = cursor.fetchone()['id']

        # Créer automatiquement une carte d'adhésion
        cursor.execute("""
            INSERT INTO cartes_adhesion (membre_id, date_delivrance, statut, montant, date_statut) 
            VALUES (%s, CURRENT_DATE, 'Délivrée', 100.00, CURRENT_DATE)
        """, (membre_id,))
        
        conn.commit()
        conn.close()
        return jsonify({"message": "Membre et carte ajoutés avec succès!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour récupérer un membre par ID
@app.route('/membres/<int:id>', methods=['GET'])
def get_membre_by_id(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM membres_entites WHERE id = %s", (id,))
        membre = cursor.fetchone()
        conn.close()
        if membre:
            return jsonify(membre)
        else:
            return jsonify({"error": "Membre non trouvé"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour mettre à jour un membre
@app.route('/membres/<int:id>', methods=['PUT'])
def update_membre(id):
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE membres_entites 
            SET nom=%s, profession=%s, age=%s, genre=%s, telephone=%s, 
                lieu_travail=%s, niveau_academique=%s, carte_adhesion=%s, 
                entite_id=%s, role_id=%s 
            WHERE id=%s
        """, (data['nom'], data['profession'], data['age'], data['genre'], 
              data['telephone'], data['lieu_travail'], data['niveau_academique'], 
              data['carte_adhesion'], data['entite_id'], data['role_id'], id))
        conn.commit()
        conn.close()
        return jsonify({"message": "Membre mis à jour avec succès!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour supprimer un membre
@app.route('/membres/<int:id>', methods=['DELETE'])
def delete_membre(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM membres_entites WHERE id = %s", (id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Membre supprimé avec succès!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour récupérer toutes les cartes d'adhésion
@app.route('/cartes', methods=['GET'])
def get_cartes():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cartes_adhesion")
        cartes = cursor.fetchall()
        conn.close()
        return jsonify(cartes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Lancer le serveur Flask
if __name__ == '__main__':
    app.run(debug=True)
