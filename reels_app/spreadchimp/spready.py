import os
import csv

import xlrd


def spready(directory):
    # Assumes the directory with the workbook is relative to the script's
    # location.
    item = os.listdir(directory)[0]

    workbook = (f'{directory}/{item}')

    # Preps the workbook that contains the information desired.
    wb = xlrd.open_workbook(workbook)
    sh = wb.sheet_by_index(0)
    total_rows = sh.nrows
    first_row = 6  # skips the first six rows as they are irrelevant.

    # Collects the names of all the films for which individual workbooks need
    # to be created.
    films = []
    for row in range(first_row, total_rows):
        row_values = sh.row_values(row)
        film_title = row_values[23]
        if film_title in films:
            pass
        else:
            films.append(film_title)

    def prep_contacts(film):
        '''Collects all contacts that match the given film into a list that
        will be used to write to the actual spreadsheet.

       Arguments:
            film = The film that contacts purchased tickets for.

        Returns:
            contacts = The list of all contacts for a given film.
        '''
        contacts = []
        for row in range(first_row, total_rows):
            contact = []
            row_values = sh.row_values(row)
            opt_in = row_values[8]
            film_title = row_values[23]
            if not opt_in:
                continue
            elif opt_in and film_title == film:
                contact = [row_values[7],  # email
                           row_values[2].title(),  # first name
                           row_values[4].title(),  # last name
                           row_values[19].replace(
                               'No Primary Phone', ''),  # phone
                           row_values[14],  # address 1
                           row_values[15],  # address 2
                           row_values[16].title(),  # city
                           row_values[17],  # state
                           row_values[18]]  # zip
                contacts.append(contact)
        return contacts

    headers = ['Email', 'First Name', 'Last Name', 'Phone',
               'Street Address', 'Address Line 2', 'City', 'State/Prov/Region',
               'Zip/Postal']
    for film in films:
        contacts = prep_contacts(film)
        with open(f'csvs/{film}.csv', mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow(headers)
            for contact in contacts:
                writer.writerow(contact)
