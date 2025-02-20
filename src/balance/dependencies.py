from typing import Annotated

from fastapi import Depends

from balance.service import BalanceService

BalanceServiceDep = Annotated[BalanceService, Depends(BalanceService)]