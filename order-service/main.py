import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from contextlib import asynccontextmanager

from database import get_order, init_db, save_order
from settings import get_settings

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Order Service", lifespan=lifespan)

class OrderRequest(BaseModel):
    product_id: str
    quantity: int = Field(gt=0)
    promo_code: str | None = None   # добавили

class OrderResponse(BaseModel):
    product_id: str
    quantity: int
    unit_price: float
    total_before_discount: float
    discount_percent: float
    discount_amount: float
    total_after_discount: float

class StoredOrderResponse(BaseModel):
    id: int
    product_id: str
    quantity: int
    unit_price: float
    total: float
    created_at: datetime

class ProductFromService(BaseModel):
    id: str
    name: str
    price: float
    available: bool

@app.get("/health")
def health():
    return {"status": "ok", "service": "order-service"}

@app.post("/orders", response_model=OrderResponse)
async def create_order(order: OrderRequest):
    # 1. Получаем товар
    product = await fetch_product(order.product_id)
    if not product.available:
        raise HTTPException(status_code=400, detail=f"Product '{order.product_id}' not available")

    total_before = product.price * order.quantity

    # 2. Получаем скидку
    discount = await fetch_discount(order.product_id, order.quantity, product.price, order.promo_code)
    discount_percent = discount["discount_percent"]
    discount_amount = total_before * discount_percent / 100.0
    total_after = total_before - discount_amount

    # 3. Сохраняем заказ (сохраняем итоговую сумму)
    save_order({
        "product_id": product.id,
        "quantity": order.quantity,
        "unit_price": product.price,
        "total": total_after,
    })

    return OrderResponse(
        product_id=product.id,
        quantity=order.quantity,
        unit_price=product.price,
        total_before_discount=total_before,
        discount_percent=discount_percent,
        discount_amount=discount_amount,
        total_after_discount=total_after,
    )

@app.get("/orders/{order_id}", response_model=StoredOrderResponse)
def read_order(order_id: int):
    saved = get_order(order_id)
    if not saved:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    return StoredOrderResponse(
        id=saved["id"],
        product_id=saved["product_id"],
        quantity=saved["quantity"],
        unit_price=float(saved["unit_price"]),
        total=float(saved["total"]),
        created_at=saved["created_at"],
    )

async def fetch_product(product_id: str) -> ProductFromService:
    url = f"{settings.product_service_url}/products/{product_id}"
    async with httpx.AsyncClient(timeout=3.0) as client:
        try:
            resp = await client.get(url)
            resp.raise_for_status()
            return ProductFromService.model_validate(resp.json())
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Product service unavailable: {exc}")
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found")
            raise HTTPException(status_code=502, detail="Product service error")

async def fetch_discount(product_id: str, quantity: int, unit_price: float, promo_code: str | None) -> dict:
    url = f"{settings.discount_service_url}/discounts/calculate"
    payload = {
        "product_id": product_id,
        "quantity": quantity,
        "unit_price": unit_price,
        "promo_code": promo_code,
    }
    async with httpx.AsyncClient(timeout=3.0) as client:
        try:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            return resp.json()
        except Exception:
            # Отказоустойчивость: если discount не отвечает, даём скидку 0
            return {"discount_percent": 0.0, "reason": "Discount service unavailable"}