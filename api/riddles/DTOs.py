from api.plugins import dto_factory

from tables.riddles import Riddles


_RiddlesDTO = dto_factory("RiddlesDTO", Riddles)
_ReadRiddlesDTO = dto_factory("ReadRiddlesDTO", Riddles, exclude=["id"])

# redefine to get rid of LSP annoying complain
RiddlesDTO = _RiddlesDTO
ReadRiddlesDTO = _ReadRiddlesDTO

