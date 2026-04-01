from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from src.models import User, db
from src.app import bcrypt

app = Blueprint("auth", __name__, url_prefix="/auth")


def valid_password(password_hash, password_raw):
    return bcrypt.check_password_hash(password_hash, password_raw)

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()
    if not user or not valid_password(user.password, password):
        return {"message":"Bad username or password"}, HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=str(user.id))
    return {"access_token": access_token}
