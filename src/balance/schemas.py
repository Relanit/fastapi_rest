from pydantic import BaseModel, condecimal


class TopUpBalanceRequest(BaseModel):
    amount: condecimal(gt=0)
