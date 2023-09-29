from pydantic import BaseModel, Field
a = Field(int)

# import inspect
# from typing import Optional

class Base(BaseModel):
    class Config:
        from_attributes = True

# def optional(*fields):
#     def dec(_cls: Base):
#         print(_cls.__name__)
#         for field in fields:
#             _cls.__fields__[field].required = False
#             # _cls.__fields__[field].annotation = Optional[_cls.__fields__[field].annotation]
#             # _cls.__fields__[field].default = None
#         return _cls

#     if fields and inspect.isclass(fields[0]) and issubclass(fields[0], BaseModel):
#         cls = fields[0]
#         fields = cls.__fields__
#         return dec(cls)
#     return dec
