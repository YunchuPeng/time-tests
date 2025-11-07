from unittest.mock import patch, Mock
from times import iss_passes

def test_iss_passes_parsing_and_formatting():
    # prepare fake JSON similar to API
    fake_json = {
        "passes": [
            {"startUTC": 1700000000, "endUTC": 1700000300},
            {"startUTC": 1700004000, "endUTC": 1700004300}
        ]
    }

    # create a fake response object
    fake_resp = Mock()
    fake_resp.json.return_value = fake_json
    fake_resp.raise_for_status.return_value = None

    with patch("times.requests.get", return_value=fake_resp) as mock_get:
        api_key = "DUMMYKEY"
        result = iss_passes(56, 0, alt=0, days=5, min_elevation=50, api_key=api_key)
        # expected formatted time strings
        import datetime
        expected = [
            (datetime.datetime.fromtimestamp(1700000000).strftime("%Y-%m-%d %H:%M:%S"),
             datetime.datetime.fromtimestamp(1700000300).strftime("%Y-%m-%d %H:%M:%S")),
            (datetime.datetime.fromtimestamp(1700004000).strftime("%Y-%m-%d %H:%M:%S"),
             datetime.datetime.fromtimestamp(1700004300).strftime("%Y-%m-%d %H:%M:%S")),
        ]
        assert result == expected

        # also assert that the requests.get was called with a URL that includes our api_key
        called_url = mock_get.call_args[0][0]
        assert "DUMMYKEY" in called_url
