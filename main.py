import pandas as pd

from scrap import get_gmaps_url, extract_lat_lng
from parse import parse_json


if __name__ == "__main__":
    # convert json into dictionary
    filename = "result2.json"
    raw_data = parse_json(filename)

    # raw_data contains url we needs to get Google Maps URL
    for data in raw_data:
        try:
            gmaps_url, new_url = get_gmaps_url(data['petfriendly_url'])
            data['gmaps_url'] = gmaps_url
            data['latitude'] = extract_lat_lng(new_url)[0]
            data['longitude'] = extract_lat_lng(new_url)[1]
            print(data)
        except Exception as e:
            print(e)
            continue

    df = pd.DataFrame(raw_data)
    df.to_excel('output.xlsx', index=False)