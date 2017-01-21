import html
import re
import urllib

import bs4
import flask
import grequests


app = flask.Flask(__name__)


TITLE_REQUEST_TIMEOUT = 3  # seconds
TEXT_FOR_UNAVAIL_TITLE = '<Unavailable>'

MENTION_REGEX = re.compile(r'^@(\w+)')
EMOTICON_REGEX = re.compile(r'^\(([a-zA-Z0-9]{1,15})\)')
LINK_REGEX = re.compile(r'^(https?://\S+)')


def parse_message(message):
    mentions, emoticons, links = [], [], []
    for word in message.split():
        mentions.extend(MENTION_REGEX.findall(word))
        emoticons.extend(EMOTICON_REGEX.findall(word))
        links.extend(LINK_REGEX.findall(word))
    links = validate_links(links)
    return (mentions, emoticons, links)


def get_title_from_response(response):
    if not response:
        return TEXT_FOR_UNAVAIL_TITLE
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    if soup.title:
        return html.escape(soup.title.text) or TEXT_FOR_UNAVAIL_TITLE
    else:
        return TEXT_FOR_UNAVAIL_TITLE


def validate_links(links):
    parsable_links = []
    for link in links:
        parsed_link = urllib.parse.urlsplit(link)
        if parsed_link.scheme in ('http', 'https') and parsed_link.netloc:
            parsable_links.append(link)
    responses = grequests.map([
        grequests.get(link, timeout=TITLE_REQUEST_TIMEOUT) for link in parsable_links
    ])
    return [
        {
            'url': link,
            'title': get_title_from_response(response)
        }
        for link, response in zip(parsable_links, responses)
    ]


@app.route('/parse', methods=['POST'])
def parse_endpoint():
    message = flask.request.form.get('message')
    if message is None:
        flask.abort(400)

    mentions, emoticons, links = parse_message(message)

    response = {}
    if mentions:
        response['mentions'] = mentions
    if emoticons:
        response['emoticons'] = emoticons
    if links:
        response['links'] = links

    return flask.jsonify(**response)
