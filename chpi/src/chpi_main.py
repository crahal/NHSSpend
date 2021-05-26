from parsing_tools import parse_wrapper
from merge_and_evaluate_tools import merge_files, normalizer
import os

raw_path = os.path.join(os.getcwd(), '..', 'data', 'raw')
clean_path = os.path.join(os.getcwd(), '..', 'data')
merge_path = os.path.join(os.getcwd(), '..', 'data', 'clean')

if __name__ == '__main__':

    for subdir in [os.path.join(raw_path, o) for o in os.listdir(raw_path)
                        if os.path.isdir(os.path.join(raw_path,o))]:
        abrev = subdir.split('\\')[-1]
        parse_wrapper(raw_path, clean_path, abrev)
    merged_df = merge_files(os.path.join(clean_path, 'merged'), merge_path)
    merged_df['normalized_supplier'] = merged_df['supplier'].apply(lambda x: normalizer(x, {}))
    merged_df.to_csv(os.path.join(merge_path,'merged_clean_spending.tsv'),
                         encoding='latin-1', sep='\t', index=False)
