import pytest

from src.app import create_app
from src.models import Role, User, db


@pytest.fixture
def app():
    app = create_app(environment="testing")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def access_token(client):
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(username="john-doe", password="test", role_id=role.id)
    db.session.add(user)
    db.session.commit()

    response = client.post("/auth/login", json={"username": user.username, "password": user.password})
    return response.json["access_token"]
