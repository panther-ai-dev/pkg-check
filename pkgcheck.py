"""Check every package in a requirements.txt against PyPI before you install it.

usage: python pkgcheck.py [requirements.txt]

For each package it asks PyPI: does it exist, when was it first released, how many
releases does it have, and does it link to its source code? Anything missing or
suspicious gets a warning. Exit code 1 if any package does not exist.
"""
import json, re, sys, urllib.error, urllib.request
from datetime import datetime, timezone

NEW_DAYS = 90          # first release newer than this = warning
FEW_RELEASES = 2       # this many releases or fewer = warning
SOURCE_HOSTS = ("github.com", "gitlab.com", "bitbucket.org", "codeberg.org")


def read_requirements(path):
    names = []
    for line in open(path, encoding="utf-8"):
        line = line.split("#", 1)[0].strip()
        if not line or line.startswith("-"):
            continue
        name = re.split(r"[\s<>=!~;\[@]", line, 1)[0]
        if name:
            names.append(name)
    return names


def pypi(name):
    url = f"https://pypi.org/pypi/{name}/json"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def check(name):
    data = pypi(name)
    if data is None:
        return "XX", ["does NOT exist on PyPI. Do not install."]
    info, releases = data["info"], data["releases"]
    uploads = [f["upload_time_iso_8601"] for files in releases.values() for f in files]
    warnings = []
    if uploads:
        first = min(datetime.fromisoformat(u.replace("Z", "+00:00")) for u in uploads)
        age = (datetime.now(timezone.utc) - first).days
        if age < NEW_DAYS:
            warnings.append(f"brand new: first release {age} days ago")
    else:
        warnings.append("name is registered but has no files")
    n = len([v for v, files in releases.items() if files])
    if uploads and n <= FEW_RELEASES:
        warnings.append(f"only {n} release(s)")
    urls = " ".join(filter(None, [info.get("home_page") or ""] + list((info.get("project_urls") or {}).values())))
    if not any(h in urls for h in SOURCE_HOSTS):
        warnings.append("no source code link")
    return ("!!" if warnings else "OK"), warnings


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "requirements.txt"
    names = read_requirements(path)
    missing = 0
    for name in names:
        mark, notes = check(name)
        missing += mark == "XX"
        print(f"[{mark}] {name}" + (": " + "; ".join(notes) if notes else ""))
    print(f"\n{len(names)} checked, {missing} not found.")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
