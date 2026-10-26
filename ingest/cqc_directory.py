import re
from datetime import datetime
from pathlib import Path

import requests

PAGE_URL = "https://www.cqc.org.uk/about-us/transparency/using-cqc-data"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}
CSV_HREF = re.compile(r'href="(https://www\.cqc\.org\.uk/system/files/[^"]+CQC_directory\.csv)"', re.I)
PRODUCED = re.compile(r"This data was produced on\s+(.+)", re.I)


def land_directory() -> Path:
    session = requests.Session()
    session.headers.update(HEADERS)

    page = session.get(PAGE_URL, timeout=60)
    page.raise_for_status()
    match = CSV_HREF.search(page.text)
    if not match:
        raise RuntimeError(f"No CQC_directory.csv link on {PAGE_URL}")
    source_url = match.group(1)

    response = session.get(source_url, timeout=120)
    response.raise_for_status()
    raw = response.content

    text = raw.decode("utf-8-sig", errors="replace")
    produced = PRODUCED.search("\n".join(text.splitlines()[:6]))
    if not produced:
        raise RuntimeError("Could not read 'produced on' date from the CSV")
    extract_date = datetime.strptime(produced.group(1).strip().strip(","), "%d %B %Y").date().isoformat()

    out_dir = Path("data/bronze/cqc_directory") / f"extract_date={extract_date}"
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "CQC_directory.csv"
    dest.write_bytes(raw)
    return dest


if __name__ == "__main__":
    path = land_directory()
    print(path, path.stat().st_size)
