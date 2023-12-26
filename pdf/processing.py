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


# def print_descr(annot):
#     """Print a short description to the right of each annot rect."""
#     annot.parent.insert_text(
#         annot.rect.br + (10, -5), "%s annotation" % annot.type[1], color=red
#     )


# doc = fitz.open('./samples/samplecv.pdf')

# for page in doc:

#     rl = page.search_for(highlight, quads=True)  # need a quad b/o tilted text
#     annot = page.add_highlight_annot(rl[0])
#     print_descr(annot)


# doc.save(__file__.replace(".py", "-%i.pdf" % page.rotation), deflate=True)


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
            if len(self.doc) <= h['page_num']:
                continue
            page = self.doc[h['page_num']]
            rl = page.search_for(h['text'], quads=True)
            if len(rl) <= h['occurence'] - 1:
                continue
            page.add_highlight_annot(rl[h['occurence'] - 1])

        unique_id = str(uuid.uuid4())
        self.doc.save('tmp/' + unique_id + '.pdf')
        return unique_id



        