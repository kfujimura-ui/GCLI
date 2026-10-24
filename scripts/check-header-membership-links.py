#!/usr/bin/env python3
"""Check that every public page header Membership link resolves to /membership/."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse


class HeaderMembershipParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.header_depth = 0
        self.anchor = None
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "header":
            self.header_depth += 1
        if tag == "a" and self.header_depth:
            self.anchor = {
                "href": attrs.get("href", ""),
                "class": attrs.get("class", ""),
                "text": [],
            }

    def handle_data(self, data):
        if self.anchor is not None:
            self.anchor["text"].append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self.anchor is not None:
            text = " ".join("".join(self.anchor["text"]).split())
            classes = set(self.anchor["class"].split())
            if "membership-link" in classes or text == "Membership":
                self.links.append({
                    "href": self.anchor["href"],
                    "text": text,
                })
            self.anchor = None
        if tag == "header" and self.header_depth:
            self.header_depth -= 1


def page_url(path: Path, root: Path) -> str:
    relative = path.relative_to(root)
    # The prototype source is copied to the public site root as index.html.
    if relative.as_posix() == "GCLI_OnlineFirst_Design_Prototype.html":
        path_part = "/"
    else:
        relative = relative.with_suffix("")
        if relative.name == "index":
            relative = relative.parent
        path_part = "/" + (str(relative).strip("/") + "/" if str(relative) else "")
    return "https://gcli.site" + path_part


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    pages = sorted(
        path for path in root.rglob("*.html")
        if ".git" not in path.parts and "node_modules" not in path.parts
    )
    failures = []
    checked = []
    excluded = []

    for page in pages:
        parser = HeaderMembershipParser()
        parser.feed(page.read_text(encoding="utf-8"))
        if not parser.links:
            excluded.append(str(page.relative_to(root)))
            continue
        base = page_url(page, root)
        for link in parser.links:
            resolved = urljoin(base, link["href"])
            parsed = urlparse(resolved)
            checked.append((str(page.relative_to(root)), link["href"], resolved))
            if parsed.scheme != "https" or parsed.netloc != "gcli.site" or parsed.path != "/membership/" or parsed.query or parsed.fragment:
                failures.append((str(page.relative_to(root)), link["href"], resolved))

    print(f"Public HTML pages enumerated: {len(pages)}")
    print(f"Header Membership links checked: {len(checked)}")
    for page, href, resolved in checked:
        print(f"PASS {page}: {href} -> {resolved}")
    print(f"Pages without a main header Membership link (intentionally excluded): {len(excluded)}")
    for page in excluded:
        print(f"EXCLUDE {page}")
    if failures:
        print("FAIL: non-canonical header Membership links:")
        for page, href, resolved in failures:
            print(f"  {page}: {href} -> {resolved}")
        return 1
    print("PASS: every main header Membership link resolves to https://gcli.site/membership/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
