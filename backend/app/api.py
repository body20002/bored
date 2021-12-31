from collections import namedtuple
from enum import Enum
import random
import json
from typing import Optional
from fastapi import APIRouter, status, HTTPException

from app.activity import Activity

router = APIRouter()

@router.get("/")
def hello_world():
    return {"msg": "hello world!"}


class ActivityParticipants(str, Enum):
    alone = "alone"
    with_a_frined = "with a friend"
    with_the_gang = "with the gang"
    party = "party"


class ActivityDuration(str, Enum):
    hours = "hours"
    minutes = "minutes"


class ActivityType(str, Enum):
    busywork = "busywork"
    charity = "charity"
    cooking = "cooking"
    diy = "diy"
    education = "education"
    music = "music"
    recreational = "recreational"
    relaxation = "relaxation"
    social = "social"


class ActivityPrice(str, Enum):
    free = "free"
    inexpensive = "inexpensive"
    expensive = "expensive"


class ActivityAccessibility(str, Enum):
    few_to_no_challenges = "Few to no challenges"
    minor_challenges = "Minor challenges"
    major_challenges = "Major challenges"


@router.get("/activity", response_model=Activity)
def get_activity(key: Optional[str] = None, participants: Optional[ActivityParticipants] = None,
        kid_friendly: Optional[bool] = None, activity_duration: Optional[ActivityDuration] = None,
        activity_type: Optional[ActivityType] = None, activity_price: Optional[ActivityPrice] = None,
        activity_accessibility: Optional[ActivityAccessibility] = None):

    with open("./db/activities.json") as activities_json:
        activities = json.load(activities_json)

    if key:
        for activity in activities:
            if activity["key"] == key:
                return activity

    if participants:
        temp_activities = []
        ParticipantsCount = namedtuple("ParticipantsCount", ["lower_bound", "upper_bound"])
        participants_count = ParticipantsCount(0, 0)
        
        if participants == ActivityParticipants.alone:
            participants_count = ParticipantsCount(1, 1)

        if participants == ActivityParticipants.with_a_frined:
            participants_count = ParticipantsCount(2, 2)

        if participants == ActivityParticipants.with_the_gang:
            participants_count = ParticipantsCount(3, 4)

        if participants == ActivityParticipants.party:
            participants_count = ParticipantsCount(5, 99999)

        for activity in activities:
            if participants_count.lower_bound <= activity["participants"] <= participants_count.upper_bound :
                temp_activities.append(activity)
        activities = temp_activities

    if kid_friendly is not None:
        temp_activities = []
        for activity in activities:
            if activity["kidFriendly"] == kid_friendly:
                temp_activities.append(activity)
        activities = temp_activities

    if activity_duration:
        temp_activities = []
        for activity in activities:
            if activity["duration"] == activity_duration.value:
                temp_activities.append(activity)
        activities = temp_activities

    if activity_type:
        temp_activities = []
        for activity in activities:
            if activity["type"] == activity_type:
                temp_activities.append(activity)
        activities = temp_activities

    if activity_price:
        temp_activities = []
        ActivityPricePound = namedtuple("ActivityPricePound", ["lower_bound", "upper_bound"])
        activity_price_pound = ActivityPricePound(0, 0)

        if activity_price == ActivityPrice.free:
            activity_price_pound = ActivityPricePound(0, 0)

        if activity_price == ActivityPrice.inexpensive:
            activity_price_pound = ActivityPricePound(0, 0.5)

        if activity_price == ActivityPrice.expensive:
            activity_price_pound = ActivityPricePound(0.5, 1)

        for activity in activities:
            if activity_price_pound.lower_bound <= activity["price"] <= activity_price_pound.upper_bound:
                temp_activities.append(activity)
        activities = temp_activities
    
    if activity_accessibility:
        temp_activities = []
        for activity in activities:
            if activity["accessibility"] == activity_accessibility:
                temp_activities.append(activity)
        activities = temp_activities

    activities_length = len(activities)
    if activities_length == 0:
        raise HTTPException(status.HTTP_409_CONFLICT, "Too many queries, try again with less queries") 

    activity = activities[random.randrange(0, len(activities))]
    return activity
