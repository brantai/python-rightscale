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
