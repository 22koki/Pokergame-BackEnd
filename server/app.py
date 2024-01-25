# app.py

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User, GameRecord
from game_logic import PokerGame

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///poker_records.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)
db.init_app(app)

# Create tables based on the defined models
with app.app_context():
    db.create_all()

poker_game = PokerGame()

# Index Route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Poker API!"})

# Route to return the deck of cards
@app.route("/deck", methods=["GET"])
def get_deck():
    # Initialize the deck before the game starts
    poker_game.initialize_deck()
    return jsonify({"deck": poker_game.deck})

@app.route("/shuffle", methods=["POST"])
def shuffle_deck():
    poker_game.deck = poker_game.get_shuffled_deck()
    return jsonify({"message": "Deck shuffled successfully", "shuffled_deck": poker_game.deck})

# Route to draw one card from the deck
@app.route("/draw", methods=["POST"])
def draw_card():
    if not poker_game.deck:
        return jsonify({"message": "No cards left in the deck"})

    card = poker_game.deck.pop(0)
    return jsonify({"card": card})

# Endpoint for User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    hashed_password = generate_password_hash(password, method='sha256')

    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# Endpoint for User Authentication
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Endpoint to record Game Results, associating it with the user who played the game
@app.route('/record_game', methods=['POST'])
def record_game():
    data = request.get_json()
    user_id = data.get('user_id')  # Assuming you have a way to get the user ID
    result = data.get('result')

    new_game_record = GameRecord(user_id=user_id, result=result)
    db.session.add(new_game_record)
    db.session.commit()

    return jsonify({"message": "Game result recorded successfully"}), 201

# Endpoint to Retrieve Scores
@app.route('/scores', methods=['GET'])
def get_scores():
    scores = GameRecord.query.all()
    serialized_scores = [score.to_dict() for score in scores]

    return jsonify({"scores": serialized_scores})
    
# Route to start the game
@app.route('/start_game', methods=['GET'])
def start_game():
    displayed_card = poker_game.start_game()
    return jsonify({"message": "Game started successfully", "displayed_card": displayed_card})

# Route to play a card
@app.route('/play_card', methods=['POST'])
def play_card():
    data = request.get_json()
    player_name = data.get('player_name')
    card_choice = data.get('card_choice')

    poker_game.play_card(player_name, card_choice)

    return jsonify({"message": "Card played successfully"})

if __name__ == "__main__":
    app.run(debug=True, port=5555)
