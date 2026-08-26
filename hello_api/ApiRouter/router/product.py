from fastapi import APIRouter

router=APIRouter()

@router.get("/product")
def get_product():
    return {
        "message":"product_list"
    }

@router.get("/product{product_id}")
def get_product_id(product_id:int):
    return {"product_id":product_id}

