import mock
from rightscale.util import find_by_name


def test_not_exact_return_all():
    """
    find_by_name() should return all matches when not exact
    """
    nada = mock.MagicMock()
    nada.soul = {'name': 'nada'}
    exp = [nada, nada, nada]
    col = mock.MagicMock()
    col.index.return_value = exp
    ret = find_by_name(col, 'dummy', exact=False)
    assert exp == ret


def test_find_by_name_returns_none():
    """
    find_by_name() should return none for no results
    """
    # empty set
    col = mock.MagicMock()
    col.index.return_value = []
    ret = find_by_name(col, 'dummy')
    assert ret is None

    # non-empty, but no matches
    nada = mock.MagicMock()
    nada.soul = {'name': 'nada'}
    col = mock.MagicMock()
    col.index.return_value = [nada, nada, nada]
    ret = find_by_name(col, 'dummy', exact=True)
    assert ret is None


def test_return_exact_of_multiple():
    """
    find_by_name() should return exact match when multiple found
    """
    exp_name = 'dummy'
    exact = mock.MagicMock()
    exact.soul = {'name': exp_name}
    notme = mock.MagicMock()
    notme.soul = {'name': 'not me'}
    col = mock.MagicMock()
    col.index.return_value = [notme, exact, notme]
    ret = find_by_name(col, exp_name)
    assert exact == ret
