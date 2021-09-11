import os

from PyPDF2 import PdfFileReader, PdfFileWriter


def split(directory, name_of_split):
    item = os.listdir(directory)[0]  # get the PDF filename

    # join the directory & PDF file name
    new_path = os.path.join(directory, item)

    pdf = PdfFileReader(new_path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))

        with open(f'pdfs/{name_of_split}-{page}.pdf', mode='wb') as output_pdf:
            pdf_writer.write(output_pdf)
