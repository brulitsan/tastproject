from typing import Optional

from pydantic import BaseModel, HttpUrl

from users.models import User


class BaseModelConfig:
    arbitrary_types_allowed = True
    from_attributes = True


class LinkSchema(BaseModel):
    user: User
    url: str
    link_type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None

    class Config(BaseModelConfig):
        pass


class LinksCollectionsSchema(BaseModel):
    link_id: int
    collection_id: int