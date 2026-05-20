import hashlib
import re
from datetime import datetime
from modals.store import USERS, pm, counter

class AuthController:

    @staticmethod
    def get_by_email(email: str):
        return next(
            (u for u in USERS.values() if u["email"] == email), None
        )

    @staticmethod
    def get_by_id(uid: int):
        return USERS.get(int(uid))

    @staticmethod
    def email_exists(email: str) -> bool:
        return any(u["email"] == email for u in USERS.values())

    @staticmethod
    def register(name: str, email: str, password: str, role: str = "customer") -> dict:
        uid = counter.next("user")
        USERS[uid] = {
            "id": uid, "name": name, "email": email,
            "password": pm.hash(password),
            "role": role, "phone": "", "address": "",
            "created_at": datetime.now().strftime("%Y-%m-%d")
        }
        return USERS[uid]

    @staticmethod
    def verify(email: str, password: str):
        user = AuthController.get_by_email(email)
        if user and pm.verify(user["password"], password):
            return user
        return None

    @staticmethod
    def change_password(uid: int, old_pw: str, new_pw: str) -> bool:
        user = USERS.get(int(uid))
        if user and pm.verify(user["password"], old_pw):
            user["password"] = pm.hash(new_pw)
            return True
        return False

auth_ctrl = AuthController()
