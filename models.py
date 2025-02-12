from datetime import datetime
from typing import List, Optional

from fastapi import Query
from pydantic import BaseModel

from .helpers import normalize_public_key, parse_nostr_private_key
from .nostr.key import PrivateKey


class CalendarSettings(BaseModel):
    nostr_private_key: str
    relays: str = ""

    @property
    def relays_list(self) -> List[str]:
        return self.relays.split(',')

    @property
    def private_key(self) -> PrivateKey:
        return parse_nostr_private_key(self.nostr_private_key)

    @property
    def public_key(self) -> str:
        return self.private_key.public_key.hex()



class CreateSchedule(BaseModel):
    wallet: str = Query(...)
    name: str = Query(...)
    start_day: int = Query(..., ge=0, le=6)
    end_day: int = Query(..., ge=0, le=6)
    start_time: str = Query(...)
    end_time: str = Query(...)
    amount: float = Query(..., ge=0)
    timeslot: int = Query(30, ge=5)
    currency: str = Query('sat')
    public_key: Optional[str] = Query(None)


class CreateUnavailableTime(BaseModel):
    start_time: str = Query(...)
    end_time: Optional[str] = Query(None)
    schedule: str = Query(...)
    name: Optional[str] = Query(None)


class CreateAppointment(BaseModel):
    name: str = Query(...)
    email: str = Query(None)
    nostr_pubkey: str = Query(None)
    info: str = Query(None)
    start_time: str = Query(...)
    end_time: str = Query(...)
    schedule: str = Query(...)

class UpdateAppointment(BaseModel):
    name: Optional[str] = Query(None)
    email: Optional[str] = Query(None)
    nostr_pubkey: Optional[str] = Query(None)
    info: Optional[str] = Query(None)
    start_time: Optional[str] = Query(None)
    end_time: Optional[str] = Query(None)
    schedule: Optional[str] = Query(None)


class Schedule(BaseModel):
    id: str
    wallet: str
    name: str
    start_day: int
    end_day: int
    start_time: str
    end_time: str
    amount: float
    timeslot: int
    currency: str
    public_key: Optional[str]

    @property
    def availabe_days(self):
        return list(range(self.start_day, self.end_day + 1))
    
    @property
    def pubkey_hex(self):
        if self.public_key:
            return normalize_public_key(self.public_key)
        return None


class UnavailableTime(BaseModel):
    id: str
    name: str
    start_time: str
    end_time: str
    schedule: str
    created_at: datetime


class Appointment(BaseModel):
    id: str
    name: str
    email: Optional[str]
    nostr_pubkey: Optional[str]
    info: Optional[str]
    start_time: str
    end_time: str
    schedule: str
    paid: bool
    created_at: datetime
