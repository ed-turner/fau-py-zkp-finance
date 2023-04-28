from cryptography.fernet import MultiFernet

from .data.models import Proof


def verify_password(proof: Proof, challenge: str, hashed_password: str, encryptor: MultiFernet) -> bool:
    """
    This will verify that the proof, challenge, and hashed password, and verifies that the proof is valid

    :param proof: The proof
    :param challenge: The challenge
    :param hashed_password: The hashed password
    :param encryptor: The encryption algorithm
    :return:
    """

    # Hash the salted password
    salted_password = hashed_password + proof.salt
    hashed_salted_password = encryptor.encrypt(salted_password.encode('utf-8')).decode()

    # Calculate the expected response to the challenge
    expected_response = (proof.random_number + int(challenge, 16) * int(hashed_salted_password, 16)) % 1000000

    # Check if the expected response matches the actual response
    return expected_response == proof.response
