from datetime import datetime
from uuid import UUID

from planner.core.models import BaseModel


def test_base_model_extension_instantiation():
    class TestModel(BaseModel):
        pass

    o = TestModel()

    assert isinstance(o.uuid, UUID)
    assert isinstance(o.created_at, datetime)
    assert isinstance(o.updated_at, datetime)


def test_tablename_generation():
    class TestModelOne(BaseModel):
        pass

    class AnotherTestModel(BaseModel):
        pass

    class YetAnotherTESTModel(BaseModel):
        pass

    assert TestModelOne.__tablename__ == "test_model_one"
    assert AnotherTestModel.__tablename__ == "another_test_model"
    assert YetAnotherTESTModel.__tablename__ == "yet_another_test_model"
