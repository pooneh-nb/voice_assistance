import re
import bs4
import email
import csv
from pathlib import Path


def extract_page(html_string):
    soup = bs4.BeautifulSoup(html_string, "lxml")
    for elem in soup.select("div.s-main-slot>div.s-result-item>div>span>div>div.a-section"):
        h2_elem = elem.select_one("h2")
        a_elem = h2_elem.select_one("a")
        skill_name = h2_elem.text.strip()

        m = re.match(r"^https://www.amazon.com/(?:[^/]+/)?dp/([0-9A-Z]+)/", a_elem["href"])
        skill_id = m.group(1)

        try:
            review_row, info_row = h2_elem.parent.next_siblings
        except ValueError:
            review_row = None
            info_row, = h2_elem.parent.next_siblings

        info = dict(id=skill_id, name=skill_name, url=f"https://www.amazon.com/dp/{skill_id}")

        if review_row is None:
            info["rating"] = -1
            info["n_ratings"] = 0
        else:
            span1, span2 = next(review_row.children).children
            info["rating"] = float(span1["aria-label"].split(maxsplit=1)[0])
            info["n_ratings"] = int(span2["aria-label"].replace(",", ""))

        left_col, right_col = info_row.children

        # left column
        try:
            fee_block, _ = next(left_col.children).children
        except ValueError:
            info["fee"] = -1
        else:
            if fee_block.text.strip() == "Free Download":
                info["fee"] = 0.00
            else:
                info["fee"] = float(re.match(r"^\$(\d+\.\d{2})\$", fee_block.text).group(1))

        # right column
        right_col = right_col.select_one("div.a-row.a-size-small.a-color-base")
        if right_col is None:
            info["language"] = "N/A"
            info["description"] = "N/A"
        else:
            for child in right_col.children:
                if isinstance(child, bs4.NavigableString):
                    continue
                elif child.name == "a":
                    info["language"] = child.text.strip()
                elif child.name == "span" and child.get("class") == ["a-color-secondary"]:
                    info["description"] = child.text.strip()

        yield info


def main():
    seen_ids = set()

    with open("index.csv", "w", newline="") as fout:
        writer = csv.DictWriter(fout, fieldnames=["id", "name", "url", "rating",
                                                  "n_ratings", "fee", "language", "description"])
        writer.writeheader()

        for subdir in Path("index").iterdir():
            for mhtml_file in subdir.rglob("*.mhtml"):
                print(mhtml_file)
                with open(mhtml_file, "rb") as fin:
                    email_data = email.message_from_binary_file(fin)

                main_part = None
                for p in email_data.walk():
                    if p.get("Content-Location") == email_data["Snapshot-Content-Location"]:
                        main_part = p.get_payload(decode=True).decode()

                for info in extract_page(main_part):
                    if info["id"] not in seen_ids:
                        seen_ids.add(info["id"])
                        writer.writerow(info)


if __name__ == "__main__":
    main()
