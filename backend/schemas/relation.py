from typing import List

from .article import Article
from .restaurant import Restaurant
from .style_tag import StyleTag
from .user import User

class ArticleRelation(Article):
    author: User
    restaurant: Restaurant
    style_tags: List[StyleTag] = []

class RestaurantRelation(Restaurant):
    articles: List[Article] = []

class StyleTagRelation(Restaurant):
    articles: List[Article] = []

class UserRelation(User):
    articles: List[Article] = []
