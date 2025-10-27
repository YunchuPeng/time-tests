from times import time_range, compute_overlap_time
import pytest

def test_given_input():
    
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)

    result = compute_overlap_time(large, short)

    expected = [
        ("2010-01-12 10:30:00", "2010-01-12 10:37:00"),
        ("2010-01-12 10:38:00", "2010-01-12 10:45:00"),
    ]

    assert result == expected



def test_no_overlap():
    r1 = time_range("2020-01-01 00:00:00", "2020-01-01 01:00:00")
    r2 = time_range("2020-01-01 02:00:00", "2020-01-01 03:00:00")
    assert compute_overlap_time(r1, r2) == []



def test_multiple_intervals_overlap():
    # r1: 10:00-12:00  → [10:00,11:00], [11:00,12:00]
    r1 = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00", 2)
    # r2: 10:30-11:30  → [10:30,11:00], [11:00,11:30]
    r2 = time_range("2010-01-12 10:30:00", "2010-01-12 11:30:00", 2)
    result = compute_overlap_time(r1, r2)
    expected = [
        ("2010-01-12 10:30:00", "2010-01-12 11:00:00"),
        ("2010-01-12 11:00:00", "2010-01-12 11:30:00"),
    ]
    assert result == expected


def test_touching_boundaries_has_no_overlap():
    r1 = time_range("2020-01-01 00:00:00", "2020-01-01 01:00:00")
    r2 = time_range("2020-01-01 01:00:00", "2020-01-01 02:00:00")
    assert compute_overlap_time(r1, r2) == []



def test_time_range_backwards_raises_error():
    with pytest.raises(ValueError, match="must be after"):
        time_range("2020-01-01 10:00:00", "2020-01-01 09:00:00")
