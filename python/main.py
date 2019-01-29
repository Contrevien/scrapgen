from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import re
import sys
import csv
import urllib.request
from collections import Counter
import json


def valid_link(link, domain):
    '''
        Utility
        Determine whether the link is within the domain
    '''

    if link.find("https://") == 0:
        link = link[8:]
    if link.find("http://") == 0:
        link = link[7:]

    if domain in link.split("."):
        return True
    return False


def find_last_name(url):
    '''
        Returns string between last and second-last '/'
    '''

    if url[-1] == '/':
        url = url[:-1]

    return url.split('/')[-1]


class Webpage(object):

    def __init__(self, url, domain):
        ch = os.getcwd() + '/python/tools/chromedriver'
        options = Options()
        options.set_headless(headless=True)
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options, executable_path=ch)
        self.domain = domain
        self.url = url
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        body = self.driver.find_element_by_tag_name("body")
        text = body.get_attribute("innerText")
        spaced_text = ""
        for s in text:
            if s == "\n":
                spaced_text += " "
            elif s.isupper():
                spaced_text += s.lower()
            else:
                spaced_text += s
        self.words = spaced_text.split()
        self.sentences = spaced_text.split('\n')
        self.frequency = Counter(self.words)
        self.befores = dict()
        self.afters = dict()
        for i in range(len(self.words)):
            if i == 0:
                self.befores[self.words[i]] = [""]
                self.afters[self.words[i]] = [self.words[i+1]]
                continue

            if i == len(self.words) - 1:
                if self.words[i] in self.befores.keys():
                    self.befores[self.words[i]].append(self.words[i-1])
                else:
                    self.befores[self.words[i]] = [self.words[i-1]]
                if self.words[i] in self.afters.keys():
                    self.afters[self.words[i]].append("")
                else:
                    self.afters[self.words[i]] = [""]
                continue

            if self.words[i] in self.befores.keys():
                self.befores[self.words[i]].append(self.words[i-1])
            else:
                self.befores[self.words[i]] = [self.words[i-1]]
            if self.words[i] in self.afters.keys():
                self.afters[self.words[i]].append(self.words[i+1])
            else:
                self.afters[self.words[i]] = [self.words[i+1]]

    def get_links(self):
        '''
            Fetch all the a-tags in the webpage
        '''

        page_links = self.driver.find_elements_by_xpath("//a[@href]")

        if len(page_links) == 0:
            print("No links found!")
            return

        links = []
        for link_el in page_links:
            link = link_el.get_attribute("href")
            if valid_link(link, self.domain):  # tested
                links.append(link)
        return links

    def get_words(self):
        '''
            Get all the words from the webpage
        '''

        return list(filter(lambda x: len(x) > 2 and all(char.isalpha() for char in x), self.words))

    def get_numbers(self):
        '''
            Get all the numbers from the webpage
        '''

        return list(filter(lambda x: all(char.isdigit() for char in x), self.words))

    def get_emails(self):
        '''
            Get all the emails from the webpage
        '''

        return list(filter(lambda x: re.match(r"[^@]+@[^@]+\.[^@]+", x), self.words))

    def get_tables_as_list(self, start=None, end=None):
        '''
            Fetch all tables
            Return content from tables no. "start" to table no. "end" as lists
            [
                [
                    [col1, col2, col3],
                    [val1, val2, val3],
                    [val4, val5, val6],
                ],
                [
                    [col1, col2, col3],
                    [val1, val2, val3],
                    [val4, val5, val6],                    
                ]
            ]
        '''

        tables = self.driver.find_elements_by_tag_name("table")
        if len(tables) == 0:
            print("No tables found!")
            return

        if end != None:
            tables = tables[start:end]

        content = []

        for table in tables:
            table_content = []

            rows = table.find_elements_by_tag_name("tr")
            for row in rows:
                row_content = []
                cols = row.find_elements_by_css_selector("*")
                for col in cols:
                    row_content.append(col.text)
                table_content.append(row_content)
            content.append(table_content)

        return content

    def get_tables_as_csv(self, start=None, end=None):
        '''
            Get Tables and save as csv file
        '''

        content = self.get_tables_as_list(start, end)

        if len(content) == 0:
            print("No tables found!")
            return

        with open(self.domain + "-tables.csv", "w", newline="") as new_file:
            csv_writer = csv.writer(new_file)

            for table in content:
                empty = ""
                for row in table:
                    csv_writer.writerow(row)
                csv_writer.writerow(empty)

    def get_images(self):
        '''
            Get all images from the website
        '''

        images = self.driver.find_elements_by_tag_name("img")
        image_urls = []
        for img in images:
            xp = self.driver.execute_script("""gPt=function(c){
                                 if(c.id!==''){
                                     return'id("'+c.id+'")'
                                 } 
                                 if(c===document.body){
                                     return c.tagName
                                 }
                                 var a=0;
                                 var e=c.parentNode.childNodes;
                                 for(var b=0;b<e.length;b++){
                                     var d=e[b];
                                     if(d===c){
                                         return gPt(c.parentNode)+'/'+c.tagName+'['+(a+1)+']'
                                     }
                                     if(d.nodeType===1&&d.tagName===c.tagName){
                                         a++
                                     }
                                 }
                             };
                             return gPt(arguments[0]).toLowerCase();""", img)
            attr = self.driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', img)
            one_attr = ""
            for key,val in attr.items():
                one_attr = str(key) + "=" + str(val)
                break
            image_urls.append(["src=" + img.get_attribute('src'), "xpath=" + xp, one_attr])

        imgs = []
        for x in image_urls:
            imgs.append({"img": x})

        return imgs

        # try:
        #     os.mkdir(find_last_name(self.url) + "-images")
        # except:
        #     pass
        # index = 1
        # for img in images:
        #     src = img.get_attribute('src')
        #     urllib.request.urlretrieve(
        #         src, "./" + find_last_name(self.url) + "-images/" + find_last_name(src))
        #     index += 1

    def get_elements(self):
        els = self.driver.find_elements_by_css_selector("*")
        elements = []
        flag = True
        for el in els:
            tg_name = el.tag_name
            if tg_name == "body":
                flag = False
            if flag or tg_name in ["br","hr"]:
                continue
            temp = {tg_name: []}
            xp = self.driver.execute_script("""gPt=function(c){
                                 if(c.id!==''){
                                     return'id("'+c.id+'")'
                                 } 
                                 if(c===document.body){
                                     return c.tagName
                                 }
                                 var a=0;
                                 var e=c.parentNode.childNodes;
                                 for(var b=0;b<e.length;b++){
                                     var d=e[b];
                                     if(d===c){
                                         return gPt(c.parentNode)+'/'+c.tagName+'['+(a+1)+']'
                                     }
                                     if(d.nodeType===1&&d.tagName===c.tagName){
                                         a++
                                     }
                                 }
                             };
                             return gPt(arguments[0]).toLowerCase();""", el)
            temp[tg_name].append("xpath=" + str(xp))

            attr = self.driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', el)
            i = 0
            for key,val in attr.items():
                if i == 2:
                    break
                one_attr = str(key) + "=" + str(val)
                temp[tg_name].append(one_attr)
                i += 1
            elements.append(temp)
        return elements

    def get_tables(self):
        tables = self.driver.find_elements_by_tag_name("table")
        tbs = []
        for table in tables:
            xp = self.driver.execute_script("""gPt=function(c){
                                 if(c.id!==''){
                                     return'id("'+c.id+'")'
                                 } 
                                 if(c===document.body){
                                     return c.tagName
                                 }
                                 var a=0;
                                 var e=c.parentNode.childNodes;
                                 for(var b=0;b<e.length;b++){
                                     var d=e[b];
                                     if(d===c){
                                         return gPt(c.parentNode)+'/'+c.tagName+'['+(a+1)+']'
                                     }
                                     if(d.nodeType===1&&d.tagName===c.tagName){
                                         a++
                                     }
                                 }
                             };
                             return gPt(arguments[0]).toLowerCase();""", table)
            tbs.append(["xpath=" + xp, "rows:4", "columns:3"])

        tbr = []
        for x in tbs:
            tbr.append({"table": x})

        return tbr



if __name__ == "__main__":
    url = sys.argv[1]
    domain = sys.argv[2]
    obj = Webpage(url, domain)
    tables = obj.get_tables()
    images = obj.get_images()
    elements = obj.get_elements()
    links = []
    for x in elements:
        if "a" in x.keys():
            links.append(x)

    result = dict()

    result["elements"] = elements
    result["tables"] = tables
    result["images"] = images
    result["links"] = links
    result["others"] = []

    print(json.dumps(result))
    