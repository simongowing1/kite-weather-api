import pytest
from conditions import KiteConditions, assess


def test_too_calm():
    ok, msg = assess(10.0)
    assert ok is False
    assert "Too calm" in msg


def test_too_strong():
    ok, msg = assess(60.0)
    assert ok is False
    assert "Too strong" in msg


def test_good_conditions():
    ok, msg = assess(25.0)
    assert ok is True
    assert "Great kite weather" in msg


def test_boundary_min():
    ok, _ = assess(15.0)
    assert ok is True


def test_boundary_max():
    ok, _ = assess(50.0)
    assert ok is True


def test_just_below_min():
    ok, _ = assess(14.9)
    assert ok is False


def test_just_above_max():
    ok, _ = assess(50.1)
    assert ok is False


def test_custom_conditions():
    custom = KiteConditions(min_wind_kmh=20.0, max_wind_kmh=40.0)
    assert assess(15.0, custom)[0] is False
    assert assess(30.0, custom)[0] is True
    assert assess(45.0, custom)[0] is False
