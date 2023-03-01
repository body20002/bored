from api.plugins import dto_factory

from tables.facts import Facts


_FactsDTO = dto_factory("FactsDTO", Facts)
_ReadFactsDTO = dto_factory("ReadFactsDTO", Facts, exclude=["id"])

# redefine to get rid of LSP annoying complain
FactsDTO = _FactsDTO
ReadFactsDTO = _ReadFactsDTO

