from sqlmodel import SQLModel, select
from sqlalchemy import func, or_, and_, cast, String, false, true
import json
from importlib import resources
from jsonschema import validate

class ValidationError(Exception):
    """Exception raised for errors in the input parameters."""
    pass

def paramAsDict(param: str):
    """Parse a JSON string into a dictionary

    Args:
        param (str): JSON string

    Returns:
        dict: Dictionary representation of the JSON string, empty dictionary if param is None
    """
    return json.loads(param) if param else {}


def paramAsArray(param: str):
    """Parse a JSON string as a list

    Args:
        param (str): JSON string

    Returns:
        list: List representation of the JSON string, empty list if param is None
    """
    return json.loads(param) if param else []


def validate_params(filter: dict | str, sort: list | str, range: list | str, fields: list | str = []) -> dict:
    """Validate filter, sort and range parameters against a JSON schema.
    
    Args:
        filter (dict | str): Filter parameters
        sort (list | str): Sort parameters
        range (list | str): Range parameters
        fields (list | str): Fields to retrieve
    
    Returns:
        dict: The validated parameters as a dictionary
    
    Raises:
        ValidationError: If the parameters are not valid
    """
    package_name = "enacit4r_sql.schemas"
    resource_name = "query-schema.json"
    with resources.open_text(package_name, resource_name) as json_file:
        schema = json.load(json_file)
    to_validate = {
        "filter": filter if isinstance(filter, dict) else paramAsDict(filter),
        "sort": sort if isinstance(sort, list) else paramAsArray(sort),
        "range": range if isinstance(range, list) else paramAsArray(range),
        "fields": fields if isinstance(fields, list) else paramAsArray(fields),
    }
    try:
        validate(instance=to_validate, schema=schema)
    except Exception as e:
        raise ValidationError(f"Invalid query parameters: {e}")
    return to_validate


