import pytest

from app.tools.tickets import create_ticket


def test_create_ticket_returns_open_ticket():
    t = create_ticket("acme", "service", "Rude staff", "low")
    assert t["ticket_id"].startswith("C-")
    assert t["status"] == "open"


def test_ticket_ids_are_unique():
    ids = {create_ticket("acme", "other", "x", "low")["ticket_id"] for _ in range(50)}
    assert len(ids) == 50


def test_invalid_category_rejected():
    with pytest.raises(ValueError):
        create_ticket("acme", "weather", "x", "low")


def test_invalid_severity_rejected():
    with pytest.raises(ValueError):
        create_ticket("acme", "service", "x", "urgent")


def test_empty_description_rejected():
    with pytest.raises(ValueError):
        create_ticket("acme", "service", "   ", "low")