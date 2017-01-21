# ACE: Atlassian Coding Exercise
Chat message parser

## Usage:

Setup:

```
virtualenv -p /usr/local/bin/python3 venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=ace
pip install --editable .
```

Run the Flask dev server:

```
flask run
```

Try some requests:

```
curl -X POST --data-urlencode "message=@bob @john (success) such a cool feature; https://twitter.com/jdorfman/status/430511497475670016" 127.0.0.1:5000/parse
```

Run the tests:

```
python test_ace.py
```

## TODOs:
Things I would do absent the time constraint:

- Write more tests! The current ones are mostly tailored to the examples in the exercise instructions.
- Mock the network dependency (for getting the page titles) in the current tests.
- Research the server to use... I'd like this to be highly concurrent particularly since it spends time doing I/O to get the page titles. Could I set this up in gunicorn?
- Research the most common ways to accept input for such APIs (I chose form data here... is that ideal?).
- Think really hard about whether my parsing regexes are right!
- Performance profiling, particularly in `parse_message` and `validate_links`. Are my regexes and strategies for scanning through the message ideal?
- Security: for page title retrieval, what are the ramifications of my requesting any link the client sends? Do I need to parse the URL more deeply and be more cautious about my outbound requests? (Almost certainly yes.)
- Caching! The outbound requests are relatively expensive; we could probably do some reasonable caching of the retrieved page titles if system load warranted it.
- Consider newer options around asyncio since I'm using Python 3. I chose grequests based on a quick search; is it really the best option? Is the library maintained?
- Are there ramifications from getting all these pages in parallel, particularly with regard to memory usage? If there are a lot of links that direct to large pages could I effectively be DOSed?
- Think more about package setup / deployment / etc. It's been a while since I bootstrapped a new app and I'm not at all sure I've set it all up in an ideal manner here. It definitely feels wonky (pip installs AND setup?? Use of `pip install --editable`?).
- Learn to use Bitbucket and submit this there! :)
