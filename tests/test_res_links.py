from nose.tools import raises
from rightscale.rightscale import Resource


def test_empty_linky_thing():
    linky = Resource()
    assert {} == linky.links


def test_resource_repr():
    r = Resource()
    assert r == eval(repr(r))

    r = {
            'a': '/path/to/a',
            'mojo': '/somefingelse/blah/blah',
            'thang': '/thang.thang',
            }
    assert r == eval(repr(r))


def test_loaded_linky_thing():
    exp = {
            'a': '/path/to/a',
            'mojo': '/somefingelse/blah/blah',
            'thang': '/thang.thang',
            }
    data = []
    for k, v in exp.items():
        data.append({'rel': k, 'href': v})
    linky = Resource({'links': data})
    assert exp == linky.links


def test_allow_customize_links():
    """
    Allow custom links independent of original initialization data.
    """
    orig = {
            'a': '/path/to/a',
            'mojo': '/somefingelse/blah/blah',
            'thang': '/thang.thang',
            }
    newmojo = 'another thing yeah'
    exp = dict(orig, mojo=newmojo)
    data = []
    for k, v in orig.items():
        data.append({'rel': k, 'href': v})
    linky = Resource({'links': data})
    linky.links['mojo'] = newmojo
    assert exp == linky.links


def test_str_resource():
    """
    str(resource) should be based on the soul.
    """
    fakey = {'foo': '/foo', 'bar': '/path/to/bar'}
    res = Resource(soul=fakey)
    assert str(fakey) == str(res)


def test_dir_resource():
    """
    dir(resource) should only be based on the embedded links.
    """
    fakey = {'foo': '/foo', 'bar': '/path/to/bar'}
    res = Resource()
    res._links = fakey
    assert set(fakey.keys()) == set(dir(res))


def test_real_resource_attr():
    """
    Resource objects should allow access to attrs named after links.
    """
    fakey = {'foo': '/foo', 'bar': '/path/to/bar'}
    res = Resource()
    res._links = fakey
    res.foo
    res.bar


@raises(AttributeError)
def test_bogus_resource_attr():
    """
    Resource objects should complain when trying to access unknown attrs.
    """
    fakey = {'foo': '/foo', 'bar': '/path/to/bar'}
    res = Resource()
    res.fubar