class QueryBuilder:
    """Helper class to generate SQL queries based on filter, sort and range parameters, based on a provided model. Limited support for join queries.
    """

    def __init__(self, model: SQLModel, filter: dict, sort: list, range: list, joinModels: dict = {}, validate: bool = False):
        """Initialize the QueryBuilder object with the provided parameters.
        
        Args:
            model (SQLModel): The model to query
            filter (dict): Filter parameters
            sort (list): Sort parameters
            range (list): Range parameters
            joinModels (dict, optional): Dictionary of join models. Defaults to {}.
            validate (bool, optional): Whether to validate the parameters. Defaults to False.
        """
        if validate:
            validate_params(filter, sort, range)
        self.model = model
        self.filter = filter
        self.sort = sort
        self.range = range
        self.joinModels = joinModels

    def build_count_query(self):
        """Count the number of rows that match the filter.

        Returns:
            int: The total count of rows that match the filter.
        """
        return self._apply_filter(select(func.count(func.distinct(self.model.id))))

    def build_query(self, total_count, fields=None):
        """Build a query that retrieves rows that match the filter, sorted and ranged as specified.
        
        Args:
            total_count (int): Total number of rows that match the filter.
            fields (list, optional): List of fields to retrieve. Defaults to None.
        
        Returns:
            tuple: A tuple containing the start index, end index and the query object.
        """
        _query = select(self.model)
        if fields and len(fields):
            columns = [getattr(self.model, field) for field in fields]
            _query = select(*columns)
        query_ = self._apply_filter(_query)
        query_ = self._apply_sort(query_)
        return self._apply_range(query_, total_count)

    def _apply_filter(self, query_):
        return self._apply_model_filter(query_, self.model, self.filter)

    def _apply_model_filter(self, query_, model, filter):
        if len(filter):
            for field, value in filter.items():
                if field == "$and":
                    clause = self._make_and_filter(model, value)
                    if clause is not None:
                        query_ = query_.where(clause)
                elif field == "$or":
                    clause = self._make_or_filter(model, value)
                    if clause is not None:
                        query_ = query_.where(clause)
                elif field in self.joinModels:
                    joinModel = self.joinModels[field]
                    query_ = self._apply_model_filter(query_, joinModel, value)
                else:
                    clause = self._make_column_filter(model, field, value)
                    if clause is not None:
                        query_ = query_.where(clause)
        return query_

    def _make_and_filter(self, model, value):
        and_clauses = []
        for sub_filter in value:
            for sub_field, sub_value in sub_filter.items():
                clause = None
                if sub_field == "$and":
                    clause = self._make_and_filter(model, sub_value)
                elif sub_field == "$or":
                    clause = self._make_or_filter(model, sub_value)
                else:
                    clause = self._make_column_filter(model, sub_field, sub_value)
                if clause is not None:
                    and_clauses.append(clause)
        if len(and_clauses):
            return and_(true(), *and_clauses)
        return None

    def _make_or_filter(self, model, value):
        or_clauses = []
        for sub_filter in value:
            for sub_field, sub_value in sub_filter.items():
                clause = None
                if sub_field == "$and":
                    clause = self._make_and_filter(model, sub_value)
                elif sub_field == "$or":
                    clause = self._make_or_filter(model, sub_value)
                else:
                    clause = self._make_column_filter(model, sub_field, sub_value)
                if clause is not None:
                    or_clauses.append(clause)
        if len(or_clauses):
            return or_(false(), *or_clauses)
        return None

    def _make_column_filter(self, model, field, value):
        column = getattr(model, field)
        clause = None
        if isinstance(value, list):
            if len(value) == 1 and value[0] is None:
                clause = self._make_filter_value(field, column, value[0])
            elif None in value:
                noNoneValues = [v for v in value if v is not None]
                clause = (or_(column.is_(None), column.in_(noNoneValues)))
            else:
                clause = (column.in_(value))
        else:
            clause = self._make_filter_value(field, column, value)
        return clause

    def _make_filter_value(self, field, column, value):
        clause = None
        if field == "id" or isinstance(value, int):
            clause = (column == value)
        elif value is None:
            clause = (column.is_(None))
        elif isinstance(value, dict):
            clause = self._make_filter_object(field, column, value)
        else:
            clause = column == value
        return clause

    def _make_filter_object(self, field, column, value):
        clause = None
        if '$exists' in value:
            if value['$exists']:
                clause = and_(column.isnot(None), cast(column, String) != 'null')
            elif not value['$exists']:
                clause = or_(column.is_(None), cast(column, String) == 'null')

        if '$ge' in value:
            clause = column >= value['$ge']
        if '$gte' in value:
            clause = column >= value['$gte']
        if '$gt' in value:
            clause = column > value['$gt']

        if '$le' in value:
            clause = column <= value['$le']
        if '$lte' in value:
            clause = column <= value['$lte']
        if '$lt' in value:
            clause = column < value['$lt']

        if '$in' in value:
            clause = column.in_(value['$in'])
        if '$nin' in value:
            clause = column.notin_(value['$nin'])

        if '$eq' in value:
            clause = column == value['$eq']
        if '$ne' in value:
            clause = column != value['$ne']

        if '$like' in value:
            clause = column.like(f"%{value['$like']}%")
        if '$ilike' in value:
            clause = column.ilike(f"%{value['$ilike']}%")
        if '$contains' in value:
            clause = column.contains(value['$contains'])

        return clause

    def _apply_sort(self, query_):
        if len(self.sort) == 2:
            sort_field, sort_order = self.sort
            attr = getattr(self.model, sort_field)
            if sort_order and sort_order.lower() == "desc":
                query_ = query_.order_by(attr.desc())
            else:
                query_ = query_.order_by(attr)
        elif len(self.sort) == 1:
            sort_field = self.sort[0]
            attr = getattr(self.model, sort_field)
            query_ = query_.order_by(attr)
        return query_

    def _apply_range(self, query_, total_count):
        if len(self.range) == 2 and self.range[1] >= 0:
            start, end = self.range
            query_ = query_.offset(start).limit(end - start + 1)
            return start, end, query_
        else:
            return 0, total_count, query_
