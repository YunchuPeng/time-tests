import datetime


def time_range(start_time, end_time, number_of_intervals=1, gap_between_intervals_s=0):
    start_time_s = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time_s = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    
    if end_time_s <= start_time_s:
        raise ValueError(f"end_time ({end_time}) must be after start_time ({start_time})")
    
    d = (end_time_s - start_time_s).total_seconds() / number_of_intervals + gap_between_intervals_s * (1 / number_of_intervals - 1)
    sec_range = [(start_time_s + datetime.timedelta(seconds=i * d + i * gap_between_intervals_s),
                  start_time_s + datetime.timedelta(seconds=(i + 1) * d + i * gap_between_intervals_s))
                 for i in range(number_of_intervals)]
    return [(ta.strftime("%Y-%m-%d %H:%M:%S"), tb.strftime("%Y-%m-%d %H:%M:%S")) for ta, tb in sec_range]


# def compute_overlap_time(range1, range2):
#     overlap_time = []
#     for start1, end1 in range1:
#         for start2, end2 in range2:
#             low = max(start1, start2)
#             high = min(end1, end2)
#             overlap_time.append((low, high))
#     return overlap_time


def compute_overlap_time(range1, range2):
    overlap_time = []
    for start1, end1 in range1:
        for start2, end2 in range2:
            low = max(start1, start2)
            high = min(end1, end2)
            if low < high:               
                overlap_time.append((low, high))
    return overlap_time


if __name__ == "__main__":
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    print(compute_overlap_time(large, short))

















# Answers UCL-COMP0233-25-26/RSE-Classwork#21
import requests
import datetime

def _format_timestamp(ts):
    """Helper: convert unix timestamp to formatted string."""
    return datetime.datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M:%S")

def iss_passes(lat, lon, alt=0, days=1, min_elevation=30, api_key=None):
    """
    Query the N2YO visualpasses API and return list of (start_str, end_str) tuples.
    Parameters:
      lat, lon: observer latitude and longitude (floats)
      alt: observer altitude in meters (int)
      days: number of days to look ahead (int)
      min_elevation: minimum elevation angle to consider (int)
      api_key: API key string (if None, caller must provide)
    Returns:
      list of (start_time_str, end_time_str), times formatted "%Y-%m-%d %H:%M:%S"
    Note: real API path may require slightly different parameters — adapt if needed.
    """
    if api_key is None:
        raise ValueError("api_key is required for iss_passes")

    # Satellite ID 25544 is ISS
    # Example endpoint format from instructions: 
    # https://api.n2yo.com/rest/v1/satellite/visualpasses/25544/{lat}/{lon}/{alt}/{days}/{min_elevation}&apiKey={key}
    url = f"https://api.n2yo.com/rest/v1/satellite/visualpasses/25544/{lat}/{lon}/{alt}/{days}/{min_elevation}&apiKey={api_key}"

    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    # Expecting data['passes'] to be a list of dicts that include unix timestamps.
    # According to many examples the keys are 'startUTC' and 'endUTC',
    # but if the API differs, adapt accordingly.
    passes = data.get("passes") or data.get("visualpasses") or data.get("response") or []
    results = []
    for p in passes:
        # try common keys
        start_ts = p.get("startUTC") or p.get("start") or p.get("start_timestamp") or p.get("startTime")
        end_ts = p.get("endUTC") or p.get("end") or p.get("end_timestamp") or p.get("endTime")
        if start_ts is None or end_ts is None:
            continue
        results.append((_format_timestamp(start_ts), _format_timestamp(end_ts)))
    return results
