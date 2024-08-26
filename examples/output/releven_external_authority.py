from pydantic import BaseModel, AnyUrl

class ExternalAuthority(BaseModel):
    class Config:
        title = "External Authority"
    external_authority_display_name: str
    external_authority_url: AnyUrl


