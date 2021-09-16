import os
import re

from PyPDF2 import PdfFileReader, PdfFileWriter


def split(directory):
    item = os.listdir(directory)[0]  # get the PDF filename

    # join the directory & PDF file name
    new_path = os.path.join(directory, item)

    pdf = PdfFileReader(new_path)

    for page in range(pdf.getNumPages()):

        # search for the film title
        pdf_text = pdf.getPage(page).extractText()
        # search for the film title, located between the strings Film: and
        # DayTicket; some pages push DayTicket to a new line so the (?s) inline
        # flag ensures that those get captured as well
        film_title = re.search('(?<=Film: )(.*)(?=DayTicket)(?s)', pdf_text)
        if film_title is None:
            # provides a default in case the regex returns None
            name_of_split = f'box-office-page-{page}'
        else:
            # remove quotation mark if used, such as in NTL
            # remove \n characters if found
            name_of_split = film_title.group(
                1).replace('"', '').replace('\n', '')

        # prepare the class that will write to a new PDF
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))

        # write to a new PDF
        with open(f'pdfs/{name_of_split}-{page}.pdf', mode='wb') as output_pdf:
            pdf_writer.write(output_pdf)
