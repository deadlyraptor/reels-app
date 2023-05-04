import os
# import csv

# import xlrd
from flask import current_app
from openpyxl import load_workbook


def spready(directory):

    directory = current_app.config['SPREADSHEET_FOLDER']
    manifest = os.listdir(directory)[0]

    wb = load_workbook(filename=(f'{directory}/{manifest}'))
    ws = wb.active

    last_row = ws.max_row
    first_row = 7

    series = []
    for row in range(first_row, last_row):
        series_title = ws.cell(row, 23).value
        if series_title in series or series_title is None:
            continue
        else:
            series.append(series_title)

    def prep_contacts(series):
        '''
        Collects all contacts that  match the given series into a list that
        will be used to write the actual spreadsheet.

        Arguments:
            series = The series the customer attended. Note that the original
            workbook has the film name but users change it to the series before
            running the workbook through the script.

        Returns:
            contacts = The list of all contacts for a given series.
        '''

        contacts = []
        for row in range(first_row, last_row):
            contact = []
            opt_in = ws.cell(row, 8).value  # email opt-in, column H
            series_title = ws.cell(row, 23).value
            if not opt_in:
                continue
            elif opt_in and series_title == series:
                contact = [ws.cell(row, 7).value,  # email, column G
                           ws.cell(row, 3).value.title(),  # first name, col C
                           ws.cell(row, 5).value.title(),  # last name, col E
                           ws.cell(row, 19).value.replace
                           ('No Primary Phone', ''),  # phone number, col S
                           ws.cell(row, 14).value,  # address 1, col N
                           ws.cell(row, 15).value,  # address 2, col O
                           ws.cell(row, 16).value.title(),  # city, col P
                           ws.cell(row, 17).value,  # state, col Q
                           ws.cell(row, 18).value,  # postal code, col R
                           ]
                contacts.append(contact)

    for series in series:
        contacts = prep_contacts(series)

        # Assumes the directory with the workbook is relative to the script's
        # location.
        # item = os.listdir(directory)[0]

        # workbook = (f'{directory}/{item}')

        # Preps the workbook that contains the information desired.
        # wb = xlrd.open_workbook(workbook)
        # sh = wb.sheet_by_index(0)
        # total_rows = sh.nrows
        # first_row = 6  # skips the first six rows as they are irrelevant.

        # Collects the names of all the films for which individual workbooks need
        # to be created.
        # films = []
        # for row in range(first_row, total_rows):
        #    row_values = sh.row_values(row)
        #    film_title = row_values[23]
        #    if film_title in films:
        #        pass
        #    else:
        #        films.append(film_title)

        # def prep_contacts(film):
        # Collects all contacts that match the given film into a list that
        #    will be used to write to the actual spreadsheet.

        #   Arguments:
        #        film = The film that contacts purchased tickets for.

        #    Returns:
        #        contacts = The list of all contacts for a given film.

        # contacts = []
        # for row in range(first_row, total_rows):
        #     contact = []
        #     row_values = sh.row_values(row)
        #     opt_in = row_values[8]
        #     film_title = row_values[23]
        #     if not opt_in:
        #         continue
        #     elif opt_in and film_title == film:
        #         contact = [row_values[7],  # email
        #                    row_values[2].title(),  # first name
        #                    row_values[4].title(),  # last name
        #                    row_values[19].replace(
        #                        'No Primary Phone', ''),  # phone
        #                    row_values[14],  # address 1
        #                    row_values[15],  # address 2
        #                    row_values[16].title(),  # city
        #                    row_values[17],  # state
        #                    row_values[18]]  # zip
        #         contacts.append(contact)
        # return contacts

        # headers = ['Email', 'First Name', 'Last Name', 'Phone',
        #            'Street Address', 'Address Line 2', 'City', 'State/Prov/Region',
        #            'Zip/Postal']
        # for film in films:
        # contacts = prep_contacts(film)
        # with open(f'csvs/{film}.csv', mode='w', newline='') as csvfile:
        #  writer = csv.writer(csvfile, delimiter=',', quotechar='"',
        #                    quoting=csv.QUOTE_MINIMAL)
        # writer.writerow(headers)
        # for contact in contacts:
        #   writer.writerow(contact)
