# import wtforms.validators

class UsersModel:
    """users model"""

    def __init__(self):
        pass

    def check_username(self, db, username):
        return db.execute(f"SELECT username FROM users WHERE username = ?", username)
    
    def check_email(self, db, email):
        return db.execute(f"SELECT email FROM users WHERE email = ?", email)

    def select_from_user(self, db, user_id, **kwargs):
        return db.execute(
            f"SELECT {','.join(kwargs.keys())} FROM users WHERE id = ?", user_id
        )
    
    def get_user_by_email(self, db, email, *args):
        return db.execute(
            f"SELECT {','.join(['username', *args])} FROM users WHERE email = ?", email
        )

    def update_user_cash(self, db, userId, cash):
        return db.execute(
            "UPDATE users SET cash = ? WHERE id = ?",
            cash,
            userId,
        )

    def update_user_password(self, db, userId, password):
        return db.execute(
            "UPDATE users SET hash = ? WHERE id = ?",
            password,
            userId,
        )
    
    def update_user_confirm(self, db, user_email, confirmed=1):
        return db.execute(
            "UPDATE users SET confirmed = ? WHERE email = ?",
            confirmed,
            user_email,
        )

    def create_user(self, db, **kwargs):
        return db.execute(
            "INSERT INTO users (username, email, hash) VALUES(?, ?, ?)",
            kwargs["username"],
            kwargs["email"],
            kwargs["password"],
        )
