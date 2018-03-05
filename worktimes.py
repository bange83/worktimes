import tabula
import pandas as pd
import numpy as np
import os

WORKPATH = '/Volumes/Transcend/nore/gdrive/Documents/OttoPrivat/worktimes/'


def filter_weekdays(table):
        valid_weekdays = ['MO', 'DI', 'MI', 'DO', 'FR', 'SA', 'SO']
        return table[table[0].str.contains(('|').join(valid_weekdays)) == True]


def glz2float(x):
        x = str(x)
        if x.find("-") > 0:
            x = x.replace("-", "")
            x = x.replace(",", ".")
            return -1 * float(x)
        else:
            x = x.replace(",", ".")
            return float(x)


def parse_table(filename):
    df = tabula.read_pdf(filename, encoding='ISO-8859-1', multiple_tables=True)

    table = df[1]

    if pd.isnull(table[1]).all():
        del table[1]
        table.columns = np.arange(0, 11)

    pd.options.mode.chained_assignment = None

    table = filter_weekdays(table)
    table['year'] = filename.split('-')[0].split('/')[-1]
    table['month'] = filename.split('-')[1].split('.')[0]
    table['day'] = table[0].str.split(" ").apply(lambda x: int(x[0]))
    table['weekday'] = table[0].str.split(" ").apply(lambda x: x[2])
    table['state'] = table[0].str.split(" ").apply(lambda x: (" ").join(x[4:]))
    table['plan'] = table[1]
    table['begin'] = table[2]
    table['end'] = table[3]
    table['trackedtime'] = table[4].str.replace(",", ".").astype(float)
    table['resttime'] = table[5].str.replace(",", ".").astype(float)
    table['restbonus'] = table[6].str.replace(",", ".").astype(float)
    table['worktime'] = table[7].str.replace(",", ".").astype(float)
    table['solltime'] = table[8].str.replace(",", ".").astype(float)
    table['glz'] = table[9].apply(lambda x: glz2float(x))
    table['overworktime'] = table[10].str.replace(",", ".").astype(float)

    parsed_table = table.loc[:, 'year':'overworktime']
    return parsed_table
    # parsed_table.to_csv(filename.replace(".pdf", ".csv"), index=False)


def get_pdf_files():
    pdf_path = WORKPATH + 'pdf'
    pdf_files = [f for f in os.listdir(pdf_path) if f.endswith('.pdf')]
    return pdf_files


def main():
    csv_path = WORKPATH + 'csv/'
    filenames = get_pdf_files()
    for filename in filenames:
        print(filename)
        parsed_table = parse_table(WORKPATH + 'pdf/' + filename)
        parsed_table.to_csv(csv_path + filename.replace(".pdf", ".csv"), index = False)


if __name__ == '__main__':
    main()
