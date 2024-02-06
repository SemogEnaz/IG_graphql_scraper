# IG_graphql_scraper

A web scraper I developed for instagram by investigating the Network requests of instagram.com

## Usage

Provide the program you want to run with some command line args, sit back and enjoy!

### post_data

This will collect the links, caption and creation date for a post. This will be entered into the txt file, the JSON has data more data like comments, tagged users, owner & likes.
`python post_data.py <your link here>`

### search_data

This will collect hashtags and users, count seems to be 55 total.
`python search_data.py <your search query here>`