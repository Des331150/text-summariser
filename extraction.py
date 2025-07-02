import pymupdf
import re

def extract_text_from_pdf(filepath: str, mode: str, value: str=""):
    doc = pymupdf.open(filepath)
    with open("output.txt", "wb") as out:
        if mode == "full":
            for page in doc:
                text = page.get_text().encode("utf-8")
                out.write(text)
                out.write(bytes((12,)))

        elif mode == "page":
            try:
                try:
                    page = doc[int(value)]
                except ValueError:
                    return "Page should be an integer."
                text = page.get_text().encode("utf-8")
                out.write(text)
            except IndexError:
                return "Page number doesn't exist."

        elif mode == "chapter":
            pattern = r"(?i)\bchapter\b[\s:]*\d+"
            try:
                start_page = int(value)
            except ValueError:
                return "Chapter should be an integer."
            in_chapter = False

            for i in range(start_page, len(doc)):
                page = doc[i]
                text = page.get_text()

                if re.search(pattern, text):
                    if not in_chapter:
                        in_chapter = True
                    else:
                        break

                if in_chapter:
                    out.write(text.encode("utf-8"))

            if not in_chapter:
                return "No chapter found"

        else:
            return "Invalid mode."