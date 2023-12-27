import gc
import sys
import fitz
import uuid

if fitz.VersionBind.split(".") < ["1", "17", "0"]:
    sys.exit("PyMuPDF v1.17.0+ is needed.")

gc.set_debug(gc.DEBUG_UNCOLLECTABLE)

red = (1, 0, 0)
blue = (0, 0, 1)
gold = (1, 1, 0)
green = (0, 1, 0)


def print_descr(annot, text):
    annot.parent.insert_text(
        annot.rect.br + (10, -5), text, color=red
    )

class PdfProcessor:
    def __init__(self, file):
        self.doc = fitz.open(file)

    def scrap_text(self):

        full_text = ""
        i = 1
        for page_num in range(self.doc.page_count):
            page = self.doc[page_num]
            text = page.get_text()
            full_text += f"\nPage {i}\n" + text
            i = i + 1

        return full_text
    
    def generate_highlights(self, highlights):
        for h in highlights:
            if len(self.doc) <= h['page_num'] - 1:
                continue
            page = self.doc[h['page_num'] - 1]
            rl = page.search_for(h['text'], quads=True)
            if len(rl) <= h['occurrence'] - 1:
                continue
            annot = page.add_highlight_annot(rl[h['occurrence'] - 1])
            print_descr(annot, h['highlight'])

        unique_id = str(uuid.uuid4())
        self.doc.save('tmp/' + unique_id + '.pdf')
        return unique_id



        