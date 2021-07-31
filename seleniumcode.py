from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PATH = "C:/Users/Rya/Desktop/Project2-2020AAPS0306H/chromedriver.exe"
class WebScrape:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=PATH)
        self.driver.maximize_window()
    
    def get(self, url):
        self.driver.get(url)
    
    def click_button(self, id):
        button = self.driver.find_element_by_id(id)
        button.click()

    def search_box(self, id, query):
        box = self.driver.find_element_by_id(id)
        box.send_keys(query)
        box.send_keys(Keys.ENTER) #Key.RETURN also works

    def get_address(self, address):
        list0 = address.splitlines() #["1711 W. TEMPLE ST", "LOS ANGELES CA 90026"]
        street_address = list0[0]
        list1 = list0[1].rsplit(" ", 1) #["LOS ANGELES CA", "90026"]
        zipcode = list1[1]
        list2 = list1[0].rsplit(" ", 1)#["LOS ANGELES", "CA"]
        city = list2[0]
        state = list2[1]
        mylist = [street_address, city, state, zipcode]
        return mylist

    def next_page_exists(self):
        next_button = self.driver.find_element_by_id("enitityTable_next")
        classValue = next_button.get_attribute("class")
        if classValue == "paginate_button next disabled":
            return 1
        elif classValue == "paginate_button next":
            next_button.find_element_by_tag_name("a").click()
            return 0

    def get_results(self, business_name):
        while(True):
            RowCount = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "RowCount")))
            if RowCount.text == "0 entity records (out of 0 records found).":
                return 1
            else:
                tbody = self.driver.find_element_by_tag_name("tbody")
                list_of_rows = tbody.find_elements_by_tag_name("tr") #returns list of all the rows on that page
                for row in list_of_rows:
                    button = row.find_element_by_name("EntityId")
                    if button.text.lower() == business_name.lower():
                        button.click()
                        address = self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[3]/div[1]/div[6]/div[2]").text
                        address_list = self.get_address(address)
                        #self.driver.quit()
                        return address_list
                #self.driver.quit()
                x = self.next_page_exists()
                if x == 1:
                    return 1
                else:
                    continue
    
    def get_results2(self, business_name):
        ResultStats = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "results-stats")))
        if ResultStats.text == "0 Results Found":
            return 1
        else:
            main = self.driver.find_element_by_id("results-details")
            list_of_results = main.find_elements_by_class_name("list-group-item")
            for result in list_of_results:
                row = result.find_element_by_class_name("row")
                button = row.find_element_by_class_name("ellipsis")
                if button.text.lower() == business_name.lower():
                    button.click()
                    streetAddress = self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div/div/div[1]/div[10]/div/div/div/a[1]/span/span[1]").text
                    city = self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div/div/div[1]/div[10]/div/div/div/a[1]/span/span[2]").text
                    state = self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div/div/div[1]/div[10]/div/div/div/a[1]/span/span[3]").text
                    zipcode = self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div/div/div[1]/div[10]/div/div/div/a[1]/span/span[4]").text
                    address_list = [streetAddress, city, state, zipcode]
                    #self.driver.quit()
                    return address_list
            #self.driver.quit()
            return 1
    
    def quit(self):
        self.driver.quit()



"""     def cal_get_results(self, business_name):
        #Also we need to wait for main to exist on the page, because this function is called immediately after we hit enter in search box.
        #So pages take time to load. So we need to wait for the page to load, then search for main.
        not_found = False
        try:
            main = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "enitityTable")))
            t_body = main.find_element_by_tag_name("tbody")
            list_of_rows = t_body.find_elements_by_tag_name("tr")#returns a list of all the rows
            #skip these 2 lines and write- list_of_rows = main.find_elements
            for row in list_of_rows:
                td = row.find_element_by_class_name("sorting_1")
                button = td.find_element_by_name("EntityId")
                if button.text.lower() == business_name.lower():
                    button.click()
                    address = self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div[3]/div[1]/div[6]/div[2]").text
                    address_list = self.get_address(address)
                    return address_list
                else:
                    not_found = True
                    return not_found
            if self.go_next_page() == True :
                self.wiki_get_results(business_name)
                if self.go_next_page() == True:
                    self.get_results(business_name)
                else:
                    not_found = True
                    return not_found
            else:
                not_found = True  
                return not_found
        finally:
            time.sleep(20)
            self.driver.quit()"""

"""calsearch = WebScrape()
business_name = "L.A. DOWNTOWN MEDICAL CENTER LLC"
calsearch.get("https://businesssearch.sos.ca.gov/")
if re.search("LLC", business_name, re.IGNORECASE) or re.search("LP", business_name, re.IGNORECASE):
    calsearch.click_button("LLCNameOpt")
else:
    calsearch.click_button("CorpNameOpt")

calsearch.search_box("SearchCriteria", business_name)
calsearch.get_results("L.A. DOWNTOWN MEDICAL CENTER LLC")"""
            