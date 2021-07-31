import pandas as pd

datafile = pd.read_excel('rawwestlawfile_1.xlsm', sheet_name='WestlawNext - Docket Alert All ', skiprows= 1) #read .xlsm file into a dataframe

datafile.drop(datafile.columns[[1, 13, 14, 15]], axis=1, inplace = True) #delete title column + last 3 columns

corp_terms_file = pd.read_csv('corp_terms_list.csv', header = None, names=['corpterms']) #read csv file as a dataframe

found = False

for business_name in datafile['Business Name']:
    terms0 = business_name.split()
    for i in terms0:
        terms1 = i.split(',')
        for j in terms1:
            j = j.lower()
            for k in list(corp_terms_file['corpterms']):
                if j == k.lower():
                    found = True
                    break
            if found:
                break
        if found:
            break
    if not found:
        datafile.drop(datafile.index[(datafile['Business Name'] == business_name)], axis = 0, inplace=True)
    else:
        found = False




