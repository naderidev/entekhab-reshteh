from pydantic import BaseModel


class University(BaseModel):
    id: int
    title: str = None
    province: str = None
    city: str = None


class AcceptanceHistoryItem(BaseModel):
    rank: int
    acceptance: str = None


class PackData(BaseModel):
    detail: University = None
    possibility: str = None