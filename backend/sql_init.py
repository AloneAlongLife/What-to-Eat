from config import DEBUG
from database.database import async_engine, Base, async_session

from models import *

async def sql_init():
    async with async_engine.begin() as conn:
        if DEBUG:
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    if DEBUG:
        async with async_session() as session:
            session.add(UserModel(**{
                "uuid": "test1",
                "username": "test1",
                "displayname": "test1",
                "hashpassword": "9aed60db6d0a1d9cfadd0ca652cf024ba14e1a488bf44c99ec677064c852877b0970d421ec376b63c830d4bb49908997e165c08b9a4d05c3592b8a14c19765d7",
            }))
            session.add(UserModel(**{
                "uuid": "test2",
                "username": "test2",
                "displayname": "test2",
                "hashpassword": "9aed60db6d0a1d9cfadd0ca652cf024ba14e1a488bf44c99ec677064c852877b0970d421ec376b63c830d4bb49908997e165c08b9a4d05c3592b8a14c19765d7",
            }))

            article1 = ArticleModel(**{
                "uuid": "test",
                "food_score": 5,
                "service_score": 5,
                "environment_score": 5,
                "comment": "test",
                "author_id": 1,
                "cost": 10,
            })
            article2 = ArticleModel(**{
                "uuid": "test2",
                "food_score": 8,
                "service_score": 8,
                "environment_score": 8,
                "comment": "test2",
                "author_id": 1,
                "cost": 1,
            })
            restaurant1 = RestaurantModel(**{
                "uuid": "test1",
                "name": "tr1",
                "location": "456",
                "location_tag": "123",
                "type_tag": "dinner",
                "city": "T",
                "business_hours": [
                    {"rest": True},
                    {"rest": False, "start": 360, "end": 600},
                    {"rest": False, "start": 360, "end": 600},
                    {"rest": False, "start": 360, "end": 600},
                    {"rest": False, "start": 360, "end": 600},
                    {"rest": True},
                    {"rest": True},
                ]
            })
            restaurant2 = RestaurantModel(**{
                "uuid": "test2",
                "name": "tr2",
                "location": "456",
                "location_tag": "123",
                "type_tag": "dinner",
                "city": "K",
                "business_hours": [
                    {"rest": True},
                    {"rest": False, "start": 360, "end": 600},
                    {"rest": False, "start": 360, "end": 600},
                    {"rest": False, "start": 360, "end": 600},
                    {"rest": False, "start": 360, "end": 600},
                    {"rest": True},
                    {"rest": True},
                ]
            })
            tag1 = StyleTagModel(**{
                "tag_name": "0"
            })
            tag2 = StyleTagModel(**{
                "tag_name": "1"
            })
            tag3 = StyleTagModel(**{
                "tag_name": "2"
            })
            article1.style_tags = [tag1, tag2]
            article1.restaurant = restaurant1
            article2.style_tags = [tag2, tag3]
            article2.restaurant = restaurant2
            session.add_all((article1, article2, tag1, tag2, tag3))

            await session.commit()
