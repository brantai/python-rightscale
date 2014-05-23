from rightscale.rightscale import RightScaleLinkyThing


def test_empty_linky_thing():
    linky = RightScaleLinkyThing()
    assert {} == linky.links


def test_loaded_linky_thing():
    exp = {
            'a': '/path/to/a',
            'mojo': '/somefingelse/blah/blah',
            'thang': '/thang.thang',
            }
    data = []
    for k, v in exp.items():
        data.append({'rel': k, 'href': v})
    linky = RightScaleLinkyThing({'links': data})
    assert exp == linky.links
