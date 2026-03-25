"""CLI tests for code-covered."""

import json
from pathlib import Path

import cli


def _write_coverage_json(tmp_path: Path, source_file: Path, missing_lines: list[int]) -> Path:
    coverage = {
        "files": {
            str(source_file): {
                "executed_lines": [1],
                "missing_lines": missing_lines,
                "excluded_lines": [],
            }
        }
    }
    coverage_path = tmp_path / "coverage.json"
    coverage_path.write_text(json.dumps(coverage))
    return coverage_path


def test_main_no_args_prints_help(capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["code-covered"])
    exit_code = cli.main()
    assert exit_code == 0
    out = capsys.readouterr().out
    assert "Quick start" in out


def test_missing_coverage_file(capsys, monkeypatch, tmp_path):
    missing = tmp_path / "nope.json"
    monkeypatch.setattr("sys.argv", ["code-covered", str(missing)])
    exit_code = cli.main()
    out = capsys.readouterr().out

    assert exit_code == 1
    assert "Coverage file not found" in out


def test_json_output(capsys, monkeypatch, tmp_path):
    source_file = tmp_path / "module.py"
    source_file.write_text("""\
def foo(x):
    if x > 0:
        return x
    return 0
""")

    coverage_path = _write_coverage_json(tmp_path, source_file, missing_lines=[2, 3])

    monkeypatch.setattr(
        "sys.argv",
        ["code-covered", str(coverage_path), "--format", "json", "--source-root", str(tmp_path)],
    )
    exit_code = cli.main()
    out = capsys.readouterr().out

    assert exit_code == 0
    data = json.loads(out)
    assert data["files_analyzed"] == 1
    assert "suggestions" in data


def test_output_file_written(capsys, monkeypatch, tmp_path):
    source_file = tmp_path / "module.py"
    source_file.write_text("""\
def foo(x):
    if x < 0:
        raise ValueError("neg")
    return x
""")

    coverage_path = _write_coverage_json(tmp_path, source_file, missing_lines=[2, 3])
    output_path = tmp_path / "stubs.py"

    monkeypatch.setattr(
        "sys.argv",
        [
            "code-covered",
            str(coverage_path),
            "-o",
            str(output_path),
            "--source-root",
            str(tmp_path),
        ],
    )

    exit_code = cli.main()
    out = capsys.readouterr().out

    assert exit_code == 0
    assert output_path.exists()
    contents = output_path.read_text()
    assert "Auto-generated test stubs" in contents
    assert "Wrote" in out


def test_version_flag(capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["code-covered", "--version"])
    exit_code = cli.main()
    out = capsys.readouterr().out.strip()
    assert exit_code == 0
    assert out == "1.0.0"


def test_diagnose_text(capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["code-covered", "--diagnose"])
    exit_code = cli.main()
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "python_version" in out
    assert "package_version" in out


def test_diagnose_json(capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["code-covered", "--diagnose-json"])
    exit_code = cli.main()
    out = capsys.readouterr().out
    assert exit_code == 0
    data = json.loads(out)
    assert "ok" in data
    assert "checks" in data
    check_names = [c["check"] for c in data["checks"]]
    assert "python_version" in check_names
