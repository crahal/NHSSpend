import xlrd
import ezodf
import glob
import traceback
import os
from unidecode import unidecode
import numpy as np
import pandas as pd
import ntpath
import logging
import asyncio
from detect_delimiter import detect
from pdf_table_parser import PdfTableParser
module_logger = logging.getLogger('nhsspend_application')
pd.options.mode.chained_assignment = None
module_logger.propagate = False
logging.getLogger().setLevel(logging.ERROR)


async def process_path(ccg_data_path, abrev):
    for (dirpath, dirnames, filenames) in os.walk(os.path.join(ccg_data_path,
                                                               abrev)):
        for filename in filenames:
            name, file_type = os.path.splitext(os.path.join(ccg_data_path,
                                                            abrev))

            if (filename.endswith('.pdf')):
                if os.path.exists(
                   os.path.join(ccg_data_path, abrev, filename+'.csv')) is False:
                    try:
                        module_logger.info('parsing ' + filename)
                        filepath = os.path.join(ccg_data_path,
                                                abrev,
                                                filename)
                        await asyncio.wait_for(parse_pdf_file(filepath),
                                               timeout=60)
                    except asyncio.TimeoutError:
                        module_logger.error('Timeout in pdf ' + filename)
                else:
                    module_logger.info('We have already parsed ' + filename)


async def parse_pdf_file(filepath):
    # TODO much of this should be handled by the parser object,
    # including exception catches and generating results dict
    module_logger.info('Starting to process pdf ' + filepath)
    try:
        # TODO dont need to join dirpath to filename
        parser = PdfTableParser(filepath)
        parser.get_page_layouts()
        parser.parse_layouts()
        parser.save_output()
    except Exception as e:
        module_logger.error('Error in pdf ' + filepath + ' :' + str(e))


def load_excel(file_):
    df = pd.read_excel(file_, index_col=None,
                       header=None, error_bad_lines=False,
                       skip_blank_lines=True, warn_bad_lines=False)
    return df


def load_text(file_):
    try:
        encoding = 'latin-1'
        with open(file_, 'r', encoding=encoding) as file:
            data = file.read().replace('\n', '')
            sep = detect(data)
        df = pd.read_csv(file_, index_col=None,
                         encoding=encoding, header=None,
                         error_bad_lines=False,
                         skip_blank_lines=True,
                         warn_bad_lines=False, engine='python',
                         sep=sep)
        return df
    except Exception as e:
        try:
            encoding = 'utf-8'
            with open(file_, 'r', encoding=encoding) as file:
                data = file.read().replace('\n', '')
                sep = detect(data)
            df = pd.read_csv(file_, index_col=None,
                             encoding=encoding, header=None,
                             error_bad_lines=False,
                             skip_blank_lines=True,
                             warn_bad_lines=False, engine='python',
                             sep=sep)
            return df
        except Exception as e:
            try:
                encoding = 'utf-16'
                with open(file_, 'r', encoding=encoding) as file:
                    data = file.read().replace('\n', '')
                    sep = detect(data)
                df = pd.read_csv(file_, index_col=None,
                                 encoding=encoding, header=None,
                                 error_bad_lines=False,
                                 skip_blank_lines=True,
                                 warn_bad_lines=False,
                                 sep=sep)
                return df
            except Exception as e:
                try:
                    encoding = "ISO-8859-1"
                    with open(file_, 'r', encoding=encoding) as file:
                        data = file.read().replace('\n', '')
                        sep = detect(data)
                    df = pd.read_csv(file_, index_col=None,
                                     encoding=encoding, header=None,
                                     error_bad_lines=False,
                                     skip_blank_lines=True,
                                     warn_bad_lines=False, engine='python',
                                     sep=sep)
                    return df
                except Exception as e:
                    module_logger.warn('Cant parse ' + ntpath.basename(file_))


def createdir(filepath, ins_type, ins):
    ''' check if the necessary subdirectory, and if not, make it'''
    if os.path.exists(os.path.join(filepath, ins_type, ins)) is False:
        os.makedirs(os.path.join(filepath, ins_type, ins))
    print('Working on ' + ins + '.')
    module_logger.info('Working on ' + ins + '.')


