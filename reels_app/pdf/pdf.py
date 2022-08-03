import os
import re

from PyPDF2 import PdfReader, PdfWriter


def split(directory):
    item = os.listdir(directory)[0]  # get the PDF filename

    # join the directory & PDF file name
    new_path = os.path.join(directory, item)

    pdf = PdfReader(new_path)

    for page in range(pdf.getNumPages()):

        # search for the film title
        pdf_text = pdf.getPage(page).extract_text()
        # search for the film title, located between the strings Film: and
        # DayTicket; some pages push DayTicket to a new line so the (?s) inline
        # flag ensures that those get captured as well
        film_title = re.search('(?<=Film: )(.*)(?=Day)(?s)', pdf_text)

        if film_title is None:
            # provides a default in case the regex returns None
            name_of_split = f'box-office-page-{page}'
        else:
            # remove quotation mark if used, such as in NTL
            # remove \n characters if found
            name_of_split = film_title.group(
                1).replace('"', '').replace('\n', '')

        # prepare the class that will write to a new PDF
        pdf_writer = PdfWriter()
        pdf_writer.addPage(pdf.getPage(page))

        # write to a new PDF
        with open(f'pdfs/{name_of_split}-{page}.pdf', mode='wb') as output_pdf:
            pdf_writer.write(output_pdf)


def rename_deluxe(directory):

    for invoice in os.listdir(directory):
        new_path = os.path.join(directory, invoice)

        pdf = PdfReader(new_path)
        pdf_text = pdf.getPage(0).extract_text()

        # get invoice number and strip new lines
        invoice_number = re.search(
            '(?<=Invoice Date:)(.*)(?=Customer Account No:)(?s)', pdf_text).group(0).strip()

        # get film title and strip new lines
        film_title = re.search(
            '(?<=Title: )(.*)(?=\n 1 4000000119)', pdf_text).group(0).strip()

        pdf_writer = PdfWriter()
        pdf_writer.addPage(pdf.getPage(0))

        # write to a new PDF
        with open(f'pdfs/Deluxe Inv {invoice_number} {film_title}.pdf', mode='wb') as output_pdf:
            pdf_writer.write(output_pdf)
