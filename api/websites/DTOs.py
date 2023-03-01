from api.plugins import dto_factory

from tables.websites import Websites


_WebsitesDTO = dto_factory("WebsitesDTO", Websites)
_ReadWebsitesDTO = dto_factory("ReadWebsitesDTO", Websites, exclude=["id"])

# redefine to get rid of LSP annoying complain
WebsitesDTO = _WebsitesDTO
ReadWebsitesDTO = _ReadWebsitesDTO

