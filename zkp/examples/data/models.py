"""
This is just to discover the data models and their expected schema
"""
from typing import Literal, Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator


class AccountInformation(BaseModel):
    """The data schema model for account"""
    account_number: str = Field(max_length=13, min_length=13)
    routing_number: Optional[str] = Field(default=None, max_length=8, min_length=8)


class AccountTransaction(BaseModel):
    """The data schema model for the account transaction"""
    amount: float = Field(default=0.0, ge=0.0)
    type: Literal['withdraw', 'deposit'] = Field(default='deposit')
    account_information: AccountInformation


class TransactionModel(BaseModel):
    """The data schema model for transactions"""
    source_account_transaction: AccountTransaction
    sink_account_transaction: AccountTransaction
    transaction_date: datetime = Field(default_factory=datetime.utcnow)

    @validator('sink_account_transaction')
    def passwords_match(cls, v, values, **kwargs):
        if 'source_account_transaction' in values:
            assert values['source_account_transaction'].type != v['sink_account_transaction'], \
                "The source and sink account transaction types are the same"

        return v
