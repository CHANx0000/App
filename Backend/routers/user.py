from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["users"])

# ── In-memory store ───────────────────────────────────────────────────────────
_users: list[dict] = []
_next_id = 1


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
    global _next_id
    if not request.name.strip():
        raise HTTPException(status_code=422, detail="Name cannot be empty.")
    if request.age < 0 or request.age > 150:
        raise HTTPException(status_code=422, detail="Age must be between 0 and 150.")
    if request.gender not in ("male", "female", "other"):
        raise HTTPException(status_code=422, detail="Gender must be male, female, or other.")

    record = {
        "id": _next_id,
        "name": request.name.strip(),
        "age": request.age,
        "gender": request.gender,
    }
    _users.append(record)
    _next_id += 1
    return record


@router.get("/users", response_model=UsersListResponse)
def list_users():
    return UsersListResponse(users=_users)
