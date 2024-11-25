from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
import models, schemas
from database import AsyncSessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/orders/", response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Create order
        db_order = models.Order(**{k: v for k, v in order.model_dump().items() if k != 'order_items'})
        db.add(db_order)
        await db.commit()
        await db.refresh(db_order)

        # Create order items
        for item in order.order_items:
            db_item = models.OrderItem(**item.model_dump(), order_id=db_order.id)
            db.add(db_item)

        await db.commit()
        await db.refresh(db_order)

        # Fetch the complete order with items
        result = await db.execute(
            select(models.Order)
            .options(selectinload(models.Order.order_items))
            .filter(models.Order.id == db_order.id)
        )
        order_with_items = result.scalar_one()

        return order_with_items
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/orders/", response_model=List[schemas.Order])
async def get_orders(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(
            select(models.Order)
            .options(selectinload(models.Order.order_items))
            .offset(skip)
            .limit(limit)
        )
        orders = result.scalars().all()
        return orders
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/orders/{order_id}", response_model=schemas.Order)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            select(models.Order)
            .options(selectinload(models.Order.order_items))
            .filter(models.Order.id == order_id)
        )
        order = result.scalar_one_or_none()

        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")

        return order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)