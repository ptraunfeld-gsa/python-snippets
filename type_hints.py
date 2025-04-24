
# Run:
# python -m mypy type_hints.py 

def fetch_issues_with_hints(url: str, headers: dict[str, str]) -> list[dict]:
    return ""

def fetch_issues_no_hints(url, headers):
    return ""


result1 = fetch_issues_with_hints("url", "headers")
result2 = fetch_issues_no_hints("url", {})