import json
import html
from pathlib import Path

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
def bookmarks_json_to_html(bookmarks: dict) -> str:
    
    def get_bookmarks_chunk(node, level=0):
        if node['type'] == "folder":
            start = f"{level * '\t'}<DT><H3>{html.escape(node['name'])}</H3>\n{level * '\t'}<DL><p>"
            if node['children'] and len(node['children']) > 0:
                middle = "\n".join([get_bookmarks_chunk(child, level+1) for child in node['children']])
            else:
                middle = ""
            end=f"{level * '\t'}</DL><p>"
            return "\n".join([start, middle, end])
        else:
            return f"{level * '\t'}<DT><A HREF=\"{node['url']}\" >{html.escape(node['name'])}</A>"

    chunk = get_bookmarks_chunk(bookmarks['roots']['bookmark_bar'])
    return "\n".join([header, chunk, footer])

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("not enough args")
        sys.exit(1)

    filename = Path(sys.argv[1])
    with open(filename, 'r', encoding='utf-8') as f:
        bookmarks = json.load(f)

    html_str = bookmarks_json_to_html(bookmarks)
    html_encoded = html_str.encode('utf-8', errors='replace')
    html_decoded = html_encoded.decode('utf-8')
    sys.stdout.reconfigure(encoding="utf-8")
    print(html_decoded)