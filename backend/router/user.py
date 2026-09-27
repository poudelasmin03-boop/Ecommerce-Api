from jose import JWTError, jwt

from passlib.context import CryptContext

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from fastapi import FastAPI, APIRouter, Depends, HTTPException, status,Form

from sqlalchemy.orm import Session

from database.db import engine, Base, get_db

from schema.product import Userregister

from models.product import User

from datetime import datetime, timedelta, timezone


app = FastAPI()


# =========================
# ROUTER
# =========================

router = APIRouter(
    prefix="/login",
    tags=["Auth_User"]
)


# =========================
# JWT SETTINGS
# =========================

SECREAT_KEY = "010fb8078932643156a8891a60c0ee9864b66a033a4fc33348c75faa51096ec5"

ALGORITHM = "HS256"


oAuth_scheme = OAuth2PasswordBearer(
    tokenUrl="login/login"
)


# =========================
# PASSWORD
# =========================

pwd_context = CryptContext(
    schemes=["argon2"],
)


ACCESS_TOKEN_EXPIRE_TIME_MINUTES = 15


# =========================
# BLACKLIST
# =========================

blacklisted_token = []


# =========================
# CREATE TOKEN
# =========================

def create_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_TIME_MINUTES
    )

    to_encode.update({
        "exp": expire,
        
    })

    token = jwt.encode(
        to_encode,
        SECREAT_KEY,
        algorithm=ALGORITHM
    )

    return token


# =========================
# REGISTER
# =========================

@router.post("/register")
async def register_account(
    username:str=Form(...),
    email:str=Form(...),
    password:str=Form(...),
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter( User.email == email).first()

    if existing_user:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exist..."
        )

    hashed_pass = pwd_context.hash(password)

    new_user = User(
        username=username,
        password=hashed_pass,
        email=email,
        is_active=True,
        is_admin = False

    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Account Register successfully.."
    }


# =========================
# LOGIN
# =========================

@router.post("/login")
async def login_account(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    username = form_data.username
    password = form_data.password

    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password.."
        )

    if not pwd_context.verify(
        password,
        user.password
    ):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password.."
        )

    access_token = create_token({
        "type": "access",
        "userid": user.userid,
        "username": user.username
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# =========================
# GET CURRENT USER
# =========================

def get_current_user(
    token: str = Depends(oAuth_scheme)
):

    print("TOKEN:", token)

    credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:

        # Check blacklisted token
        if token in blacklisted_token:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been failed"
            )

        # Decode token
        payload = jwt.decode(
            token,
            SECREAT_KEY,
            algorithms=[ALGORITHM]
        )

        # Get data from token
        username = payload.get("username")
        userid = payload.get("userid")
        token_type = payload.get("type")

        # Validate token data
        if username is None:
            raise credentials

        if userid is None:
            raise credentials

        if token_type != "access":
            raise credentials

    except JWTError:

        raise credentials

    return {
        "token":"access",
        "username": username,
        "userid": userid
    }


# =========================
# LOGOUT
# =========================

@router.post("/logout")
async def logout_views(
    token: str = Depends(oAuth_scheme)
):

    blacklisted_token.append(token)

    return {
        "message": "logout"
    }


#