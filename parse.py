import json
import re
from urllib.parse import urlencode


def parse_json(filename)-> list:
    result = []

    with open(filename, 'r') as f:
        js = json.load(f)

    for item in js['records']:
        record_id = item['id']
        name = item['fields']['Name']
        category = item['fields']['Type']
        image_url = get_image_url(item['fields']['Image'])
        instagram_url = get_instagram_url(item['fields']['Button'])
        petfriendly_url = convert_url(name, record_id)
        search_url = convert_search_url(item['fields']['SEO:Description'])
        value = {'id': record_id, 'name': name, 'category': category, 'image_url': image_url, 'instagram_url': instagram_url, 'petfriendly_url':petfriendly_url, 'search_url':search_url}
        result.append(value)
    return result

def convert_search_url(text):
    base_url = "https://www.google.com/search?"
    url = base_url + urlencode({'q':text})
    return url

def convert_url(name, record_id):
    name = name.replace(' ', '-').replace('&', '%26').replace('/', '%2F').replace('?', '%3F').replace(':', '%3A').replace('(', '%28').replace(')', '%29').replace("'", '%27').replace("\n", "").replace(',', '%2C')
    base_url = "https://www.petfriendly123.com/pet-friendly/"
    if "¿" in name:
        url = "https://www.petfriendly123.com/pet-friendly?recordId="+record_id
    else:
        url = base_url + name + "/r/" + record_id
    return url

def get_image_url(text):
    # This regex pattern looks for a string that starts with 'http' and is enclosed in parentheses
    match = re.search(r'\((http[^)]+)\)', text)
    if match:
        return match.group(1)  # Returns the URL without the parentheses
    return None
def get_gmaps_url(text):
    text = str(text)
    pattern = r'https://www.google.com/maps/place/[^ ]+'
    match = re.search(pattern, text)
    if match:
        return match.group(0)  # Returns the first URL found
    return None

def get_instagram_url(text):
    # This regex pattern looks for URLs in the href attribute of an anchor tag
    match = re.search(r'href="([^"]+)"', text)
    if match:
        return match.group(1)  # Returns the URL without the surrounding attribute markers
    return None


if __name__ == "__main__":
    filename = "result2.json"
    raw = parse_json(filename)
    print(raw)

    

