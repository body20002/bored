from pydantic.dataclasses import dataclass

@dataclass
class Activity:
    activity: str
    availability: float
    type: str
    participants: int
    price: float
    accessibility: str
    duration: str
    kidFriendly: bool
    link: str
    key: int


