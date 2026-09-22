import pytest
from main import ItemList

def test_get():
    itemlist = ItemList()
    returnal = itemlist.get()
    assert returnal == {'items': ['item1', 'item2']}