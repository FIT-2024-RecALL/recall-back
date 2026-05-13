def test_example():
    """A simple test to verify the testing framework works"""
    assert 1 + 1 == 2


def test_string_operations():
    """Test basic string operations"""
    text = "hello world"
    assert text.upper() == "HELLO WORLD"
    assert text.split() == ["hello", "world"]