from api.plugins import dto_factory

from tables.activities import Activities


_ActivitiesDTO = dto_factory("ActivitiesDTO", Activities)
_ReadActivitiesDTO = dto_factory("ReadActivitiesDTO", Activities, exclude=["id"])

# redefine to get rid of LSP annoying complain
ActivitiesDTO = _ActivitiesDTO
ReadActivitiesDTO = _ReadActivitiesDTO
