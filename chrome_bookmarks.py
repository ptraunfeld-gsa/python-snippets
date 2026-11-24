import json
import html
from pathlib import Path
from urllib.parse import urlsplit
import sys

header = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
    It will be read and overwritten.
    DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
"""

footer = """
</DL><p>
"""

ALLOWED_SCHEMES = {"http", "https", "file", "chrome"}

def log_error(message: str):
    print(f"ERROR: {message}", file=sys.stderr)

def log_warning(message: str):
    print(f"WARNING: {message}", file=sys.stderr)

def safe_text(value) -> str:
    if not isinstance(value, str):
        value = ""
    return html.escape(value, quote=True)


def safe_href(value: str, allowed_schemes = ALLOWED_SCHEMES) -> str:
    if not isinstance(value, str):
        raise ValueError(f"Invalid non-string URL: {value}")

    value = value.strip()

    if any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        raise ValueError(f"Invalid control character in URL: {value}")

    try:
        parsed = urlsplit(value)
    except Exception:
        raise ValueError(f"Invalid URL: {value}")
        

    if parsed.scheme.lower() not in allowed_schemes:
        raise ValueError(f"Invalid scheme: {value}")

    return html.escape(value, quote=True)


def bookmarks_json_to_html(bookmarks: dict) -> str:
    
    def get_bookmarks_chunk(node, level=0):
        if node['type'] == "folder":
            start = f"{level * '\t'}<DT><H3>{safe_text(node['name'])}</H3>\n{level * '\t'}<DL><p>"
            if node['children'] and len(node['children']) > 0:
                middle = "\n".join([get_bookmarks_chunk(child, level+1) for child in node['children']])
            else:
                middle = ""
            end=f"{level * '\t'}</DL><p>"
            return "\n".join([start, middle, end])
        else:
            try:
                return f"{level * '\t'}<DT><A HREF=\"{safe_href(node['url'])}\" >{safe_text(node['name'])}</A>"
            except ValueError as e:
                log_warning(f"Bookmark '{node['name']}': {e}")
                return ""

    chunk = get_bookmarks_chunk(bookmarks['roots']['bookmark_bar'])
    return "\n".join([header, chunk, footer])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        log_error("not enough args")
        sys.exit(1)
    
    filename = Path(sys.argv[1])
    with open(filename, 'r', encoding='utf-8') as f:
        bookmarks = json.load(f)

    html_str = bookmarks_json_to_html(bookmarks)
    html_encoded = html_str.encode('utf-8', errors='replace')
    html_decoded = html_encoded.decode('utf-8')
    sys.stdout.reconfigure(encoding="utf-8")
    print(html_decoded)