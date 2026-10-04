import pytest
import threading
from app.tools.tickets import create_ticket
def test_missing_company_id_rejected():
    with pytest.raises(ValueError):
        create_ticket("", "service", "x", "low")


def test_bad_customer_contact_rejected():
    with pytest.raises(ValueError):
        create_ticket("acme", "service", "x", "low", customer_contact="a" * 101)


def test_concurrent_creation_gives_unique_ids():
    ids = []

    def worker():
        for _ in range(25):
            ids.append(create_ticket("acme", "other", "x", "low")["ticket_id"])

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(ids) == 200
    assert len(set(ids)) == 200

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