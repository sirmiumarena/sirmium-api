from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import a2s
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

SERVER_IP = os.getenv("SERVER_IP", "185.211.103.141")
SERVER_PORT = int(os.getenv("SERVER_PORT", "3076"))

SERVER_ADDRESS = (SERVER_IP, SERVER_PORT)


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "message": "Sirmium Arena API radi!"
    })


@app.route("/api/status")
def server_status():

    try:
        # Dohvata informacije o CS 1.6 serveru
        info = a2s.info(
            SERVER_ADDRESS,
            timeout=3.0
        )

        # Dohvata listu igrača
        try:
            players = a2s.players(
                SERVER_ADDRESS,
                timeout=3.0
            )
        except Exception:
            players = []

        player_list = []

        for player in players:
            player_list.append({
                "name": player.name,
                "score": player.score,
                "duration": round(player.duration)
            })

        return jsonify({
            "online": True,
            "ip": SERVER_IP,
            "port": SERVER_PORT,
            "hostname": info.server_name,
            "map": info.map_name,
            "players": info.player_count,
            "max_players": info.max_players,
            "ping": None,
            "player_list": player_list
        })

    except Exception as e:

        return jsonify({
            "online": False,
            "ip": SERVER_IP,
            "port": SERVER_PORT,
            "hostname": "Sirmium Arena",
            "map": "-",
            "players": 0,
            "max_players": 0,
            "ping": None,
            "player_list": [],
            "error": str(e)
        })


if __name__ == "__main__":

    print("---------------------------------------")
    print("        SIRMIUM ARENA API")
    print("---------------------------------------")
    print(f"CS 1.6 SERVER: {SERVER_IP}:{SERVER_PORT}")
    print("API PORT: 8080")
    print("---------------------------------------")

    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8080")),
        debug=False
    )
