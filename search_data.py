import json
import requests

def parse_content_links(res_json: json) -> list[str]:
    edges = res_json['data']['xdt_shortcode_media']['edge_sidecar_to_children']['edges']
    links = []
    for edge in edges:
        node = edge['node']
        # indexing the link of highest quality image
        if node['is_video']:
            links.append(node['video_url'])
        else:
            links.append(node['display_resources'][-1]['src'])

    return links

search_query = 'a'

# Initial page to get CSRF token
url = 'https://www.instagram.com/accounts/login/'

session = requests.Session()  # Use a session object to persist cookies
response = session.get(url)
csrf_token = session.cookies.get('csrftoken')  # Extract CSRF token from cookies

graphql_url = 'https://www.instagram.com/api/graphql'

headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.8",
    "content-type": "application/x-www-form-urlencoded",
    "sec-ch-ua": '"Not A(Brand";v="99", "Brave";v="121", "Chromium";v="121"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Linux\"",
    "x-asbd-id": "129477",
    "x-csrftoken": csrf_token,
    "x-fb-friendly-name": "PolarisSearchBoxRefetchableQuery",
    "x-fb-lsd": "h8X5BFP5SjC0osfBshe0wc",
    "x-ig-app-id": "936619743392459",
    "Referer": "https://www.instagram.com/",
}

# The body payload from your fetch request, adjusted if necessary
data = {
    "av": "0",
    "__d": "www",
    "__user": "0",
    "__a": "1",
    "__req": "15",
    "__hs": "19757.HYP:instagram_web_pkg.2.1..0.1",
    "dpr": "1",
    "__ccg": "UNKNOWN",
    "__rev": "1011213034",
    "__s": "0dwyfn:i9q988:6rjrgl",
    "__hsi": "7331786191526987932",
    "__dyn": "7xeUjG1mxu1syUbFp60DU98nwgU7SbzEdF8aUco2qwJw5ux609vCwjE1xoswIwuo2awlU-cw5Mx62G3i1ywOwv89k2C1Fwc60AEC7U2czXwae4UaEW2G1NwwwNwKwHw8Xxm16wUwtEvw4JwJCwLyES1Twoob82ZwrUdUbGwmk1xwmo6O1FwlE6PhA6bxy4UjK5V8",
    "__csr": "ghMIZEnatiKWimJ4AXGjZ4AAGlkGKrh9aXDUDVVQh7ByqxeleXx6h3VWJeunnzVGBCkwoKXQeGJVKiAGyHCUB5h4q9zuVVe9zEBz5p9t162OfzFFokx6aw05eIxq1bg4S581D9U2aBm0czw1Q4hckM9-0EodotxC0sp03lo3uG444Zwwxy0lCm0yU0KWcwboMkwkUeo02ELw",
    "__comet_req": "7",
    "fb_dtsg": "NAcPQAaGFGwhyU98wdOSTA7yCi4K6DOE5irur2Bz8P_Qeb4IBIhTD5Q:17865379441060568:1706767704",
    "jazoest": "26037",
    "lsd": "h8X5BFP5SjC0osfBshe0wc",
    "__spin_r": "1011213034",
    "__spin_b": "trunk",
    "__spin_t": "1707064498",
    "fb_api_caller_class": "RelayModern",
    "fb_api_req_friendly_name": "PolarisSearchBoxRefetchableQuery",
    "variables": '{"data":{"context":"blended","include_reel":"true","query":"'+ search_query +'","rank_token":"","search_surface":"web_top_search"},"hasQuery":true}',
    "server_timestamps": "true",
    "doc_id": "7134903286586471"
}


cookies = {
    "csrftoken": csrf_token,
}

response = session.post(graphql_url, headers=headers, data=data, cookies=cookies)

print('Content snippets:')
print('\tStatus Code:', response.status_code)
print('\tResponse Headers:', str(response.headers)[:100])
print('\tContent Snippet:', response.text[:100], '\n')

post_json_file = 'search_response.json'
try:
    res_json = response.json()

    if 'data' in res_json and 'extensions' in res_json:
        print("Response JSON contains 'data' attribute.")
    else:
        print("Response JSON structure is unexpected.")

    with open(post_json_file, 'w', encoding='utf-8') as f:
        json.dump(res_json, f, ensure_ascii=False, indent=4)

    print (f'Response JSON written to file "{post_json_file}"')

except ValueError:
    print('Failed to parse response as JSON.')

"""
post_link_file = 'search_link.txt'
content_links = parse_content_links(res_json)
with open(post_link_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(content_links))
print(f'Post links written to "{post_link_file}"')
"""

print("CSRF token:", csrf_token)