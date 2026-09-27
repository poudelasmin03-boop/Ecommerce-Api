from database.db import Base
from sqlalchemy import Column,Integer,String,VARCHAR,Float,Boolean,ForeignKey
from sqlalchemy.orm import relationship

class Product(Base):
  __tablename__ = "Products"
  pid = Column(Integer,primary_key=True)
  name = Column(VARCHAR(200),nullable=False)
  price =Column(Float,nullable=False)
  stock = Column(Integer,nullable=False)
  category = Column(VARCHAR(200),nullable=False)
  description =Column(VARCHAR(1000),nullable=False)
  image = Column(String(200),nullable=False)





class User(Base):
  __tablename__ ="User"
  userid = Column(Integer,primary_key=True)
  username = Column(String(200),nullable=False)
  email  = Column(String(200),nullable=False)
  password = Column(String(200),nullable=False)
  is_admin = Column(Boolean,default=False,nullable=False)
  is_active =Column(Boolean,nullable=False)




class Addtocart(Base):
  __tablename__ = "Addtocart"
  cartid = Column(Integer,primary_key=True)
  user_id = Column(Integer,ForeignKey("User.userid",ondelete="CASCADE"))
  product_id = Column(Integer,ForeignKey("Products.pid",ondelete="CASCADE"))
  quantity = Column(Integer,nullable=False)
  product = relationship("Product")



class Wishlist(Base):
  __tablename__ = "wishlist"
  wishlistid = Column(Integer,primary_key=True)
  user_id = Column(Integer,ForeignKey("User.userid",ondelete="CASCADE"))
  product_id = Column(Integer,ForeignKey("Products.pid",ondelete="CASCADE"))
  product = relationship("Product")
  
  



#   Python model class → Product
# Database table     → Products