import pandas as pd
import numpy as np
import os
import string
import csv
from tqdm import tqdm
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl import connections

connections.create_connection(hosts=['localhost'], timeout=20)
client = Elasticsearch()


def normalizer(name, norm_dict={}):
    ''' normalise entity names with manually curated dict'''
    if isinstance(name, str):
        name = name.upper()
        for key, value in norm_dict.items():
            name = name.replace(key, value)
        name = name.replace(r"\(.*\)", "")
        name = "".join(l for l in name if l not in string.punctuation)
        name = ' '.join(name.split())
        name = name.strip()
        return name
    else:
        return None


def get_matches(matchlist, indexname, num_matches):
    ''' get matches from ES indexname instance'''
    responses = []
    for match in tqdm(matchlist):
        s = Search(using=client, index=indexname).query("match", name=match)
        response = s.execute()
        result_row = {'query_string': match}
        for n, hit in enumerate(response):
            if n < num_matches:
                result_row['match_{n}'.format(n=n)] = hit.name
                result_row['score_{n}'.format(n=n)] = hit.meta.score
            else:
                break
        responses += [result_row]
    return responses


def save_to_csv(rows, filepath, num_matches):
    ''' reshape the ES output data'''
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


def reconcile_general(mergepath, reconcilepath, filename,  num_matches=5):
    ''' high level reconciliation function for raw names'''
    suppliers_ccg = pd.read_csv(os.path.join(mergepath, filename[0]), sep='\t')
    suppliers_trust = pd.read_csv(os.path.join(mergepath, filename[1]), sep='\t')
    suppliers_nhsengland = pd.read_csv(os.path.join(mergepath, filename[2]), sep='\t')
    matchlist = suppliers_ccg["supplier"].tolist()+suppliers_trust["supplier"].tolist()+suppliers_nhsengland["supplier"].tolist()
    matchlist = list(set(matchlist))
    company_responses = get_matches(matchlist, 'general', num_matches)
    save_path = os.path.join(reconcilepath, 'general_matches.csv')
    save_to_csv(company_responses, save_path, num_matches)


def reconcile_general_norm(mergepath, reconcilepath, filename,
                           norm_path, num_matches=5):
    ''' high level reconciliation function for normalised names'''
    suppliers_ccg = pd.read_csv(os.path.join(mergepath, filename[0]), sep='\t')
    norm_df = pd.read_csv(norm_path, sep='\t')
    norm_dict = dict(zip(norm_df['REPLACETHIS'], norm_df['WITHTHIS']))
    suppliers_ccg['supplier'] = suppliers_ccg['supplier'].\
        apply(lambda x: normalizer(x, norm_dict))
    suppliers_trust = pd.read_csv(os.path.join(mergepath, filename[1]), sep='\t')
    suppliers_trust['supplier'] = suppliers_trust['supplier'].\
        apply(lambda x: normalizer(x, norm_dict))
    suppliers_nhsengland = pd.read_csv(os.path.join(mergepath, filename[2]), sep='\t')
    suppliers_nhsengland['supplier'] = suppliers_nhsengland['supplier'].\
        apply(lambda x: normalizer(x, norm_dict))
    matchlist = suppliers_ccg["supplier"].tolist()+suppliers_trust["supplier"].tolist()+suppliers_nhsengland["supplier"].tolist()
    matchlist = list(set(matchlist))
    company_responses = get_matches(matchlist, 'general_norm', num_matches)
    save_path = os.path.join(reconcilepath, 'general_norm_matches.csv')
    save_to_csv(company_responses, save_path, num_matches)
