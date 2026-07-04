"""
Download archived images from the Wayback Machine for Dutray Yorkies.
Uses the 'id_' prefix to get raw files instead of the Wayback Machine viewer page.
Saves to images/uploads/ organized by category.
"""
import os
import urllib.request
import time
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(BASE_DIR, "images", "uploads")

# Create subdirectories
for subdir in ["hero", "dams", "sires", "testimonials", "puppies", "logo"]:
    os.makedirs(os.path.join(IMG_DIR, subdir), exist_ok=True)


def wayback_raw_url(wayback_url):
    """
    Convert a regular Wayback Machine URL to its raw/identity version.
    e.g., https://web.archive.org/web/20180107173016/http://example.com/img.jpg
    becomes https://web.archive.org/web/20180107173016id_/http://example.com/img.jpg
    """
    return re.sub(
        r'(web\.archive\.org/web/\d+)',
        r'\1id_',
        wayback_url
    )


# Image URLs from Wayback Machine CDX index
# Format: (wayback_url, local_filename, category)
IMAGES = [
    # Logo
    ("https://web.archive.org/web/20180107173016/http://dutrayyorkies.com/wp-content/uploads/2016/05/lgo2.png",
     "logo/logo.png", "logo"),

    # Homepage hero/slider
    ("https://web.archive.org/web/20250308091206/https://dutrayyorkies.com/wp-content/uploads/2016/05/frontpageslider-1024x629.jpg",
     "hero/frontpage-slider.jpg", "hero"),

    # About page - Tracy's dog
    ("https://web.archive.org/web/20180107192315/http://dutrayyorkies.com/wp-content/uploads/2015/04/39002_1432596706402_179896_n.jpg",
     "hero/about-photo.jpg", "about"),

    # Dams
    ("https://web.archive.org/web/20190521192828/http://dutrayyorkies.com/wp-content/uploads/2015/04/971444_10200508625069616_1272491016_n.jpg",
     "dams/dam-1.jpg", "dams"),
    ("https://web.archive.org/web/20181027074023/http://dutrayyorkies.com/wp-content/uploads/2016/05/13006622_10207899212069672_4851672745940670185_n-200x200.jpg",
     "dams/dam-2.jpg", "dams"),
    ("https://web.archive.org/web/20181027084626/http://dutrayyorkies.com/wp-content/uploads/2016/05/13219610_10208058273286103_185353708_n-150x150.jpg",
     "dams/dam-3.jpg", "dams"),
    ("https://web.archive.org/web/20181027092603/http://dutrayyorkies.com/wp-content/uploads/2016/05/14344899_10209025101976216_5040748077228936065_n-200x200.jpg",
     "dams/dam-4.jpg", "dams"),
    ("https://web.archive.org/web/20181027050343/http://dutrayyorkies.com/wp-content/uploads/2016/05/18034926_10210987776681857_38756297_n-200x200.jpg",
     "dams/dam-5.jpg", "dams"),

    # Sires - Gizmo
    ("https://web.archive.org/web/20181027030920/http://dutrayyorkies.com/wp-content/uploads/2017/09/Gizmo-Sep-1-150x150.jpg",
     "sires/gizmo-1.jpg", "sires"),
    ("https://web.archive.org/web/20181027064458/http://dutrayyorkies.com/wp-content/uploads/2018/03/gizmo-2017-150x150.jpg",
     "sires/gizmo-2.jpg", "sires"),
    # Sires - Levi
    ("https://web.archive.org/web/20181027111350/http://dutrayyorkies.com/wp-content/uploads/2018/04/levi--150x150.jpg",
     "sires/levi.jpg", "sires"),

    # Testimonials photos
    ("https://web.archive.org/web/20181027032650/http://dutrayyorkies.com/wp-content/uploads/2015/04/13220519_10208068136332673_3642538009885554134_o-1024x684.jpg",
     "testimonials/family-1.jpg", "testimonials"),
    ("https://web.archive.org/web/20181027042931/http://dutrayyorkies.com/wp-content/uploads/2016/05/juddar-and-donna-150x150.jpg",
     "testimonials/juddar-donna.jpg", "testimonials"),
    ("https://web.archive.org/web/20181027050758/http://dutrayyorkies.com/wp-content/uploads/2017/04/connie-and-richie-150x150.jpg",
     "testimonials/connie-richie.jpg", "testimonials"),
    ("https://web.archive.org/web/20181027061236/http://dutrayyorkies.com/wp-content/uploads/2018/04/barbra-and-Harley-150x150.jpg",
     "testimonials/barbra-harley.jpg", "testimonials"),

    # Puppies / Litters
    ("https://web.archive.org/web/20181027075303/http://dutrayyorkies.com/wp-content/uploads/2016/05/kate-litter-1-200x200.jpg",
     "puppies/kate-litter.jpg", "puppies"),
    ("https://web.archive.org/web/20181027114902/http://dutrayyorkies.com/wp-content/uploads/2016/05/levi-litter-picture-200x200.jpg",
     "puppies/levi-litter.jpg", "puppies"),
    ("https://web.archive.org/web/20181027104554/http://dutrayyorkies.com/wp-content/uploads/2016/05/lola-litter-200x200.jpg",
     "puppies/lola-litter.jpg", "puppies"),
    ("https://web.archive.org/web/20181027075913/http://dutrayyorkies.com/wp-content/uploads/2016/05/lucy-litter1-200x200.jpg",
     "puppies/lucy-litter.jpg", "puppies"),
    ("https://web.archive.org/web/20181027025851/http://dutrayyorkies.com/wp-content/uploads/2018/04/gizmo-littler-200x200.jpg",
     "puppies/gizmo-litter.jpg", "puppies"),
    ("https://web.archive.org/web/20181027093306/http://dutrayyorkies.com/wp-content/uploads/2018/07/hercules-boy-200x200.jpg",
     "puppies/hercules-boy.jpg", "puppies"),
    ("https://web.archive.org/web/20181027054058/http://dutrayyorkies.com/wp-content/uploads/2018/07/hercules-girl--200x200.jpg",
     "puppies/hercules-girl.jpg", "puppies"),
    ("https://web.archive.org/web/20181027102624/http://dutrayyorkies.com/wp-content/uploads/2016/05/kate-christmas-pic-200x200.jpg",
     "puppies/kate-christmas.jpg", "puppies"),

    # DSC photos (puppies/general)
    ("https://web.archive.org/web/20181027103458/http://dutrayyorkies.com/wp-content/uploads/2016/05/DSC01368-150x150.jpg",
     "puppies/dsc01368.jpg", "puppies"),
    ("https://web.archive.org/web/20181027070753/http://dutrayyorkies.com/wp-content/uploads/2016/05/DSC03123-150x150.jpg",
     "puppies/dsc03123.jpg", "puppies"),
    ("https://web.archive.org/web/20181027072739/http://dutrayyorkies.com/wp-content/uploads/2016/05/DSC03192-150x150.jpg",
     "puppies/dsc03192.jpg", "puppies"),
    ("https://web.archive.org/web/20181027075610/http://dutrayyorkies.com/wp-content/uploads/2016/05/DSC03193-150x150.jpg",
     "puppies/dsc03193.jpg", "puppies"),
    ("https://web.archive.org/web/20181027112156/http://dutrayyorkies.com/wp-content/uploads/2016/05/DSC03194-150x150.jpg",
     "puppies/dsc03194.jpg", "puppies"),
    ("https://web.archive.org/web/20181027114026/http://dutrayyorkies.com/wp-content/uploads/2016/05/DSC03195-150x150.jpg",
     "puppies/dsc03195.jpg", "puppies"),
    ("https://web.archive.org/web/20181027085134/http://dutrayyorkies.com/wp-content/uploads/2016/05/DSC03216-150x150.jpg",
     "puppies/dsc03216.jpg", "puppies"),
    ("https://web.archive.org/web/20181027092642/http://dutrayyorkies.com/wp-content/uploads/2016/05/DSC03220-150x150.jpg",
     "puppies/dsc03220.jpg", "puppies"),
    ("https://web.archive.org/web/20181027072826/http://dutrayyorkies.com/wp-content/uploads/2016/05/DSC03223-150x150.jpg",
     "puppies/dsc03223.jpg", "puppies"),
    ("https://web.archive.org/web/20190212173821/http://dutrayyorkies.com/wp-content/uploads/2016/08/DSC01899-300x200.jpg",
     "puppies/dsc01899.jpg", "puppies"),
    ("https://web.archive.org/web/20181027091406/http://dutrayyorkies.com/wp-content/uploads/2016/08/DSC01964-150x150.jpg",
     "puppies/dsc01964.jpg", "puppies"),
]


