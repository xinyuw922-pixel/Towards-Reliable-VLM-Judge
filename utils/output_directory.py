"""Protect source paths and preserve existing outputs before regeneration."""

from pathlib import Path
import sys
import tempfile


def validate_output_directory(path: Path, *, source_roots: tuple[Path, ...] = ()) -> Path:
    """Resolve an output and reject broad, symlinked or source-overlapping paths."""
    path = Path(path).absolute()
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError(f'Output must not traverse a symlink: {path}')
    path = path.resolve()
    repo = Path(__file__).resolve().parents[1]
    protected = (Path.home().resolve(), repo, Path.cwd().resolve())
    if len(path.parts) < 3 or any(path == p or path in p.parents for p in protected):
        raise ValueError(f'Refusing unsafe output directory: {path}')
    system_roots = ('etc', 'usr', 'bin', 'sbin', 'lib', 'lib64', 'boot', 'dev', 'proc', 'sys', 'run')
    source_dirs = ('tools', 'utils', 'scripts', 'requirements', 'environments', 'assets', '.github', '.git')
    if (path.parts[1] in system_roots or '.git' in path.parts
            or any(path == repo / name or repo / name in path.parents for name in source_dirs)):
        raise ValueError(f'Refusing system or source-code directory: {path}')
    for source in source_roots:
        source = Path(source).resolve(strict=True)
        if path == source or path in source.parents or source in path.parents:
            raise ValueError(f'Output overlaps source directory: {path} / {source}')
    if path.exists() and not path.is_dir():
        raise ValueError(f'Output is not a directory: {path}')
    return path


def prepare_output_directory(path: Path, *, source_roots: tuple[Path, ...] = (),
                             overwrite: bool = True) -> Path:
    """Create output without deleting existing files; retain old output in a backup."""
    path = validate_output_directory(path, source_roots=source_roots)
    if path.exists():
        if not overwrite:
            raise FileExistsError(path)
        backup = Path(tempfile.mkdtemp(prefix=f'.{path.name}.backup-', dir=path.parent))
        try:
            path.rename(backup / path.name)
        except BaseException:
            backup.rmdir()
            raise
        print(f'Previous output preserved at: {backup / path.name}', file=sys.stderr)
    path.mkdir(parents=True, exist_ok=False)
    return path
