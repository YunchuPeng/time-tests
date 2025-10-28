from times import time_range, compute_overlap_time
import pytest


# 1st version
# def test_given_input():
    
#     large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
#     short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)

#     result = compute_overlap_time(large, short)

#     expected = [
#         ("2010-01-12 10:30:00", "2010-01-12 10:37:00"),
#         ("2010-01-12 10:38:00", "2010-01-12 10:45:00"),
#     ]

#     assert result == expected


# def test_no_overlap():
#     r1 = time_range("2020-01-01 00:00:00", "2020-01-01 01:00:00")
#     r2 = time_range("2020-01-01 02:00:00", "2020-01-01 03:00:00")
#     assert compute_overlap_time(r1, r2) == []



# def test_multiple_intervals_overlap():
#     # r1: 10:00-12:00  → [10:00,11:00], [11:00,12:00]
#     r1 = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00", 2)
#     # r2: 10:30-11:30  → [10:30,11:00], [11:00,11:30]
#     r2 = time_range("2010-01-12 10:30:00", "2010-01-12 11:30:00", 2)
#     result = compute_overlap_time(r1, r2)
#     expected = [
#         ("2010-01-12 10:30:00", "2010-01-12 11:00:00"),
#         ("2010-01-12 11:00:00", "2010-01-12 11:30:00"),
#     ]
#     assert result == expected


# def test_touching_boundaries_has_no_overlap():
#     r1 = time_range("2020-01-01 00:00:00", "2020-01-01 01:00:00")
#     r2 = time_range("2020-01-01 01:00:00", "2020-01-01 02:00:00")
#     assert compute_overlap_time(r1, r2) == []




# 2nd version
# @pytest.mark.parametrize(
#     "t1_args, t2_args, expected",
#     [
        
#         (
#             ("2010-01-12 10:00:00", "2010-01-12 12:00:00", 1, 0),
#             ("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60),
#             [
#                 ("2010-01-12 10:30:00", "2010-01-12 10:37:00"),
#                 ("2010-01-12 10:38:00", "2010-01-12 10:45:00"),
#             ],
#         ),
        
#         (
#             ("2010-01-12 10:00:00", "2010-01-12 12:00:00", 2, 0),
#             ("2010-01-12 10:30:00", "2010-01-12 11:30:00", 2, 0),
#             [
#                 ("2010-01-12 10:30:00", "2010-01-12 11:00:00"),
#                 ("2010-01-12 11:00:00", "2010-01-12 11:30:00"),
#             ],
#         ),
        
#         (
#             ("2020-01-01 00:00:00", "2020-01-01 01:00:00", 1, 0),
#             ("2020-01-01 02:00:00", "2020-01-01 03:00:00", 1, 0),
#             [],
#         ),
        
#         (
#             ("2020-01-01 00:00:00", "2020-01-01 01:00:00", 1, 0),
#             ("2020-01-01 01:00:00", "2020-01-01 02:00:00", 1, 0),
#             [],
#         ),
#     ],
#     ids=[
#         "given_example",
#         "multi-interval-partial",
#         "no-overlap",
#         "touching-no-overlap",
#     ],
# )
# def test_overlaps_parametrized(t1_args, t2_args, expected):
#     r1 = time_range(*t1_args)
#     r2 = time_range(*t2_args)
#     assert compute_overlap_time(r1, r2) == expected

# def test_time_range_backwards_raises_error():
#     with pytest.raises(ValueError, match="must be after"):
#         time_range("2020-01-01 10:00:00", "2020-01-01 09:00:00")






# 3rd version
import yaml
import pytest
from times import time_range, compute_overlap_time
from pathlib import Path

# 1. Load fixture.yaml
fixtures_path = Path(__file__).parent.parent / "fixture.yaml"
if not fixtures_path.exists():
    # Fallback in case tests are located in a subdirectory
    fixtures_path = Path(__file__).parent / "fixture.yaml"

with open(fixtures_path, "r", encoding="utf-8") as fh:
    fixtures = yaml.safe_load(fh)

# 2. Convert YAML data into tuples for pytest parametrize
param_list = []
ids = []
for item in fixtures:
    t1_args = tuple(item["time_range_1"])
    t2_args = tuple(item["time_range_2"])
    # Convert expected value from nested lists (YAML) into a list of tuples
    # to match the format returned by compute_overlap_time
    expected = [tuple(x) for x in item["expected"]]
    param_list.append((t1_args, t2_args, expected))
    ids.append(item.get("id") or f"case_{len(ids)}")

@pytest.mark.parametrize("t1_args, t2_args, expected", param_list, ids=ids)
def test_overlaps_parametrized(t1_args, t2_args, expected):
    r1 = time_range(*t1_args)
    r2 = time_range(*t2_args)
    assert compute_overlap_time(r1, r2) == expected


# Negative test (written separately)
def test_time_range_backwards_raises_error():
    with pytest.raises(ValueError, match="must be after"):
        time_range("2020-01-01 10:00:00", "2020-01-01 09:00:00")
