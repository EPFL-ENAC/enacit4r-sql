from enacit4r_sql.utils.query import validate_params, ValidationError

def test_validate_empty_params():
  try:
    validate_params({}, [], [])
  except ValidationError as e:
    assert False, f"Error: {e}"
  try:
    validate_params("{}", "[]", "[]")
  except ValidationError as e:
    assert False, f"Error: {e}"
  try:
    validate_params(None, None, None)
  except ValidationError as e:
    assert False, f"Error: {e}"

def test_validate_filter_eq():
  try:
    validate_params({"stars": { "$eq": 1 }}, [], [])
  except ValidationError as e:
    assert False, f"Error: {e}"
  try:
    validate_params({"name": { "$eq": "john" }}, [], [])
  except ValidationError as e:
    assert False, f"Error: {e}"

def test_validate_filter_ne():
  try:
    validate_params({"stars": { "$ne": 1 }}, [], [])
  except ValidationError as e:
    assert False, f"Error: {e}"
  try:
    validate_params({"name": { "$ne": "john" }}, [], [])
  except ValidationError as e:
    assert False, f"Error: {e}"

def test_validate_filter_exists():
  try:
    validate_params({"name": { "$exists": True }}, [], [])
  except ValidationError as e:
    assert False, f"Error: {e}"
  try:
    validate_params({"name": { "$exists": False }}, [], [])
  except ValidationError as e:
    assert False, f"Error: {e}"
  try:
    validate_params({"name": { "$exists": 1 }}, [], [])
    assert False
  except ValidationError as e:
    pass
  try:
    validate_params({"name": { "$exists": "true" }}, [], [])
    assert False
  except ValidationError as e:
    pass

def test_validate_filter_gt():
  try:
    validate_params({"stars": { "$gt": 1 }}, [], [])
  except ValidationError as e:
    assert False, f"Error: {e}"
  try:
    validate_params({"name": { "$gt": "john" }}, [], [])
    assert False
  except ValidationError as e:
    pass

def test_validate_filter_gte():
  try:
    validate_params({"stars": { "$gte": 1 }}, [], [])
  except ValidationError as e:
    assert False, f"Error: {e}"
  try:
    validate_params({"name": { "$gte": "john" }}, [], [])
    assert False
  except ValidationError as e:
    pass

def test_validate_filter_lt():
  try:
    validate_params({"stars": { "$lt": 1 }}, [], [])
  except ValidationError as e:
    assert False, f"Error: {e}"
  try:
    validate_params({"name": { "$lt": "john" }}, [], [])
    assert False
  except ValidationError as e:
    pass

def test_validate_filter_lte():
  try:
    validate_params({"stars": { "$lte": 1 }}, [], [])
  except ValidationError as e:
    assert False, f"Error: {e}"
  try:
    validate_params({"name": { "$lte": "john" }}, [], [])
    assert False
  except ValidationError as e:
    pass

def test_validate_filter_in():
  try:
    validate_params({"name": { "$in": ["john", "doe"] }}, [], [])
  except ValidationError as e:
    assert False, f"Error: {e}"
  try:
    validate_params({"stars": { "$in": [1, 2, 3] }}, [], [])
  except ValidationError as e:
    assert False, f"Error: {e}"
    
def test_validate_filter_nin():
  try:
    validate_params({"name": { "$nin": ["john", "doe"] }}, [], [])
  except ValidationError as e:
    assert False, f"Error: {e}"
  try:
    validate_params({"stars": { "$nin": [1, 2, 3] }}, [], [])
  except ValidationError as e:
    assert False, f"Error: {e}"

def test_validate_filter_and():
  try:
    validate_params({"$and": [ {"stars": { "$ge": 1 }}, {"title": { "$like": "Drone" }} ]}, [], [])
  except ValidationError as e:
    assert False, f"Error: {e}"

def test_validate_filter_or():
  try:
    validate_params({"$or": [ {"stars": { "$ge": 1 }}, {"title": { "$like": "Drone" }} ]}, [], [])
  except ValidationError as e:
    assert False, f"Error: {e}"

def test_validate_filter_and_or():
  try:
    validate_params({"$and": [ {"stars": { "$ge": 1 }}, {"$or": [ {"title": { "$like": "Drone" }}, {"title": { "$like": "Robot" }} ]} ]}, [], [])
  except ValidationError as e:
    assert False, f"Error: {e}"

def test_validate_filter_or_and():
  try:
    validate_params({"$or": [ {"stars": { "$ge": 1 }}, {"$and": [ {"title": { "$like": "Drone" }}, {"title": { "$like": "Robot" }} ]} ]}, [], [])
  except ValidationError as e:
    assert False, f"Error: {e}"