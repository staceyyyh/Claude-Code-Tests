from pydantic import BaseModel

class SitemapRequest(BaseModel):
    url: str
    include_both: bool = False
