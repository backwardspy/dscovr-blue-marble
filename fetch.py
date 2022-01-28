"""
Uses the NASA EPIC API to download the latest earth image.
"""
import json
import shutil
from datetime import datetime
from pathlib import Path
from urllib import request


def get_latest_archive_url(data: dict) -> str:
    """
    Use the given metadata to find the archive URL of the latest image.
    """
    metadata = data[-1]
    img = metadata["image"]
    date = datetime.strptime(metadata["date"], "%Y-%m-%d %H:%M:%S")
    archive_path = f"{date.year:04}/{date.month:02}/{date.day:02}/png/{img}.png"
    archive_url = f"https://epic.gsfc.nasa.gov/archive/natural/{archive_path}"
    return archive_url


def download_image(url: str) -> None:
    """
    Download the image at the given URL into ./earth.png
    """
    path = Path("./earth.png")
    with request.urlopen(url) as resp, path.open("wb") as image_file:
        shutil.copyfileobj(resp, image_file)


def main() -> None:
    """
    Request metadata from the NASA EPIC API and download the latest image.
    """
    with request.urlopen("https://epic.gsfc.nasa.gov/api/natural") as resp:
        data = json.load(resp)
        archive_url = get_latest_archive_url(data)
        download_image(archive_url)


if __name__ == "__main__":
    main()
