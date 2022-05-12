# from activities.models import Activity as ActivityModel
# from facts.models import Fact as FactModel
# from riddles.models import Riddle as RiddleModel
# from websites.models import Website as WebsiteModel

# from tortoise.contrib.pydantic.creator import pydantic_model_creator
# from pydantic import Field

# Activity = pydantic_model_creator(ActivityModel, name="Activity")
# ActivityIn = pydantic_model_creator(
#     ActivityModel, name="ActivityIn", exclude_readonly=True
# )
# Fact = pydantic_model_creator(FactModel, name="Fact")
# FactIn = pydantic_model_creator(FactModel, name="FactIn", exclude_readonly=True)

# Riddle = pydantic_model_creator(RiddleModel, name="Riddle")
# RiddleIn = pydantic_model_creator(RiddleModel, name="RiddleIn", exclude_readonly=True)

# Website = pydantic_model_creator(WebsiteModel, name="Websites")
# WebsiteIn = pydantic_model_creator(
#     WebsiteModel, name="WebsitesIn", exclude_readonly=True
# )

# there's a bug in tortoise which makes their pydantic_model_creator function not behave correctly
