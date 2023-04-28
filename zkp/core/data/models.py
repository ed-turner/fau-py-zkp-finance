from pydantic import BaseModel


class Proof(BaseModel):
    """The data schema model for the proof"""
    salt: str
    random_number: int
    response: int
