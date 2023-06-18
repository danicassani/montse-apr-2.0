import pytest

def test_test():
    assert True

def test_user_creation():
    from db.models import User
    user = User(id = 1, name = "Alexander Alex Ander")
    assert user != None
    assert user.id == 1
    assert user.name == "Alexander Alex Ander"
    assert user.exp == 0
    assert user.intervalic_level == 1
    assert user.table_name == "user"
    assert user.attribute_list == ["id", "name", "exp", "intervalic_level", "table_name"]

def test_model_creation():
    from db.models import Model
    model = Model()
    assert model != None
    assert model.table_name == "model"
    assert model.attribute_list == ["table_name"]



