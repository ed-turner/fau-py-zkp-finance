import hashlib
import random

from .data.models import Proof


def prove_password(password: str, challenge: str) -> Proof:
    """
    This function will take a password and generates a proof of knowledge
    of the password without revealing the password itself

    :param password: The password
    :param challenge: The challenge
    :return: The proof
    """
    # Hash the password
    hashed_password = hashlib.sha1(password).hexdigest()

    # Generate a random salt and hash the salted password
    salt = str(random.randint(1, 1000000))
    salted_password = hashed_password + salt

    hashed_salted_password = hashlib.sha1(salted_password.encode('utf-8')).hexdigest()

    # Generate a random number
    r = random.randint(1, 1000000)

    # Calculate the response to the challenge
    response = (r + int(challenge, 16) * int(hashed_salted_password, 16)) % 1000000

    # Generate the proof
    proof = Proof(salt=salt, random_number=r, response=response)

    return proof
