import orjson
import hashlib

from zkp.core.prover import prove_password
from zkp.core.verifier import verify_password

from .data.models import TransactionModel, AccountTransaction, AccountInformation
from .data.serializer import json_serializer


if __name__ == "__main__":

    print("Assembling the data")

    # example source account information
    example_source_account = AccountInformation(
        account_number="0"*13
    )

    # example sink account information
    example_sink_account = AccountInformation(
        account_number="0" * 12 + "1"
    )

    # example source transaction
    example_source_transaction = AccountTransaction(
        account_information=example_source_account, type="deposit", amount=1.0
    )

    # example sink transaction
    example_sink_transaction = AccountTransaction(
        account_information=example_sink_account, type="withdraw", amount=1.0
    )

    # example transaction
    example_transaction = TransactionModel(
        sink_account_transaction=example_sink_transaction,
        source_account_transaction=example_source_transaction
    )

    # serializes the data
    json_serialized_data = orjson.dumps(
        example_transaction.dict(), default=json_serializer
    )

    challenge = "5"

    hashed_json_serialized_data = hashlib.sha1(json_serialized_data)

    example_proof = prove_password(
            password=json_serialized_data,
            challenge=challenge
    )

    if verify_password(
        proof=example_proof,
        challenge=challenge,
        hashed_password=hashed_json_serialized_data
    ):
        print("We were able to verify the proof")
    else:
        print("The proof verification failed")
        print(example_proof)
        print(hashed_json_serialized_data.hexdigest())



