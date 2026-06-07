from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Discount Service")

class DiscountRequest(BaseModel):
    product_id: str
    quantity: int
    unit_price: float
    promo_code: str | None = None

class DiscountResponse(BaseModel):
    discount_percent: float
    reason: str

@app.get("/health")
def health():
    return {"status": "ok", "service": "discount-service"}

@app.post("/discounts/calculate", response_model=DiscountResponse)
def calculate_discount(req: DiscountRequest):
    # Правило 1: промокод STUDENT10 → 10%
    if req.promo_code == "STUDENT10":
        return DiscountResponse(discount_percent=10.0, reason="Student promo code applied")
    # Правило 2: оптовая скидка при количестве >= 10
    if req.quantity >= 10:
        return DiscountResponse(discount_percent=15.0, reason="Wholesale discount (>=10 items)")
    # Правило 3: большая сумма заказа (≥ 500)
    total = req.quantity * req.unit_price
    if total >= 500:
        return DiscountResponse(discount_percent=5.0, reason="Large order discount")
    # По умолчанию
    return DiscountResponse(discount_percent=0.0, reason="No discount applicable")