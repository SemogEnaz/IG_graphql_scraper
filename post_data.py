import json
import requests
import sys
import datetime

no_debug = any('no-d' in arg for arg in sys.argv)

def parse_post_date(res_json: json) -> str:
    milli_sec_since_epoch = init_parse(res_json)['edge_media_to_caption']['edges'][0]['node']['created_at']
    dt_object = datetime.datetime.fromtimestamp(
        int(milli_sec_since_epoch))
    return str(dt_object)

def parse_comment_count(res_json: json) -> int:
    return init_parse(res_json)['edge_media_parent_comment']['count']

def parse_like_count(res_json: json) -> int:
    return init_parse(res_json)['edge_media_preview_like']['count']

def parse_caption(res_json: json) -> str:
    return init_parse(res_json)['edge_media_to_caption']['edges'][0]['node']['text']

def parse_content_links(res_json: json) -> list[str]:
    links = []
    try:
        edges = init_parse(res_json)['edge_sidecar_to_children']['edges']
        for edge in edges:
            node = edge['node']
            # indexing the link of highest quality image
            if node['is_video']:
                links.append(node['video_url'])
            else:
                links.append(node['display_resources'][-1]['src'])
    except:
        links.append(init_parse(res_json)['display_resources'][-1]['src'])

    return links

def init_parse(res_json: json) -> json:
    return res_json['data']['xdt_shortcode_media']

def extract_shortcode(post_link: str) -> str:
    post_link = post_link[post_link.find('/p/') + 3:]
    post_link = post_link[:post_link.find('/')]
    return post_link

def get_link_n_code() -> str:
    post_link = "https://www.instagram.com/p/C2yssBPtQ0S/?utm_source=ig_web_button_share_sheet"

    for arg in sys.argv[1:]:
        if 'https://' in arg:
            post_link = arg
            break
        if not no_debug: print('\nNo link provided, using default...')

    short_code = extract_shortcode(post_link)
    if not no_debug: print(f'Post Link: {post_link}\nShort Code: {short_code}\n')
    return post_link, short_code

def get_headers(csrf_token: str, post_link: str) -> object:
    return {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.5",
        "content-type": "application/x-www-form-urlencoded",
        "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Brave\";v=\"121\", \"Chromium\";v=\"121\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Linux\"",
        "x-asbd-id": "129477",
        "x-csrftoken": csrf_token,
        "x-fb-friendly-name": "PolarisPostActionLoadPostQueryQuery",
        "x-fb-lsd": "AVp00KSxSKk",
        "x-ig-app-id": "936619743392459",
        "Referer": post_link,
    }

def get_payload(short_code: str) -> object:
    return {
        "av": "0",
        "__d": "www",
        "__user": "0",
        "__a": "1",
        "__req": "3",
        "__hs": "19757.HYP:instagram_web_pkg.2.1..0.0",
        "dpr": "1",
        "__ccg": "UNKNOWN",
        "__rev": "1011213034",
        "__s": "0koxku:cv0yoe:70tehn",
        "__hsi": "7331769549619738950",
        "__dyn": "7xeUjG1mxu1syUbFp60DU98nwgU29zEdEc8co2qwJw5ux609vCwjE1xoswIwuo2awlU-cw5Mx62G3i1ywOwv89k2C1Fwc60AEC7U2czXwae4UaEW2G1NwwwNwKwHw8Xxm16wUwtEvw4JwJCwLyES1Twoob82ZwrUdUbGwmk1xwmo6O1FwlE6PhA6bxy4UjK5V8",
        "__csr": "ghMIZEnatiKWimJ4AXGjZ4AAGlkGKrh9aXDUDVVQh7ByqxeleXx6h3VWJeunnzVGBCkwoKXQeGJVKiAGyHCUB5h4q9zuVVe9zEBz5oN162OfzFEb801jJUmwiQ1dxi0pOu0yFlw38U0t14iwRwdu7o1U404dax11fo2xw63w3Iz1i1jw0aCC",
        "__comet_req": "7",
        "lsd": "AVp00KSxSKk",
        "jazoest": "2902",
        "__spin_r": "1011213034",
        "__spin_b": "trunk",
        "__spin_t": "1707060623",
        "fb_api_caller_class": "RelayModern",
        "fb_api_req_friendly_name": "PolarisPostActionLoadPostQueryQuery",
        "variables": f'{{"shortcode":"{short_code}","fetch_comment_count":40,"fetch_related_profile_media_count":3,"parent_comment_count":24,"child_comment_count":3,"fetch_like_count":10,"fetch_tagged_user_count":null,"fetch_preview_comment_count":2,"has_threaded_comments":true,"hoisted_comment_id":null,"hoisted_reply_id":null}}',
        "server_timestamps": "true",
        "doc_id": "10015901848480474",
    }


# Initial page to get CSRF token
url = 'https://www.instagram.com/accounts/login/'

session = requests.Session()  # Use a session object to persist cookies
response = session.get(url)
csrf_token = session.cookies.get('csrftoken')  # Extract CSRF token from cookies

graphql_url = 'https://www.instagram.com/api/graphql'
post_link, short_code = get_link_n_code()

headers = get_headers(csrf_token, post_link)
data = get_payload(short_code)
cookies = { "csrftoken": csrf_token }

response = session.post(graphql_url, headers=headers, data=data, cookies=cookies)

if not no_debug:
    print('Content snippets:')
    print('\tStatus Code:', response.status_code)
    print('\tResponse Headers:', str(response.headers)[:100])
    print('\tContent Snippet:', response.text[:100], '\n')

try:
    res_json = response.json()

    if not no_debug:
        if 'data' in res_json and 'extensions' in res_json:
            print("Response JSON contains 'data' attribute.")
        else:
            print("Response JSON structure is unexpected.")

        post_json_file = 'post_response.json'
        with open(post_json_file, 'w', encoding='utf-8') as f:
            json.dump(res_json, f, ensure_ascii=False, indent=4)

        print (f'Response JSON written to file "{post_json_file}"')

except ValueError:
    raise ValueError("JSON could not be created!, response error.")

content_links = parse_content_links(res_json)
if no_debug: print(json.dumps(content_links))

if not no_debug:
    post_link_file = 'post_link.txt'
    with open(post_link_file, 'w', encoding='utf-8') as f:
        created_date = parse_post_date(res_json) + '\n\n'
        caption = parse_caption(res_json) + '\n\n'
        f.write(created_date)
        f.write(caption)
        f.write('\n'.join(content_links))

    print(f'Post links written to "{post_link_file}"')
    print(f'CSRF token: {csrf_token}\n')
