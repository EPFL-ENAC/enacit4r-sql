from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy.dialects.postgresql import JSONB as JSON
from enacit4r_sql.utils.query import QueryBuilder

class Author(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    email: str
    institutions: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    article_id: Optional[int] = Field(default=None, foreign_key="article.id", ondelete="CASCADE")

    # relationships
    article: Optional["Article"] = Relationship(back_populates="authors")


class Article(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    title: str
    stars: int
    # relationships
    authors: List["Author"] = Relationship(back_populates="article")
    
def test_empty_count_query():
    builder = QueryBuilder(Article, {}, [], [])
    query = builder.build_count_query()
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT count(distinct(article.id)) AS count_1 FROM article"

def test_count_query():
    builder = QueryBuilder(Article, {"title": { "$like": "drone" }}, ["title", "desc"], [0,9])
    query = builder.build_count_query()
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT count(distinct(article.id)) AS count_1 FROM article WHERE article.title LIKE :title_1"

def test_empty_query():
    builder = QueryBuilder(Article, {}, [], [])
    start, end, query = builder.build_query(1)
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT article.id, article.title, article.stars FROM article"

def test_empty_query_with_sort():
    builder = QueryBuilder(Article, {}, ["title", "desc"], [])
    start, end, query = builder.build_query(1)
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT article.id, article.title, article.stars FROM article ORDER BY article.title DESC"

def test_empty_query_with_range():
    builder = QueryBuilder(Article, {}, [], [0, 9])
    start, end, query = builder.build_query(1)
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT article.id, article.title, article.stars FROM article LIMIT :param_1 OFFSET :param_2"

def test_eq_query():
    builder = QueryBuilder(Author, {"name": { "$eq": "John Doe" }}, [], [])
    start, end, query = builder.build_query(1)
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT author.id, author.name, author.email, author.institutions, author.article_id FROM author WHERE author.name = :name_1"

def test_eq2_query():
    builder = QueryBuilder(Author, {"name": "John Doe"}, [], [])
    start, end, query = builder.build_query(1)
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT author.id, author.name, author.email, author.institutions, author.article_id FROM author WHERE author.name = :name_1"

def test_ne_query():
    builder = QueryBuilder(Author, {"name": { "$ne": "John Doe" }}, [], [])
    start, end, query = builder.build_query(1)
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT author.id, author.name, author.email, author.institutions, author.article_id FROM author WHERE author.name != :name_1"

def test_in_num_query():
    builder = QueryBuilder(Article, {"stars": { "$in": [1, 2] }}, [], [])
    start, end, query = builder.build_query(1)
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT article.id, article.title, article.stars FROM article WHERE article.stars IN (__[POSTCOMPILE_stars_1])"

def test_nin_num_query():
    builder = QueryBuilder(Article, {"stars": { "$nin": [1, 2] }}, [], [])
    start, end, query = builder.build_query(1)
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT article.id, article.title, article.stars FROM article WHERE (article.stars NOT IN (__[POSTCOMPILE_stars_1]))"

def test_lt_query():
    builder = QueryBuilder(Article, {"stars": { "$lt": 1 }}, [], [])
    start, end, query = builder.build_query(1)
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT article.id, article.title, article.stars FROM article WHERE article.stars < :stars_1"

def test_lte_query():
    builder = QueryBuilder(Article, {"stars": { "$lte": 1 }}, [], [])
    start, end, query = builder.build_query(1)
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT article.id, article.title, article.stars FROM article WHERE article.stars <= :stars_1"

def test_le_query():
    builder = QueryBuilder(Article, {"stars": { "$le": 1 }}, [], [])
    start, end, query = builder.build_query(1)
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT article.id, article.title, article.stars FROM article WHERE article.stars <= :stars_1"

def test_gt_query():
    builder = QueryBuilder(Article, {"stars": { "$gt": 1 }}, [], [])
    start, end, query = builder.build_query(1)
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT article.id, article.title, article.stars FROM article WHERE article.stars > :stars_1"

def test_gte_query():
    builder = QueryBuilder(Article, {"stars": { "$gte": 1 }}, [], [])
    start, end, query = builder.build_query(1)
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT article.id, article.title, article.stars FROM article WHERE article.stars >= :stars_1"

def test_ge_query():
    builder = QueryBuilder(Article, {"stars": { "$ge": 1 }}, [], [])
    start, end, query = builder.build_query(1)
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT article.id, article.title, article.stars FROM article WHERE article.stars >= :stars_1"

def test_in_num_query():
    builder = QueryBuilder(Article, {"stars": { "$ge": 1 }}, [], [])
    start, end, query = builder.build_query(1)
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT article.id, article.title, article.stars FROM article WHERE article.stars >= :stars_1"


def test_like_query():
    builder = QueryBuilder(Article, {"title": { "$like": "Drone" }}, [], [])
    start, end, query = builder.build_query(1)
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT article.id, article.title, article.stars FROM article WHERE article.title LIKE :title_1"

def test_ilike_query():
    builder = QueryBuilder(Article, {"title": { "$ilike": "drone" }}, [], [])
    start, end, query = builder.build_query(1)
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT article.id, article.title, article.stars FROM article WHERE lower(article.title) LIKE lower(:title_1)"

def test_contains_query():
    builder = QueryBuilder(Author, {"institutions": { "$contains": ["CERN", "MIT"] }}, [], [])
    start, end, query = builder.build_query(1)
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT author.id, author.name, author.email, author.institutions, author.article_id FROM author WHERE author.institutions @> :institutions_1"

def test_in_query():
    builder = QueryBuilder(Author, {"name": { "$in": ["Max Planck", "Albert Einstein"] }}, [], [])
    start, end, query = builder.build_query(1)
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT author.id, author.name, author.email, author.institutions, author.article_id FROM author WHERE author.name IN (__[POSTCOMPILE_name_1])"

def test_nin_query():
    builder = QueryBuilder(Author, {"name": { "$nin": ["Max Planck", "Albert Einstein"] }}, [], [])
    start, end, query = builder.build_query(1)
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT author.id, author.name, author.email, author.institutions, author.article_id FROM author WHERE (author.name NOT IN (__[POSTCOMPILE_name_1]))"

def test_exists_query():
    builder = QueryBuilder(Author, {"name": { "$exists": True }}, [], [])
    start, end, query = builder.build_query(1)
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT author.id, author.name, author.email, author.institutions, author.article_id FROM author WHERE author.name IS NOT NULL AND CAST(author.name AS VARCHAR) != :param_1"

def test_not_exists_query():
    builder = QueryBuilder(Author, {"name": { "$exists": False }}, [], [])
    start, end, query = builder.build_query(1)
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT author.id, author.name, author.email, author.institutions, author.article_id FROM author WHERE author.name IS NULL OR CAST(author.name AS VARCHAR) = :param_1"

def test_and_query():
    builder = QueryBuilder(Article, {"$and": [ {"stars": { "$ge": 1 }}, {"title": { "$like": "Drone" }} ]}, [], [])
    start, end, query = builder.build_query(1)
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT article.id, article.title, article.stars FROM article WHERE article.stars >= :stars_1 AND article.title LIKE :title_1"

def test_or_query():
    builder = QueryBuilder(Article, {"$or": [ {"stars": { "$ge": 1 }}, {"title": { "$like": "Drone" }} ]}, [], [])
    start, end, query = builder.build_query(1)
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT article.id, article.title, article.stars FROM article WHERE article.stars >= :stars_1 OR article.title LIKE :title_1"

def test_and_or_query():
    builder = QueryBuilder(Article, { "$and": [ {"id": 1}, {"$or": [ {"stars": { "$ge": 1 }}, {"title": { "$like": "Drone" }} ]} ]}, [], [])
    start, end, query = builder.build_query(1)
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT article.id, article.title, article.stars FROM article WHERE article.id = :id_1 AND (article.stars >= :stars_1 OR article.title LIKE :title_1)"

def test_invalid_filter_field_query():
    builder = QueryBuilder(Article, {"invalid": { "$exists" : True }}, [], [])
    try:
        builder.build_query(1)
        assert False
    except Exception as e:
        assert True

def test_invalid_sort_field_query():
    builder = QueryBuilder(Article, {}, ["invalid", "desc"], [])
    try:
        builder.build_query(1)
        assert False
    except Exception as e:
        assert True

def test_join_query():
    builder = QueryBuilder(Article, {"$author": {"name": {"$ilike": "john"}}}, [], [], joinModels={"$author": Author})
    start, end, query = builder.build_query(1)
    # TODO automate this
    query = query.join(Author, Author.id == Article.id).distinct()
    assert query is not None
    #print(as_sql(query))
    assert as_sql(query) == "SELECT DISTINCT article.id, article.title, article.stars FROM article JOIN author ON author.id = article.id WHERE lower(author.name) LIKE lower(:name_1)"


def as_sql(query):
    return "".join(str(query).split("\n"))