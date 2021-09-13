from typing import Optional

from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import crud
import database
import models
import schemas
from settings import Config

router = APIRouter()

get_db = database.get_db


@router.get("/")
def hello():
    return f"{Config.GREETING} from {Config.HOSTNAME} !"


@router.get("/health")
def health():
    return {"status": {"ok"}}


@router.post("/register",
             response_model=schemas.User,
             response_class=JSONResponse,
             status_code=status.HTTP_201_CREATED)
def create(
    request: schemas.User, db: Session = Depends(get_db)) -> JSONResponse:
    content: dict = request.dict()
    content.pop("id")

    try:
        result_id = crud.create(db, models.User, content)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The data must be unique")

    content.update({"id": result_id})
    return JSONResponse(content, status_code=status.HTTP_201_CREATED)


@router.post("/login",
             response_class=JSONResponse,
             status_code=status.HTTP_200_OK)
def login(
    request: schemas.Login, db: Session = Depends(get_db)) -> JSONResponse:
    user = crud.read(db, models.User,
                     [and_(models.User.name == request.username)])

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The username does not exist",
        )

    if user.password != request.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="The wrong password")

    payload = {"id": user.id, "name": user.name, "email": user.email}

    try:
        auth_session_id = crud.create(db, models.Session, {"payload": payload})
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The data must be unique")

    response = JSONResponse(f"{user.name} login",
                            status_code=status.HTTP_200_OK)
    response.set_cookie("session_id", str(auth_session_id), httponly=True)
    return response


@router.get("/logout",
            response_class=JSONResponse,
            status_code=status.HTTP_200_OK)
def logout(session_id: Optional[str] = Cookie(None),
           db: Session = Depends(get_db)) -> JSONResponse:
    if not session_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not signed in")

    auth_session = crud.read(db, models.Session,
                             [and_(models.Session.id == session_id)])

    if not auth_session:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not signed in")

    username = auth_session.payload['name']

    crud.delete(db, models.Session, [and_(models.Session.id == session_id)])

    response = JSONResponse(f"{username} logout",
                            status_code=status.HTTP_200_OK)
    response.set_cookie("session_id", "", expires=0)
    return response


@router.get(
    "/auth",
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
)
def auth(session_id: Optional[str] = Cookie(None),
         db: Session = Depends(get_db)) -> JSONResponse:
    if not session_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not signed in")

    auth_session = crud.read(db, models.Session,
                             [and_(models.Session.id == session_id)])

    if not auth_session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not signed in")

    headers = {
        "X-UserId": str(auth_session.payload["id"]),
        "X-User": auth_session.payload["name"],
        "X-Email": auth_session.payload["email"],
    }
    return JSONResponse(f"{auth_session.payload['name']} authentication",
                        status_code=status.HTTP_200_OK,
                        headers=headers)


@router.put("/edit",
            response_model=schemas.User,
            response_class=JSONResponse,
            status_code=status.HTTP_200_OK)
def edit(
        request: schemas.User,
        db: Session = Depends(get_db),
        session_id: Optional[str] = Cookie(None),
) -> JSONResponse:

    if not session_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not signed in")

    content: dict = request.dict()
    content.pop("id")

    auth_session = crud.read(db, models.Session,
                             [and_(models.Session.id == session_id)])

    if not auth_session:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not signed in")

    user_id = auth_session.payload["id"]

    try:
        crud.update(db, models.User, user_id, content)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="The data must be unique")

    payload = {"id": user_id, "name": request.name, "email": request.email}
    crud.update(db, models.Session, session_id, {"payload": payload})
    content.update({"id": user_id})

    return JSONResponse(content, status_code=status.HTTP_200_OK)
