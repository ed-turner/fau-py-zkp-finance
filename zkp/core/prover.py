from cryptography.fernet import MultiFernet
import random

from .data.models import Proof


def prove_password(password: str, challenge: str, encryptor: MultiFernet) -> Proof:
    """
    This function will take a password and generates a proof of knowledge
    of the password without revealing the password itself

    :param password: The password
    :param challenge: The challenge
    :param encryptor: The encryption algorithm
    :return: The proof
    """
    # Hash the password
    hashed_password = encryptor.encrypt(password.encode('utf-8')).decode()

    # Generate a random salt and hash the salted password
    salt = str(random.randint(1, 1000000))
    salted_password = hashed_password + salt
    hashed_salted_password = encryptor.encrypt(salted_password.encode('utf-8')).decode()

    # Generate a random number
    r = random.randint(1, 1000000)

    # Calculate the response to the challenge
    response = (r + int(challenge, 16) * int(hashed_salted_password, 16)) % 1000000

    # Generate the proof
    proof = Proof(salt=salt, random_number=r, response=response)

    return proof
