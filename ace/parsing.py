import html
import re
import urllib

import bs4
import grequests


TITLE_REQUEST_TIMEOUT = 3  # seconds
TEXT_FOR_UNAVAIL_TITLE = '<Unavailable>'

REGEXES = (
    # Since these are evaluated "first-one-wins", keep them ordered by most common type first:
    # (Which I'm only guessing at absent real data!)
    ('mentions', re.compile(r'^@(\w+)\W*$')),
    ('emoticons', re.compile(r'^\(([a-zA-Z0-9]{1,15})\)$')),
    ('links', re.compile(r'^(https?://\S+)$', re.I)),
)


def parse_message(message, session=None):
    result = {}
    for word in message.split():
        for kind, regex in REGEXES:
            found = regex.findall(word)
            if found:
                result.setdefault(kind, []).extend(found)
                break
    if 'links' in result:
        result['links'] = validate_links(result['links'], session)
    return result


def get_title_from_response(response):
    if response and response.ok:
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        if soup.title and soup.title.text:
            return html.escape(soup.title.text)
    return TEXT_FOR_UNAVAIL_TITLE


def validate_links(links, session=None):
    if session is None:
        session = grequests.Session()
    parsable_links = []
    for link in links:
        parsed_link = urllib.parse.urlsplit(link)
        if parsed_link.scheme in ('http', 'https') and parsed_link.netloc:
            # TODO: more sophisticated checking of the parsed bits?
            parsable_links.append(link)
    responses = grequests.map([  # Hopefully concurrent requesting if multiple links
        session.get(link, timeout=TITLE_REQUEST_TIMEOUT) for link in parsable_links
    ])
    return [
        {
            'url': link,
            'title': get_title_from_response(response)
        }
        for link, response in zip(parsable_links, responses)
    ]
