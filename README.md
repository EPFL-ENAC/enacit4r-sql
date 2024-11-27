# ENAC-IT4R Python SQL Utils

A Python library of SQL utils that are commomly used in the EPFL ENAC IT infrastructure:
 
 * `QueryBuilder`: a class to build SQL queries with multiple related models and to facilitate results paging, sort and filters from a REST entry point.

## Usage
To include the SQL library in your project:

```shell
poetry add git+https://github.com/EPFL-ENAC/enacit4r-sql#someref
```

Note: `someref` should be replaced by the commit hash, tag or branch name you want to use.

### Filter

A filter specifies the conditions that the data must meet to be included in the result set. The filter is a dictionary that can contain multiple conditions. The criteria are combined with logical operators (`$and`, `$or`).

```python
{
    '$and': [
        {
            '$or': [
                {'types': {'$contains': ['civil-engineer']}},
                {'types': {'$contains': ['architect']}}
            ]
        }, 
        {
            '$or': [
                {'name': {'$ilike': 'archi'}}, 
                {'address': {'$ilike': 'archi'}}
            ]
        }
    ]
}
```

Each criteria is a dictionary with a key that represents the field to filter and a value that represents the condition. The condition is a dictionary with a key that represents the operator and a value that represents the value to compare.

* `$eq`: equal

```python
{'name': {'$eq': 'John'}}
```

* `$ne`: not equal

```python
{'name': {'$ne': 'John'}}
```

* `$lt`: less than

```python
{'age': {'$lt': 18}}
```

* `$lte` or `$le`: less than or equal

```python
{'age': {'$lte': 18}}
```

* `$gt`: greater than

```python
{'age': {'$gt': 18}}
```

* `$gte` or `$ge`: greater than or equal

```python
{'age': {'$gte': 18}}
```

* `$ilike`: case-insensitive like

```python
{'name': {'$ilike': 'john'}}
```

* `$like`: like

```python
{'name': {'$like': 'john'}}
```

* `$contains`: array contains another array

```python
{'types': {'$contains': ['civil-engineer', 'architect']}}
```

* `$in`: in

```python
{'type': {'$in': ['civil-engineer', 'architect']}}
# can be simplified to
{'type': ['civil-engineer', 'architect']}
```

* `$nin`: not in

```python
{'types': {'$nin': ['civil-engineer', 'architect']}}
```

* `$exists`: check is null or not

```python
{'name': {'$exists': True}}
```

Note: The operators can be extended when models are joined (1-to-many relationship).

### Sort

The sort specification is a list which first item is the field to sort and the second is the direction of the sort (`ASC` or `DESC`).

```python
['name', 'ASC']
```

Notes:

* The default direction is `ASC`.
* The sort specification by multiple fields is not supported (yet).

### Range

The range specification is a list with two items: the start and the end positions (0-based).

For instance to get the first 10 results (offset 0, limit 10), the range would be:

```python
[0, 9]
```

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