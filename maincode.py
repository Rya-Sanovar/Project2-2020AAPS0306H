from pandacode import datafile
from seleniumcode import WebScrape
import re

def fill_data(business_name, address_list, source):
    row_index = datafile.index[(datafile['Business Name'] == business_name)]
    datafile.at[row_index, 'Source'] = source
    datafile.at[row_index, "Street Address"] = address_list[0]
    datafile.at[row_index, "City"] = address_list[1]
    datafile.at[row_index, "State"] = address_list[2]
    datafile.at[row_index, "Zip"] = address_list[3]

#FIRST - We go to the California Business Search website.
calsearch = WebScrape()
corpwiki = WebScrape()

for business_name in datafile['Business Name']:
    calsearch.get("https://businesssearch.sos.ca.gov/")
    if re.search("LLC", business_name, re.IGNORECASE) or re.search("LP", business_name, re.IGNORECASE):
        calsearch.click_button("LLCNameOpt")
    else:
        calsearch.click_button("CorpNameOpt")

    calsearch.search_box("SearchCriteria", business_name)
    address_list = calsearch.get_results(business_name)
    if type(address_list) is list:
        source = "California Business Search"
        fill_data(business_name, address_list, source)
    else: #it returns 1
        #go to Corp Wiki and check
        corpwiki.get("https://www.corporationwiki.com/")
        corpwiki.search_box("keywords", business_name)
        address_list = corpwiki.get_results2(business_name)
        if type(address_list) is list:
            source = "Corporation Wiki"
            fill_data(business_name, address_list, source)
        else:
            empty_list = [" ", " ", " ", " "]
            fill_data(business_name, empty_list, source)
    
calsearch.quit()
corpwiki.quit()

print(datafile.head)

