from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from SilenceWriter import SilenceWriter
from RequestRepository import RequestRepository
from UserRepository import UserRepository
from logger import logger
from models import db

app = Flask(__name__)

CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    allow_headers=["Content-Type", "username"],
    methods=["GET", "POST"]
)


app.config["SQLALCHEMY_DATABASE_URI"] = Config.DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
with app.app_context():
    db.create_all()

logger.info("DB initialized")


@app.route("/silence", methods=["POST"])
def get_silence_data():
    username = request.headers.get("username", "NA")
    data = request.json
    logger.info(f"[payload] : {str(data)}", username)
    request_id = RequestRepository.create_request(
        timestamp=data["timestamp"],
        username=username,
        matchers=str(data["matchers"]),
        start=data["start"],
        end=data["end"],
        comment=data["comment"]
    )

    user = UserRepository.user_exists(username)

    if user is None:
        logger.error("[error]: Username doesn't exist", username)
        return jsonify({"Message": "User Doesn't exist"}), 400

    sil_response = SilenceWriter.create_silence(payload=data, user=username, folders=user)

    if sil_response["status_code"] == 202:
        logger.info(f"[silence created]: {sil_response['silenceID']}")
        RequestRepository.update_status(request_id=request_id, status="success", silenceID=sil_response["silenceID"])
    elif sil_response["status_code"] == 400:
        logger.info(f"[error]: {sil_response['failureMsg']}")
        RequestRepository.update_status(request_id=request_id, status="failed", failReason=sil_response["failureMsg"])

    return jsonify({"request_id": request_id}), 202


@app.route("/history", methods=["GET"])
def get_history():
    username = request.headers.get("username", "NA")
    logger.info(f"[History] : Request Received", username)
    prev_requests = RequestRepository.get_all_requests_by_username(username)
    result = [
        {
            "id": r.id,
            "timestamp": r.timestamp,
            "username": username,
            "status": r.status,
            "start": r.start,
            "end": r.end,
            "comment": r.comment,
            "silenceID": r.silenceID
        }
        for r in prev_requests
    ]
    return jsonify(result)


@app.route("/create_user", methods=["POST"])
def create_new_user():
    data = request.json
    user = UserRepository.create_user(
                username=data["username"],
                team=data["team"],
                folder_access=data["folder_access"]
            )
    if Config.DEBUG:
        print(f"user_id: {user}")

    logger.info("[User]: New User Created")
    return jsonify({"user_id": user}), 202


if __name__ == "__main__":
    app.run()
