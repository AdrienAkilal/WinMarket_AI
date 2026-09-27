"""Pre-import isolation checks; no database connection or application import."""
import os
from pathlib import Path
from urllib.parse import urlsplit


class ProtectedTargetError(ValueError):
    pass


def protected_paths():
    paths = [Path.home() / 'Desktop' / 'WinMarket AI']
    if os.name == 'nt':
        paths += [Path('C:/WinMarketAI-Postgres'), Path('C:/WM55bis')]
    return paths


def validate_path(path, *, forbidden=None):
    resolved = Path(path).expanduser().resolve()
    for root in forbidden if forbidden is not None else protected_paths():
        root = Path(root).resolve()
        if resolved == root or root in resolved.parents or resolved in root.parents:
            raise ProtectedTargetError('Protected or overlapping filesystem target refused')
    return resolved


def validate_url(url):
    try:
        parsed = urlsplit(url)
        port = parsed.port
    except ValueError:
        raise ProtectedTargetError('Invalid database target') from None
    if parsed.scheme not in ('postgresql', 'postgresql+pg8000'):
        raise ProtectedTargetError('An explicit isolated PostgreSQL target is required')
    if parsed.query or parsed.fragment or parsed.hostname not in ('localhost', '127.0.0.1', '::1'):
        raise ProtectedTargetError('Only unambiguous loopback database targets are accepted')
    if port is None or port == 5432 or not parsed.path.startswith('/wm56_'):
        raise ProtectedTargetError('Protected/default port or database namespace refused')
    if not parsed.username or not parsed.username.startswith('wm56_'):
        raise ProtectedTargetError('A dedicated wm56_ database role is required')
    return url


def validate_environment(values, root):
    validate_path(root)
    for name in ('DATA_DIR', 'OUTPUT_DIR', 'LOCAL_STORAGE_PATH', 'LOGS_DIR', 'EMBEDDING_CACHE_DIR'):
        if values.get(name):
            validate_path(values[name])
    if values.get('DATABASE_URL'):
        validate_url(values['DATABASE_URL'])
    if values.get('BASE_URL'):
        url = urlsplit(values['BASE_URL'])
        if url.hostname not in ('localhost','127.0.0.1','::1') or url.port in (None,8000):
            raise ProtectedTargetError('An explicit separate loopback application port is required')
