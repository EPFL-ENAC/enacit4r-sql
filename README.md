# ENAC-IT4R Python SQL Utils

A Python library of SQL utils that are commomly used in the EPFL ENAC IT infrastructure:
 
 * `QueryBuilder`: a class to build SQL queries with multiple related models and to facilitate results paging, sort and filters from a REST entry point.

## Usage
To include the SQL library in your project:

```shell
poetry add git+https://github.com/EPFL-ENAC/enacit4r-sql#someref
```

Note: `someref` should be replaced by the commit hash, tag or branch name you want to use.

### QueryBuilder

Note: WIP, query parameters to be modelized

```python
from enacit4r_sql.utils.query import QueryBuilder

# Example of a query on Study model with a filter and a join on Builing model
query_builder = QueryBuilder(model=Study,
    filter = { "$building": { "$and": [ { "altitude": { "$gte": 1000 } }, { "climate_zone": ["Csa"] } ]}},
    sort = ["name", "ASC"],
    range = [0, 9],
    joinModels = { "$building": Building })

# TODO use query_builder to build a query
```