from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


__all__ = ["CamelCaseBaseModel", "IsPublicModelMixin", "IsPublicIdModel"]


class CamelCaseBaseModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    @classmethod
    def fields(cls) -> list[str]:
        return list(cls.model_fields.keys())


class IsPublicModelMixin(BaseModel):
    is_public: bool


class IsPublicIdModel(CamelCaseBaseModel):
    id: int
    is_public: bool