def remove_null_files(filepath, abrev):
    remList = ['annual','report','map','guide', 'fact', 'govern', 'leadership']
    allFiles = glob.glob(os.path.join(filepath, abrev, '*'))
    for file_ in allFiles:
        if file_.endswith('.pdf'):
            for word in remList:
                if word in file_:
                    os.remove(file_)
                    break


def parse_wrapper(ccg_data_path, filepath, abrev):
    try:
        remove_null_files(ccg_data_path, abrev)
        asyncio.run(process_path(ccg_data_path, abrev))
        df = parse_data(ccg_data_path, abrev)
        df.to_csv(os.path.join(filepath, '../..', 'cleaned',
                               abrev + '.csv'), index=False)
        module_logger.info('Successfully parsed: ' + str(abrev))
    except Exception as e:
        module_logger.debug('Parsing files failed: ' + traceback.format_exc())


def heading_replacer(columnlist, filepath):
    columnlist = [x if str(x) != 'nan' else 'dropme' for x in columnlist]
    columnlist = ['dropme' if str(x) == '-1.0' else x for x in columnlist]
    columnlist = [x if str(x) != '£' else 'amount' for x in columnlist]
    columnlist = [unidecode(x) if type(x) is str else x for x in columnlist]
    if ('Total Amount' in columnlist) and ('Amount' in columnlist):
        columnlist = ['dropme' if x ==
                      'Total Amount' else x for x in columnlist]
    if ('Gross' in columnlist) and ('Nett Amount' in columnlist):
        columnlist = ['Amount' if str(x) == 'Gross' else x for x in columnlist]
        columnlist = ['dropme' if str(x) ==
                      'Nett Amount' else x for x in columnlist]
    if ('Gross' in columnlist) and ('NET ' in columnlist):
        columnlist = ['Amount' if str(x) == 'Gross' else x for x in columnlist]
        columnlist = ['dropme' if str(x) == 'NET ' else x for x in columnlist]
    if ('Gross' in columnlist) and ('Amount' not in columnlist):
        columnlist = ['Amount' if str(x) == 'Gross' else x for x in columnlist]
    if ('Mix of Nett & Gross' in columnlist) and ('Amount' not in columnlist):
        columnlist = ['Amount' if str(x) ==
                      'Mix of Nett & Gross' else x for x in columnlist]
    columnlist = [
        'dropme' if 'departmentfamily' in str(x) else x for x in columnlist]
    columnlist = ['amount' if str(x) == '£' else x for x in columnlist]
    columnlist = [''.join(filter(str.isalpha, str(x).lower()))
                  for x in columnlist]
    replacedict = pd.read_csv(os.path.join(
        filepath, '..', '..', 'data_support', 'replacedict.csv'),
        header=None, dtype={0: str}).set_index(0).squeeze().to_dict()
    for item in range(len(columnlist)):
        for key, value in replacedict.items():
            if key == columnlist[item]:
                columnlist[item] = columnlist[item].replace(key, value)
    return columnlist


