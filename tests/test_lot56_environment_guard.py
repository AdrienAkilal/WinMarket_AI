"""Sentinels only: refusal precedes any connection or write."""
from pathlib import Path
import pytest
from src.core import environment_guard as guard


def test_overlap_and_resolved_path_refused(tmp_path, monkeypatch):
    protected=tmp_path/'preserved'
    protected.mkdir()
    sentinel=protected/'sentinel'
    sentinel.write_bytes(b'unchanged')
    monkeypatch.setattr(guard,'protected_paths',lambda:[protected])
    for candidate in (protected, protected/'child', protected/'..'/'preserved', tmp_path):
        with pytest.raises(guard.ProtectedTargetError):
            guard.validate_path(candidate)
    assert sentinel.read_bytes()==b'unchanged'
    assert guard.validate_path(tmp_path/'new')==tmp_path/'new'


@pytest.mark.parametrize('url',[
    'postgresql://wm56_app@127.0.0.1:5432/wm56_test',
    'postgresql://wm56_app@127.0.0.1:5546/winmarket_app_db',
    'postgresql://wm56_app@127.0.0.1/wm56_test',
    'postgresql://wm56_app@127.0.0.1:5546/wm56_test?port=5432',
    'postgresql://wm56_app@localhost:5546/wm56_test?host=elsewhere',
    'postgresql://wm56_app@external:5546/wm56_test',
])
def test_endpoints_refused_without_connecting(url):
    with pytest.raises(guard.ProtectedTargetError):
        guard.validate_url(url)


def test_init_refuses_before_directory_or_socket(tmp_path, monkeypatch):
    import scripts.local_env as local
    from argparse import Namespace
    calls=[]
    monkeypatch.setattr(local,'port_open',lambda p:calls.append(p))
    target=tmp_path/'must-not-exist'
    with pytest.raises(guard.ProtectedTargetError):
        local.initialize(Namespace(runtime=target,database='wm56_test',pg_port=5432,app_port=8056,pg_bin=None))
    assert not target.exists() and calls==[]


def test_no_env_loading_during_test_collection():
    from src.core import config
    assert config._TEST_MODE is True
    assert not config.ANTHROPIC_API_KEY
