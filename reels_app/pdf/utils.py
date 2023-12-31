import os
import re

from PyPDF2 import PdfReader, PdfWriter


def rename_deluxe_invoices(directory):
    """Batch rename Deluxe invoices.

    The function searches the PDF for the invoice number and film title, then
    creates a new PDF with the following naming scheme:

    Deluxe Inv {invoice-number} {film-title}.pdf
    """
    for invoice in os.listdir(directory):
        new_path = os.path.join(directory, invoice)

        pdf = PdfReader(new_path)
        pdf_text = pdf.pages[0].extract_text()

        # get invoice number and strip new lines
        invoice_number = re.search(
            '(?<=Invoice Date:)(.*)(?=Customer Account No:)(?s)',
            pdf_text).group(0).strip()

        # replace any illegal characters in the film title with a space
        # otherwise function will error due to filename issues
        film_title = re.search(
            '(?<=Title: )(.*)', pdf_text).group(0).strip().upper()
        film_title_sanitized = re.sub(
            '\"|\:|\/|\\|\<|\>|\||\?|\*|\n', ' ', film_title)

        pdf_writer = PdfWriter()
        pdf_writer.add_page(pdf.pages[0])

        # write to a new PDF
        with open((f'downloads/Deluxe Inv {invoice_number} '
                  f'{film_title_sanitized}.pdf'),
                  mode='wb') as output_pdf:
            pdf_writer.write(output_pdf)


def split_box_office_report(directory):
    """Split the Distributor by Film and Type report into separate PDFs."""
    item = os.listdir(directory)[0]  # get the PDF filename

    # join the directory & PDF file name
    new_path = os.path.join(directory, item)

    pdf = PdfReader(new_path)

    for page, unused in enumerate(pdf.pages):

        pdf_text = pdf.pages[page].extract_text()

        # search for the film title, located between the strings Film: and
        # DayTicket; some pages push DayTicket to a new line so the (?s) inline
        # flag ensures that those get captured as well
        film_title = re.search('(?<=Film: )(.*)(?=Day)(?s)', pdf_text)

        if film_title is None:
            # provides a default in case the regex returns None
            new_film_title = f'box-office-page-{page}'
        else:
            # replace any illegal characters with a space otherwise function
            # will error due to filename issues
            new_film_title = re.sub(
                '\"|\:|\/|\\|\<|\>|\||\?|\*|\n', ' ', film_title.group(1))

        # prepare the class that will write to a new PDF
        pdf_writer = PdfWriter()
        pdf_writer.add_page(pdf.pages[page])

        # write to a new PDF
        with open(f'downloads/{new_film_title}-{page}.pdf', mode='wb') as output_pdf:
            pdf_writer.write(output_pdf)
