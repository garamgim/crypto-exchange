from app.api.bitmex.auth import *

def test_to_valid_json_with_base_model():
    class TestModel(BaseModel):
        id: int
        name: str
        age: int | None = None

    model_instance = TestModel(id=1, name="John", age=None)
    result = to_valid_json(model_instance)
    expected_result = '{"id":1,"name":"John"}'
    assert result == expected_result

def test_to_valid_json_with_dict():
    data = {"id": 1, "name": "John", "age": None}
    result = to_valid_json(data)
    expected_result = '{"id":1,"name":"John"}'
    assert result == expected_result