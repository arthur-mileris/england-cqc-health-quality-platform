from pathlib import Path
import requests

DIRECTORY_URL = "https://www.cqc.org.uk/system/files/2026-09/30_september_2026_CQC_directory.csv"
EXTRACT_DATE = "2026-09-30"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

def land_directory() -> Path:
    out_dir = Path("data/bronze/cqc_directory") / f"extract_date={EXTRACT_DATE}"
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "CQC_directory.csv"
    response = requests.get(DIRECTORY_URL, headers=HEADERS, timeout=120)
    response.raise_for_status()
    dest.write_bytes(response.content)
    return dest

if __name__ == "__main__":
    path = land_directory()
    print(path, path.stat().st_size)
