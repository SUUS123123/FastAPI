from fastapi import APIRouter

from app.api.v1 import categories, customers, products, purchases

router = APIRouter()
router.include_router(categories.router)
router.include_router(products.router)
router.include_router(customers.router)
router.include_router(purchases.router)
