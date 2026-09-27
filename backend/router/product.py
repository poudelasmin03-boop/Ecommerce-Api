from models.product import Product
from fastapi import FastAPI,APIRouter,UploadFile,File,Form,Depends,HTTPException
from database.db import get_db
from models.product import Product,Addtocart,Wishlist
from sqlalchemy.orm import Session
import  os
from fastapi.staticfiles import StaticFiles
from router.user import get_current_user
import shutil
router = APIRouter(
  prefix="/product",
  tags=["Products"]
)

app = FastAPI()
#### folder createing
folder = "products/"

os.makedirs(folder,exist_ok=True)



### GET ALL PRODUCTS
@router.get("/")
async def all_product(db:Session=Depends(get_db)):
  products = db.query(Product).all()
  return{
    "products":products
  }


####  SEARCH PRODUCT BY NAME
@router.get("/search/")
async def search_product(name:str,db:Session=Depends(get_db)):
  product = db.query(Product).filter(Product.name == name).first()

  if not product:
    return HTTPException(
      status_code=404,
      detail = "Product not found"
    )

  return{
    "product":product
  }


###### INSERT PRODUCT
@router.post("/")
async def add_product(
  name:str=Form(...),
  price:float=Form(...),
  stock:int=Form(...),
  category:str=Form(...),
  description:str=Form(...),
  image:UploadFile=File(...),
  db:Session=Depends(get_db)
):
  

  file_path = os.path.join(folder,image.filename)

  with open(file_path, "wb") as buffer:
    shutil.copyfileobj(image.file,buffer)


  new_product = Product(
    name = name,
    price = price,
    stock = stock,
    description = description,
    category =category,
    image =image.filename
  )  

  db.add(new_product)
  db.commit()
  db.refresh(new_product)
  return new_product
  



##### DELETE PRODUCT 
@router.delete("/{id}")
async def delete_product(id:int,db:Session=Depends(get_db)):
  product = db.query(Product).filter(Product.id == id).first()

  if not product:
    raise HTTPException(
      status_code= 400,
      detail="Product not found"
    )

  db.delete(product)
  db.commit()
  return {
    "message":"Successfully deleted.."
  }





# ==================================================
# ==========Start of Add to cart====================
# ===================================================

##### Add to cart section

@router.post("/add/{pid}")
async def add_to_cart(
  pid:int,
  current_user=Depends(get_current_user),
  db:Session=Depends(get_db)
):

##### checking if product available or not and return the query 
  product = db.query(Product).filter(Product.pid==pid).first()

  if  not product:
    raise HTTPException(
      status_code=400,
      detail = "Product not found"
    )

  user_id = current_user['userid']

  ### checking already  existing on not
  checked_product = db.query(Addtocart).filter(
    Addtocart.user_id == user_id,
    Addtocart.product_id ==pid
  ).first()

  if checked_product:
    quantity+=1


  addcart = Addtocart(
    product_id = pid,
    user_id = user_id,
    quantity=1,
    product = product
  )

  db.add(addcart)
  db.commit()
  db.refresh(addcart)


  return {
    "addcart":addcart,
    "message":"Successfully added"
  }


######Display the  items  

@router.get("/addtocart")
async def display_addtocart(
  wishlistid :int,
  db:Session=Depends(get_db),
  current_user = Depends(get_current_user)
):
  user_id = current_user["userid"]

  #### Display the items of only login user
  items = db.query(Addtocart).filter(
    Addtocart.user_id == user_id,
    
  ).all()

  if not items:
    return{
      "Messaage":"Items arenot added by you.."
    }

  return{
    "items":items
  }




### REMOVE FROM ADD TO CART
@router.delete("/addtocart/{cartid}")
async def remove_cart(
  cartid:int,
  db:Session=Depends(get_db),
  current_user=Depends(get_current_user)
):
  user_id = current_user["userid"]


  ##### Checking is the items is belogs to current user

  item = db.query(Addtocart).filter(
    Addtocart.user_id == user_id,
    Addtocart.cartid == cartid
  ).first()

  db.delete(item)
  db.commit()

  return{
    "message":"Successfully deleted the items "
  }
  


# ==================================================
# ==========End of Add to cart====================
# ===================================================

# #####=========================================
# ======= Starting  Wishlist part  is Here=======
# ================================================


###### ADD TO WISHLIST

@router.post("/wishlist/{pid}")
async def add_to_wishlist(
  pid:int,
  current_user=Depends(get_current_user),
  db:Session=Depends(get_db) 
):

  #### checking to product exists or not
  product = db.query(Product).filter(Product.pid == pid).first()
  if not product:
    raise HTTPException(
      status_code=400,
      detail="Product not found"
    )

  user_id = current_user["userid"]

  favourite = db.query(Wishlist).filter(
    Wishlist.product_id == pid,
    Wishlist.user_id == user_id
  ).first()


  if favourite:
    raise HTTPException(
      status_code= 401,
      detail = "Already added product"
    )


  item = Wishlist(
    product_id = pid,
    user_id = user_id,
    product = product
  )

  db.add(item)
  db.commit()
  db.refresh(item)



  return{
    "item":item,
    "message":"Product successfully added to wishlist"
  }




#### Display wishlist product


@router.get("/wishlist")
async def get_wishlist(
  db:Session=Depends(get_db),
  current_user = Depends(get_current_user)
):

  user_id =current_user["userid"]

  items = db.query(Wishlist).filter(
    Wishlist.user_id == user_id
  ).all()


  return{
    "items":items
  }


###### DELETE FROM A WISHLIST
@router.delete("/wishlist/{wishlistid}")
async def delete_wishlist(
  wishlistid:int,
  pid:int,
  db:Session=Depends(get_db),
  current_user=Depends(get_current_user)  
):

 


  user_id = current_user['userid']

  ### checked item is belongs to the a authenticated user
  item = db.query(Wishlist).filter(
    Wishlist.wishlistid == wishlistid,
    Wishlist.user_id == user_id
  ).filter


  db.delete(item)
  db.commit()
  return{
    "message":"Product deleted from wishlist"
  }
 
#####===============================
# ======= End of    Wishlist part  is Here=======
# =================================
