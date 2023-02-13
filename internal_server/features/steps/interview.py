from behave import *
from urllib import request, error

use_step_matcher("re")


@given("I perform (?P<method>.+) request to the server (?P<url>.+) with (?P<header>.+)")
def step_impl(context, method, url, header):
    """
    :type context: behave.runner.Context
    :type method: str
    :type url: str
    :type header: str
    """

    req = request.Request(
        f"{context.connection_string}{url}", data=None if method == "GET" else {}
    )
    req.add_header(header, "TEST 123")
    try:
        context.resp = request.urlopen(req)
        context.data = context.resp.read()
    except error.HTTPError as err:
        context.err = err
        context.data = err.read()


@then("I have response with (?P<status>.+) code and content contains (?P<content>.+)")
def step_impl(context, status, content):
    """
    :type context: behave.runner.Context
    :type status: str
    :type content: str
    """

    s = int(status)

    if s == 200:
        fh = context.resp
    else:
        fh = context.err

    assert fh.code == s

    if content:
        print(context.data.decode())
        assert content in context.data.decode()
