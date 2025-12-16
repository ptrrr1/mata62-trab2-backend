import logging

from fastapi import APIRouter, HTTPException, status

from src.controllers.credit_controller import CreditController
from src.custom_types.credit_types import CreditHistoryResponse, CreditHistoryCompleteResponse, CreditBuyRequest

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/credits", tags=["Credits"])


@router.get("/user_id/{id}", summary="Get current credit amount")
def get_user_credits(id: int) -> int:
    response = CreditController.get_user_credits(id)

    if response is None:
        raise HTTPException(status_code=404, detail="User not found")

    return response


@router.get("/history/user_id/{id}", summary="Get credit history")
def get_user_credits_history(id: int) -> list[CreditHistoryResponse]:
    response = CreditController.get_user_credits_history(id)

    if response is None:
        raise HTTPException(status_code=404, detail="User not found")

    return [
        CreditHistoryResponse(amount=r.amount, created_at=r.created_at)
        for r in response
    ]


@router.get("/history/all", summary="Get credit history")
def get_all_credits_history() -> list[CreditHistoryCompleteResponse]:
    response = CreditController.get_all_credits_history()

    return [
        CreditHistoryCompleteResponse(
            id=r.id, user_id=r.user_id, amount=r.amount, created_at=r.created_at
        )
        for r in response
    ]


@router.post(
    "/buy/user_id/{id}",
    status_code=status.HTTP_201_CREATED,
    summary="Create a buy request",
)
def create_buy_request(id: int, t: CreditBuyRequest):
    response = CreditController.create_buy_request(id, t.amount)

    if not response:
        raise HTTPException(status_code=400, detail="Failed to create buy request")

    return dict(message="Request created successfully")


@router.post(
    "/use/user_id/{id}",
    status_code=status.HTTP_201_CREATED,
    summary="Create a buy request",
)
def use_credit(id: int, t: CreditBuyRequest):
    response = CreditController.use_credit(id, t.amount)

    if not response:
        raise HTTPException(status_code=400, detail="Failed to use credits")

    return dict(message="Request created successfully")
