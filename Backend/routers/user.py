from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from db import get_connection

router = APIRouter(prefix="/api", tags=["users"])


# ── Pydantic models ───────────────────────────────────────────────────────────
class UserCreateRequest(BaseModel):
    name: str
    age: int
    gender: str  # "male" | "female" | "other"


class UserRecord(BaseModel):
    id: int
    name: str
    age: int
    gender: str


class UsersListResponse(BaseModel):
    users: list[UserRecord]


# ── Endpoints ─────────────────────────────────────────────────────────────────
@router.post("/users", response_model=UserRecord, status_code=201)
def create_user(request: UserCreateRequest):
    if not request.name.strip():
        raise HTTPException(status_code=422, detail="Name cannot be empty.")
    if request.age < 0 or request.age > 150:
        raise HTTPException(status_code=422, detail="Age must be between 0 and 150.")
    if request.gender not in ("male", "female", "other"):
        raise HTTPException(status_code=422, detail="Gender must be male, female, or other.")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (name, age, gender) VALUES (%s, %s, %s) RETURNING id, name, age, gender",
                (request.name.strip(), request.age, request.gender),
            )
            row = cur.fetchone()
        conn.commit()
    return dict(row)


@router.get("/users", response_model=UsersListResponse)
def list_users():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, age, gender FROM users ORDER BY id")
            rows = cur.fetchall()
    return UsersListResponse(users=[dict(r) for r in rows])
