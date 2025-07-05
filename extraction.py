import pymupdf
import re
from fastapi import HTTPException, status

def extract_text_from_pdf(filepath: str, mode: str, value: str="", chapter: str | None = None, pages: str | None = None):
    doc = pymupdf.open(filepath)
    with open("output.txt", "wb") as out:
        if mode == "full":
            for page in doc:
                text = page.get_text().encode("utf-8")
                out.write(text)
                out.write(bytes((12,)))

        elif mode == "pages":
                try:
                    page_numbers = [int(p.strip()) for p in pages.split(",")] 
                except ValueError:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid page numbers format")
                
                for page in page_numbers:
                    try:
                        page = doc[page]
                        text = page.get_text().encode("utf-8")
                        out.write(text)
                    except IndexError:
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Page {page} not found in the document") 

        elif mode == "chapter":
            pattern = r"(?i)\bchapter\b[\s:]*\d+"
            try:
                start_page = int((value))
            except ValueError:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid start page format")
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
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chapter not found")

        else:
            return "Invalid mode."
    
    with open("output.txt", "r", encoding="utf-8") as result:
        return result.read()