def download_image(url, filename):
    """Download a single image from Wayback Machine using raw/id_ URL."""
    filepath = os.path.join(IMG_DIR, filename)

    # Delete existing file (it's probably an HTML page from the previous bad download)
    if os.path.exists(filepath):
        os.remove(filepath)

    raw_url = wayback_raw_url(url)

    try:
        req = urllib.request.Request(raw_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()

            # Verify it's actually an image (not HTML)
            if data[:15].lower().startswith(b'<!doctype') or data[:6].lower().startswith(b'<html'):
                print(f"  FAIL (got HTML): {filename}")
                return False

            with open(filepath, 'wb') as f:
                f.write(data)
            print(f"  OK ({len(data):,} bytes): {filename}")
            return True
    except Exception as e:
        print(f"  FAIL: {filename} - {e}")
        return False


def main():
    print(f"Downloading {len(IMAGES)} images (using raw/id_ URLs) to: {IMG_DIR}")
    print("=" * 60)

    success = 0
    failed = 0

    for url, filename, category in IMAGES:
        print(f"\n[{category}] {filename}")
        if download_image(url, filename):
            success += 1
        else:
            failed += 1
        # Be polite to Wayback Machine
        time.sleep(1)

    print("\n" + "=" * 60)
    print(f"Done! {success} downloaded, {failed} failed.")


if __name__ == "__main__":
    main()
