import os
import pydump.cd


def test_cd():
    cwd = os.getcwd()
    with pydump.cd.cd('pydump'):
        sub = os.getcwd()
        assert os.path.join(cwd, 'pydump') == sub
    assert os.getcwd() == cwd
