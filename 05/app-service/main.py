from typing import Optional

from fastapi import FastAPI, Cookie, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


class SessionSchema(BaseModel):
    id: str


@app.get("/")
async def root():
    return {"message": "Hello world"}


@app.get("/health")
def health():
    return {"status": {"ok"}}


@app.get('/profile',
         response_model=SessionSchema,
         response_class=JSONResponse,
         status_code=status.HTTP_200_OK)
def get_profile(session_id: Optional[str] = Cookie(None)) -> JSONResponse:
    if not session_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Unauthorized')

    data = {
        'id': session_id,
    }
    content = SessionSchema.parse_obj(data).dict()
    return JSONResponse(content, status_code=status.HTTP_200_OK)
