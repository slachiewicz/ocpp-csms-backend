from passlib.hash import pbkdf2_sha256 as sha256


async def is_relevant_password(raw_password: str, password_hash: str) -> bool:
    return sha256.verify(raw_password, password_hash)
