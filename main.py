import pandas as pd

from scrap import get_gmaps_url, extract_lat_lng, Scraper
from parse import parse_json


def main():
    # convert json into dictionary
    filename = "data.json"
    raw_data = parse_json(filename)
    s = Scraper()

    # raw_data contains url we needs to get Google Maps URL
    for i,data in enumerate(raw_data):
        try:
            print(f"Fetching {i+1} of {len(raw_data)}")
            gmaps_url, new_url = get_gmaps_url(data['petfriendly_url'])
            data['gmaps_url'] = gmaps_url
            data['latitude'] = extract_lat_lng(new_url)[0]
            data['longitude'] = extract_lat_lng(new_url)[1]
            
        except Exception as e:
            print(e)
            continue

        try:
            data['address'] = s.get_html(data['search_url']).get_address()
            data['image'] = s.get_image(data['image_url'], data['name'])
        except Exception as e:
            print(e)
            continue


    df = pd.DataFrame(raw_data)
    df.to_excel('output.xlsx', index=False)

if __name__ == "__main__":
    main()