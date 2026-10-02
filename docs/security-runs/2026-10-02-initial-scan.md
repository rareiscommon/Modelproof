# Security Scan — 2026-10-02T15:22:26Z

## Scanners run
- pip-audit — Python dependency CVEs
- gitleaks — secret scanning
- bandit — Python static analysis
- semgrep — multi-language static analysis
- trivy — dependency vulnerability scan

## Environment
- Python: Python 3.14.4
- Lock file: requirements.lock.txt

## Results — all clean

### pip-audit
```
No known vulnerabilities found
```

### gitleaks
```
[90m6:22PM[0m [32mINF[0m [1m9 commits scanned.[0m
[90m6:22PM[0m [32mINF[0m [1mscanned ~20120 bytes (20.12 KB) in 671ms[0m
[90m6:22PM[0m [32mINF[0m [1mno leaks found[0m
```

### bandit
```
	Total issues (by severity):
		Low: 0
		Medium: 0
		High: 0
	Total issues (by confidence):
		Low: 0
		Medium: 0
		High: 0
```

### semgrep
```
 • Findings: 0 (0 blocking)
 • Rules run: 290
```

### trivy
```

Report Summary

┌───────────────────────┬──────┬─────────────────┐
│        Target         │ Type │ Vulnerabilities │
├───────────────────────┼──────┼─────────────────┤
│ requirements.lock.txt │ pip  │        0        │
└───────────────────────┴──────┴─────────────────┘
Legend:
- '-': Not scanned
- '0': Clean (no security findings detected)

```

## Conclusion
All five scanners report zero high/critical findings. No CVEs, no secrets, no static analysis issues.