def clean_df(df, list_, file_, filepath):
    try:
        if len(df.columns) < 3:
            if df.iloc[0].str.contains('!DOC').any():
               module_logger.debug(ntpath.basename(file_) + ': html. Delete.')
               return None
            elif df.iloc[0].str.contains('no data', case=False).any():
                module_logger.debug(ntpath.basename(file_) + ': no data.')
                return None
            else:
                module_logger.debug(ntpath.basename(file_) + ': not tabular?')
                return None
        while (((any("supplier" in str(s).lower() for s in list(df.iloc[0]))) is False)
               and ((any("merchant" in str(s).lower() for s in list(df.iloc[0]))) is False)
               and ((any("merchant name" in str(s).lower() for s in list(df.iloc[0]))) is False)
               and ((any("vendor name" in str(s).lower() for s in list(df.iloc[0]))) is False)
               and ((any("suppidt)" in str(s).lower() for s in list(df.iloc[0]))) is False)
               and ((any("supplier name" in str(s).lower() for s in list(df.iloc[0]))) is False)) \
            or (((any("amount" in str(s).lower() for s in list(df.iloc[0]))) is False)
                    and ((any("total" in str(s).lower() for s in list(df.iloc[0]))) is False)
                and ((any("gross" in str(s).lower() for s in list(df.iloc[0]))) is False)
                and ((any("£" in str(s).lower() for s in list(df.iloc[0]))) is False)
                and ((any("spend" in str(s).lower() for s in list(df.iloc[0]))) is False)
                #                    and ((any("sum of amount" in str(s).lower() for s in list(df.iloc[0]))) is False)
                and ((any("mix of nett & gross" in str(s).lower() for s in list(df.iloc[0]))) is False)
                and ((any("value" in str(s).lower() for s in list(df.iloc[0]))) is False)):
            try:
                df = df.iloc[1:]
            except Exception as e:
                module_logger.debug('Problem with trimming' +
                                    ntpath.basename(file_) +
                                    '. ' + str(e))
        df.columns = heading_replacer(list(df.iloc[0]), filepath)
        if file_.endswith('.pdf.csv'):
            counter = 0
            amount_count = np.nan
            vat_count = np.nan
            trans_count = np.nan
            for col in df.columns.tolist():
                counter = counter + 1
                if 'vat' in col.lower():
                    vat_count = counter
                if 'amount' in col.lower():
                    amount_count = counter
                if amount_count == vat_count-1:
                    df['amount'] = np.nan
                    break
            for col in df.columns.tolist():
                counter = counter + 1
                if 'trans' in col.lower():
                    trans_count = counter
                if 'amount' in col.lower():
                    amount_count = counter
                if (amount_count == trans_count-1) or  (amount_count == trans_count+1):
                    df = df[~(df['transactionnumber'].isnull())]
                    break
        if len(df.columns.tolist()) != len(set(df.columns.tolist())):
            df = df.loc[:, ~df.columns.duplicated()]
        df = df.iloc[1:]
        df.rename(columns=lambda x: x.strip(), inplace=True)
        # drop empty rows and columns where half the cells are empty
        df = df.dropna(thresh=4, axis=0)
        df = df.dropna(thresh=0.75 * len(df), axis=1)
        df['file'] = ntpath.basename(file_)
        if (list(df).count('amount') == 0) and\
           (list(df).count('gross') == 1):
            df = df.rename(columns={'gross': 'amount'})
        if (list(df).count('amount') == 0) and\
           (list(df).count('grossvalue') == 1):
            df = df.rename(columns={'grossvalue': 'amount'})
        if len(df) > 0:
            try:
                df['negative'] = 1
                df['negative'] = np.where(df['amount'].astype(str).str.contains('-'), -1, df['negative'])
                df['negative'] = np.where(df['amount'].astype(str).str.contains('\('), -1, df['negative'])
                df['amount'] = df['amount'].astype(str).str.replace(
                   ',', '').str.extract('(\d+)', expand=False).astype(float)
                df['amount'] = df['amount']*df['negative']
            except Exception as e:
                module_logger.debug("Can't convert amount to float in " +
                                    ntpath.basename(file_) +
                                    'Columns in file :' + str(df.columns.tolist()))
            if df.empty is False:
                module_logger.info('Successfully parsed: ' +
                                   ntpath.basename(file_))
                return df
        else:
            module_logger.info('No data in ' + ntpath.basename(file_) + '!')
    except Exception as e:
        try:
            module_logger.debug('The columns: ' + str(df.columns.tolist()) +
                                ' in ' + ntpath.basename(file_))
        except Exception as e:
            try:
                module_logger.debug('The first row: ' + str(df.iloc[0]) +
                                    ' in ' + ntpath.basename(file_))
            except:
                module_logger.debug('Problem with ' + ntpath.basename(file_) +
                                    ': ' + str(e))


