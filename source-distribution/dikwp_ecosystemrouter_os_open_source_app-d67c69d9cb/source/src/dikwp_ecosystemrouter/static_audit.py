from pathlib import Path
import ast
from typing import Dict, List

FORBIDDEN_IMPORTS = {"socket", "requests", "httpx", "urllib", "subprocess", "paramiko", "ftplib", "telnetlib"}
FORBIDDEN_CALLS = {"eval", "exec", "compile", "__import__", "system", "popen", "spawn", "remove", "unlink", "rmdir"}


def audit_path(path: str) -> Dict:
    root = Path(path)
    findings: List[Dict] = []
    for py in root.rglob("*.py"):
        try:
            tree = ast.parse(py.read_text(encoding="utf-8"))
        except Exception as e:
            findings.append({"file": str(py), "type": "parse_error", "detail": str(e)})
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.name.split(".")[0]
                    if name in FORBIDDEN_IMPORTS:
                        findings.append({"file": str(py), "type": "forbidden_import", "detail": alias.name})
            if isinstance(node, ast.ImportFrom):
                name = (node.module or "").split(".")[0]
                if name in FORBIDDEN_IMPORTS:
                    findings.append({"file": str(py), "type": "forbidden_import", "detail": node.module})
            if isinstance(node, ast.Call):
                func = node.func
                fname = ""
                if isinstance(func, ast.Name):
                    fname = func.id
                elif isinstance(func, ast.Attribute):
                    fname = func.attr
                if fname in FORBIDDEN_CALLS:
                    findings.append({"file": str(py), "type": "forbidden_call", "detail": fname})
    return {
        "pass": not findings,
        "finding_count": len(findings),
        "findings": findings,
        "policy": "No network imports, subprocess, dynamic execution, hidden telemetry, host mutation, or real-world actuation helpers in the offline core."
    }
