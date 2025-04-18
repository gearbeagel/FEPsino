import uuid


def generate_random_username():
    return f"user_{uuid.uuid4().hex[:8]}"
