from pwdlib import PasswordHash


class   Password:
    def __init__(self):
        self.password_hash = PasswordHash.recommended()

    def hash_password(
            self,
            password: str
    ) -> str:
        return self.password_hash.hash(password)

    def verify_password(
            self,
            plain_password: str,
            hashed_password: str
    ) -> bool:
        return self.password_hash.verify(
            plain_password,
            hashed_password
        )

password = Password()