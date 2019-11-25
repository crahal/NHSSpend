import pandas as pd
import numpy as np
import os
import re
import csv
from cleanco import cleanco
from tqdm import tqdm
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import connections

connections.create_connection(hosts=['localhost'], timeout=20)
client = Elasticsearch()


def company_normalizer(company_name):
    if isinstance(company_name, str):
        company_name = company_name.upper()
        company_name = company_name.replace(',', '')
        company_name = company_name.replace(' - ', ' ')
        company_name = company_name.replace(r"\(.*\)","")
        company_name = re.sub("[\(\[].*?[\)\]]", "", company_name)
        company_name = company_name.replace(' AND ', ' & ')
        company_name = company_name.strip()
#        company_name = company_name.encode('utf-8')
#        company_name = cleanco(company_name).clean_name()
        company_name = company_name.replace('.', '')
#        company_name = cleanco(company_name).clean_name()
        return company_name
    else:
        return None


def get_matches(matchlist, indexname, num_matches):
    responses = []
    for match in tqdm(matchlist):
        s = Search(using=client, index=indexname).query("match", name=match)
        response = s.execute()
        result_row = {'query_string': match}
        for n, hit in enumerate(response):
               if n<num_matches:
                   result_row['match_{n}'.format(n=n)] = hit.name
                   result_row['score_{n}'.format(n=n)] = hit.meta.score
               else:
                   break
        responses += [result_row]
    return responses


def save_to_csv(rows, filepath, num_matches):
    """Save a list of dictionaries as a csv file"""
    matchlist = ['match_{n}'.format(n=n) for n in range(0, num_matches)]
    scorelist = ['score_{n}'.format(n=n) for n in range(0, num_matches)]
    fieldnames = ['query_string']
    fieldnames = fieldnames + matchlist + scorelist
    with open(filepath, 'w', encoding='utf8') as csvout:
        writer = csv.writer(csvout, delimiter=',')
        writer.writerow(fieldnames)
        outlist = []
        for match in rows:
            row_to_save = []
            for key in fieldnames:
                if key in match:
                    row_to_save.append(str(match[key]))
                else:
                    row_to_save.append(np.nan)
            outlist.append(row_to_save)
        writer.writerows(outlist)


#def get_companydata():
#    ''' needs to be written'''


#def reconcile_everything(datapath, reconcilepath,)


# legacy code, now
#def reconcile_charities(mergepath, reconcilepath, filename, num_matches=5):
#    suppliers = pd.read_csv(os.path.join(mergepath, filename), sep='\t')
#    matchlist = suppliers["supplier"].tolist()
#    charity_responses = get_matches(matchlist, 'charities', num_matches)
#    save_to_csv(charity_responses,
#                os.path.join(reconcilepath, 'charity_matches.csv'),
#                num_matches)


# legacy code, now
#def reconcile_companies(mergepath, reconcilepath, filename,  num_matches=5):
#    suppliers = pd.read_csv(os.path.join(mergepath, filename), sep='\t')
#    matchlist = suppliers["supplier"].tolist()
#    company_responses = get_matches(matchlist, 'companies', num_matches)
#    save_to_csv(company_responses,
#                os.path.join(reconcilepath, 'company_matches.csv'),
#                num_matches)


def reconcile_general(mergepath, reconcilepath, filename,  num_matches=5):
    suppliers = pd.read_csv(os.path.join(mergepath, filename), sep='\t')
    matchlist = suppliers["supplier"].tolist()
    company_responses = get_matches(matchlist, 'general', num_matches)
    save_to_csv(company_responses,
                os.path.join(reconcilepath, 'general_matches.csv'),
                num_matches)
