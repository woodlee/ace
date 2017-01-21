import ace
import json
import unittest


class AceParsingTestCase(unittest.TestCase):
    input = ''
    output = {}

    def setUp(self):
        self.maxDiff = 10000
        self.app = ace.app.test_client()

    def runTest(self):
        res = self.app.post('/parse', data={'message': self.input})
        self.assertEqual(json.loads(res.data), self.output)


class SimpleMentiontest(AceParsingTestCase):
    input = '@chris you around?'
    output = {
        'mentions': [
            'chris'
        ]
    }


class MultiMentionTest(AceParsingTestCase):
    input = ' @marty marty @tim @tim joe '
    output = {
        'mentions': [
            'marty',
            'tim',
            'tim'
        ]
    }


class SimpleEmoticonTest(AceParsingTestCase):
    input = 'Good morning! (megusta) (coffee)'
    output = {
        'emoticons': [
            'megusta',
            'coffee'
        ]
    }


class MultiEmoticonTest(AceParsingTestCase):
    input = '(coffee) (coffee) (coffee)'
    output = {
        'emoticons': [
            'coffee',
            'coffee',
            'coffee'
        ]
    }


class ParenthesizedMentionNotParsed(AceParsingTestCase):
    input = 'hey (@foobar) hey'
    output = {}


class NoTitleForNonexistentLink(AceParsingTestCase):
    input = 'this is bad @marty: http://kjwekjtwet'
    output = {
        'mentions': [
            'marty'
        ],
        'links': [
            {
                'url': 'http://kjwekjtwet',
                'title': ace.ace.TEXT_FOR_UNAVAIL_TITLE
            }
        ]
    }


class SimpleLinkTest(AceParsingTestCase):
    input = 'Olympics are starting soon; http://www.nbcolympics.com'
    output = {
        "links": [
            {
               "url": "http://www.nbcolympics.com",
               "title": "2018 PyeongChang Olympic Games | NBC Olympics"
            }
        ]
    }


class AllTokenTypesTest(AceParsingTestCase):
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


if __name__ == '__main__':
    unittest.main()