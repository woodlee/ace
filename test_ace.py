import ace.parsing
import json
import requests
import requests_mock
import unittest


class ParsingEndpointTestCase(unittest.TestCase):
    input = ''
    output = {}
    mocked_requests = []  # 3-tuples of (method, request URL, response body)

    def setUp(self):
        self.maxDiff = 10000
        self.app = ace.app.test_client()
        self.session = requests.Session()
        self.adapter = requests_mock.Adapter()
        self.session.mount('mock', self.adapter)
        for mocked_req in self.mocked_requests:
           self.adapter.register_uri(mocked_req[0], mocked_req[1], text=mocked_req[2])

    def runTest(self):
        res = self.app.post('/parse', data={'message': self.input})
        self.assertEqual(json.loads(res.data), self.output)


class SimpleMentiontest(ParsingEndpointTestCase):
    input = '@chris you around?'
    output = {
        'mentions': [
            'chris'
        ]
    }


class MultiMentionTest(ParsingEndpointTestCase):
    input = ' @marty marty @tim @tim joe '
    output = {
        'mentions': [
            'marty',
            'tim',
            'tim'
        ]
    }


class SimpleEmoticonTest(ParsingEndpointTestCase):
    input = 'Good morning! (megusta) (coffee)'
    output = {
        'emoticons': [
            'megusta',
            'coffee'
        ]
    }


class MultiEmoticonTest(ParsingEndpointTestCase):
    input = '(coffee) (coffee) (coffee)'
    output = {
        'emoticons': [
            'coffee',
            'coffee',
            'coffee'
        ]
    }


class ParenthesizedMentionNotParsed(ParsingEndpointTestCase):
    input = 'hey (@foobar) hey'
    output = {}


class NoTitleForNonexistentLink(ParsingEndpointTestCase):
    input = 'this is bad @marty: http://kjwekjtwet'
    output = {
        'mentions': [
            'marty'
        ],
        'links': [
            {
                'url': 'http://kjwekjtwet',
                'title': ace.parsing.TEXT_FOR_UNAVAIL_TITLE
            }
        ]
    }


class SimpleLinkTest(ParsingEndpointTestCase):
    mocked_requests = [
        ('GET', 'http://www.nbcolympics.com', '<title>my_mocked_title</title>')
    ]
    input = 'Olympics are starting soon; http://www.nbcolympics.com'
    output = {
        "links": [
            {
               "url": "http://www.nbcolympics.com",
               "title": "jkdfhsdjfh"
            }
        ]
    }


class AllTokenTypesTest(ParsingEndpointTestCase):
    input = '@bob @john (success) such a cool feature; https://twitter.com/jdorfman/status/430511497475670016'
    output = {
        "mentions": [
           "bob",
           "john"
        ],
        "emoticons": [
            "success"
        ],
        "links": [
            {
                "url": "https://twitter.com/jdorfman/status/430511497475670016",
                "title": "Justin Dorfman on Twitter: &quot;nice @littlebigdetail from @HipChat (shows hex colors when pasted in chat). http://t.co/7cI6Gjy5pq&quot;"
            }
        ]
    }

class ParseMessageTestCase(unittest.TestCase):
    input = ''
    output = {}
    mocked_requests = []  # 3-tuples of (method, request URL, response body)

    def setUp(self):
        self.maxDiff = 10000
        self.session = requests.Session()
        self.adapter = requests_mock.Adapter()
        self.session.mount('mock', self.adapter)
        for mocked_req in self.mocked_requests:
           self.adapter.register_uri(mocked_req[0], mocked_req[1], text=mocked_req[2])

    def runTest(self):
        res = ace.parsing.parse_message(self.input, self.session)
        self.assertEqual(res, self.output)


class ParseMessageTest(ParseMessageTestCase):
    mocked_requests = [
        ('GET', 'http://www.nbcolympics.com', '<title>my_mocked_title</title>')
    ]
    input = 'Olympics are starting soon; http://www.nbcolympics.com'
    output = {
        "links": [
            {
               "url": "http://www.nbcolympics.com",
               "title": "jkdfhsdjfh"
            }
        ]
    }


if __name__ == '__main__':
    unittest.main()