def parse_data(filepath, department, filestoskip=[]):
    allFiles = glob.glob(os.path.join(filepath, department, '*'))
    frame = pd.DataFrame()
    list_ = []
    filenames = []
    removefields = pd.read_csv(os.path.join(
        filepath, '..', '..', 'data_support', 'remfields.csv'),
        names=['replacement'])['replacement'].values.tolist()
    for file_ in allFiles:
        if (', '.join(ntpath.basename(file_).split('.')[0]) not in filenames) and \
           (ntpath.basename(file_).endswith('.pdf') is False):
            filenames.append(ntpath.basename(file_).split('.')[0])
            if ntpath.basename(file_) in [x.lower() for x in filestoskip]:
                module_logger.info(ntpath.basename(file_) +
                                   ' is excluded! Verified problem.')
                continue
            if os.path.getsize(file_) == 0:
                module_logger.debug(ntpath.basename(
                    file_) + ' is 0b: skipping')
                continue
            if file_.lower().endswith(tuple(['.csv', '.xls', '.tsv',
                                             '.xlsx', '.ods'])) is False:
                module_logger.debug(ntpath.basename(file_) +
                                    ': not csv, xls, xlsx or ods: ' +
                                    ' not parsing...')
                continue
            df = pd.DataFrame()
            if (file_.lower().endswith('.xls')) or\
               (file_.lower().endswith('xlsx')):
                try:
                    df = load_excel(file_)
                except Exception as e:
                    try:
                        df = load_text(file_)
                        module_logger.debug('cant read ' + str(file_) + ' as' +
                                            ' .xls, but can read a text file')
                    except:
                       module_logger.debug('cant read ' + str(file_) +
                                          ' as .xls or a text file')
            elif (file_.lower().endswith('.csv')) or\
                 (file_.lower().endswith('.tsv')):
                try:
                    df = load_text(file_)
                except Exception as f:
                    module_logger.debug('cant read ' + str(file_) +
                                        ' as csv/tsv')
                    print(traceback.format_exc())
            elif (file_.lower().endswith('.ods')):
                df = read_ods(file_)
                df.index = df.index + 1  # shifting index
                df = df.sort_index()
            else:
                print('???')
            try:
                if not df.empty:
                    df = clean_df(df, list_, file_, filepath)
                    list_.append(df)
            except Exception as e:
                print(e)
            else:
                continue
    frame = pd.concat(list_, sort=False)
    for column in frame.columns.tolist():
        if column.lower() in removefields:
            frame.drop([column], inplace=True, axis=1)
        if (column == ' ') or (column == ''):
            frame.drop([column], inplace=True, axis=1)
    #    frame = frame.drop_duplicates(keep='first', inplace=True)
    if 'nan' in list(frame):
        frame = frame.drop(labels=['nan'], axis=1)
    return frame


def read_date(date):
    return xlrd.xldate.xldate_as_datetime(date, 0)


def read_ods(filename, sheet_no=0, header=0):
    tab = ezodf.opendoc(filename=filename).sheets[sheet_no]
    df = pd.DataFrame({col[header].value: [x.value for x in col[header + 1:]]
                       for col in tab.columns()})
    df = df.T.reset_index(drop=False).T
    df = df.drop(columns=[list(df)[-1]], axis=1)
    return df.T.reset_index(drop=False).T


#def merge_files(rawpath):
#    frame = pd.DataFrame()
#    list_ = []
#    for file_ in glob.glob(os.path.join(rawpath, '..', 'output',
#                                        'mergeddepts', '*.csv')):
#        df = pd.read_csv(file_, index_col=None, low_memory=False,
#                         header=0, encoding='latin-1',
#                         dtype={'transactionnumber': str,
#                                'amount': float,
#                                'supplier': str,
#                                'date': str,
#                                'expensearea': str,
#                                'expensetype': str,
#                                'file': str})
#        df['dept'] = ntpath.basename(file_)[:-4]
#        list_.append(df)
#    frame = pd.concat(list_, sort=False)
#    frame.dropna(thresh=0.90 * len(df), axis=1, inplace=True)
#    if pd.to_numeric(frame['date'], errors='coerce').notnull().all():
#        frame['date'] = pd.to_datetime(frame['date'].apply(read_date),
#                                       dayfirst=True,
#                                       errors='coerce')
#    else:
#        df['date'] = pd.to_datetime(df['date'],
#                                    dayfirst=True,
#                                    errors='coerce')
#    frame['transactionnumber'] = frame['transactionnumber'].str.replace('[^\w\s]', '')
#    frame['transactionnumber'] = frame['transactionnumber'].str.strip("0")
#    return frame
