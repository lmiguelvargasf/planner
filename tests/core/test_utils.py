import pytest
from planner.core.utils import camel_to_snake


@pytest.mark.parametrize(
    "camel_str,expected",
    [
        pytest.param("Base", "base", id="one_word"),
        pytest.param("UUIDMixin", "uuid_mixin", id="all_caps_word"),
        pytest.param("TimeStampedMixin", "time_stamped_mixin", id="mixed_case_word"),
        pytest.param("Base2Model3", "base2_model3", id="mixed_case_word_with_digits"),
    ],
)
def test_camel_to_snake(camel_str, expected):
    assert camel_to_snake(camel_str) == expected
