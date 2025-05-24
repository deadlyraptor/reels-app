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
        invoice_number = (
            re.search("(?s)(?<=Invoice Date:)(.*)(?=Customer Account No:)", pdf_text)
            .group(0)
            .strip()
        )

        # replace any illegal characters in the film title with a space
        # otherwise function will error due to filename issues
        film_title = re.search("(?<=Title: )(.*)", pdf_text).group(0).strip().upper()
        film_title_sanitized = re.sub('"|\:|\/|\\|\<|\>|\||\?|\*|\n', " ", film_title)

        pdf_writer = PdfWriter()
        pdf_writer.add_page(pdf.pages[0])

        # write to a new PDF
        with open(
            (f"downloads/Deluxe Inv {invoice_number} {film_title_sanitized}.pdf"),
            mode="wb",
        ) as output_pdf:
            pdf_writer.write(output_pdf)


def split_box_office_report(directory):
    """Split the Distributor by Film and Type report into separate PDFs."""
    item = os.listdir(directory)[0]  # get the PDF filename

    # join the directory & PDF file name
    new_path = os.path.join(directory, item)

    pdf = PdfReader(new_path)

    for page, unused in enumerate(pdf.pages):
        pdf_text = pdf.pages[page].extract_text()
        # print(pdf_text)

        # search for the film title, located between the strings Film: and
        # DayTicket; some pages push DayTicket to a new line so the (?s) inline
        # flag ensures that those get captured as well
        film = re.search("(?s)(?<=Film: )(.*)(?=Day)", pdf_text)

        # search for the distributor, located between the strings 'Distributor:'
        # and 'Film.' There are six spaces between the distributor string and
        # the 'Film' string.
        distributor = re.search("(?<=Distributor: )(.*)(?=      Film)", pdf_text)

        # some pages in the report do not have the distributor field so when
        # that page is reached, we set distributor to a default value of
        # 'DISTRIB' to ensure that the PDF can be written without error.
        # on Macs, files starting with a . are hidden files so we change the
        # default distributor value to another placeholder where appropriate
        if distributor is None or distributor.group(0) == "...":
            distributor = "DISTRIB"
        else:
            distributor = distributor.group(0)

        if film is None:
            # provides a default in case the regex returns None
            film = "box-office-page"
        else:
            # replace any illegal characters with a space otherwise function
            # will error due to filename issues
            film = re.sub('"|\:|\/|\\|\<|\>|\||\?|\*|\n', "", film.group(1))

        # prepare the class that will write to a new PDF
        pdf_writer = PdfWriter()
        pdf_writer.add_page(pdf.pages[page])

        # write to a new PDF
        with open(
            f"downloads/{distributor}-{film}-{page}.pdf", mode="wb"
        ) as output_pdf:
            pdf_writer.write(output_pdf)
