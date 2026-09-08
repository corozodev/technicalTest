"""Deterministic, valid data factories used by the UI tests."""

from __future__ import annotations

import os
import random
from dataclasses import dataclass
from datetime import date


FIRST_NAMES = ("Avery", "Jordan", "Morgan", "Taylor", "Riley")
LAST_NAMES = ("Rivera", "Nguyen", "Patel", "Bennett", "Santos")
DEPARTMENTS = ("Quality", "Engineering", "Operations", "Support")


@dataclass(frozen=True)
class UserData:
    first_name: str
    last_name: str
    email: str
    age: str
    salary: str
    department: str


@dataclass(frozen=True)
class PracticeFormData:
    first_name: str
    last_name: str
    email: str
    gender: str
    mobile: str
    birth_date: date
    subject: str
    hobby: str
    address: str
    state: str
    city: str


def _rng(stream: str) -> random.Random:
    # Set QA_SEED to replay exactly the same values reported by a failing run.
    return random.Random(f"{os.getenv('QA_SEED', 'demoqa-suite')}:{stream}")


def make_user(stream: str = "user") -> UserData:
    rng = _rng(stream)
    first_name = rng.choice(FIRST_NAMES)
    last_name = rng.choice(LAST_NAMES)
    token = rng.randint(10000, 99999)
    return UserData(
        first_name=first_name,
        last_name=last_name,
        email=f"qa_{stream}_{token}@example.com",
        age=str(rng.randint(22, 60)),
        salary=str(rng.randrange(45000, 100001, 5000)),
        department=rng.choice(DEPARTMENTS),
    )


def make_practice_form_data() -> PracticeFormData:
    rng = _rng("practice-form")
    return PracticeFormData(
        first_name=rng.choice(FIRST_NAMES),
        last_name=rng.choice(LAST_NAMES),
        email=f"qa.practice.{rng.randint(10000, 99999)}@example.com",
        gender="Female",
        mobile="9" + "".join(str(rng.randrange(10)) for _ in range(9)),
        birth_date=date(1993, 6, 15),
        subject="Maths",
        hobby="Sports",
        address=f"{rng.randint(100, 999)} Quality Avenue",
        state="NCR",
        city="Delhi",
    )
