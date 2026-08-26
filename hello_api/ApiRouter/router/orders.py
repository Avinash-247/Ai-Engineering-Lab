from fastapi import APIRouter

# ikkada manam prefix enduku uses chestam ante prathi sari order ani rasa badulu simple ga "/" illa pettu ko varchi, 
router=APIRouter(prefix="/orders",
                 tags=["orders"])
#Tags enduku use chestam ante tag use chey tam valla output andadi okka perfect organization lo untadi ante cagegory wise ga 
# ippudu nenu orders lo use chesa ka batting nuvvu deni run cheste "orders" ani okka pedda hedding laga kanapadi dantlo ney 
# http request untai, so deni valla data anadi messy kadhu
@router.get("/")
def get_orders():
    return {
        "message":"list of orders"
    }

@router.get("/{order_id}")
def get_order_id(order_id:int):
    return {"order_id":order_id}

