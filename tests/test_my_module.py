# tests/test_my_module.py

from src.my_module import greet

def test_greet():
    assert greet("World") == "Hello, World!"