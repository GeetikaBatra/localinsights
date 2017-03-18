import re
from bs4 import BeautifulSoup            
from scraper import Scraper
import sys, getopt

to_date =""
# we initialise a bot tahema that will have run the parsing functions
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv,"t:f:")
except getopt.GetoptError:
    print 'county.py -f <fromdate> -t <todate>'
    sys.exit(2)
for opt, arg in opts:
    if opt == '-f':
        from_date = arg
    if opt == '-t':
        to_date = arg

domain = "http://www.criis.com/cgi-bin/new_get_recorded.cgi"
params= """DOC_TYPE=000&doc_dateA={from_date}&doc_dateB={to_date}&SEARCH_TYPE=DOCTYPE&OLD_DOCTYPE=&OLD_DOCMULTI=&COUNTY=fresno&YEARSEGMENT=current&ORDER_TYPE=Recorded+Official&LAST_RECORD=1&SCREENRETURN=doc_search.cgi&SCREEN_RETURN_NAME=Recorded+Document+Search""".format(from_date=from_date,to_date=to_date)
# we put the parameters that a domain will need to land to the next page along
# with the page details
county = Scraper("county", start_date="1/1/2015", end_date="1/2/201")
county_args = {
    
    "page1": {
        "url": "{domain}?{params}".format(domain=domain, params=params)
}
}



@county.scrape(county_args["page1"]["url"])
def parse_page1():
    # We have the source of the page, let's ask BeaultifulSoup to parse it for
    # the bot
    soup = BeautifulSoup(county.response.text, "html.parser")
    # to do: write the remaining of the functions
    # look into https://gist.github.com/phillipsm/0ed98b2585f0ada5a769
    records= []
    for body_row in soup.select("table.records"):
        

        cells = body_row.findAll('tr')
        
        for cell in cells[8:]:
            table_row = cell.findAll('td')
            temp_row = []
            for each in table_row:
                if each.text == 'Show Detail':
                    temp_row.append((each.a["href"]).encode('utf-8'))
                else:
                    temp_row.append((each.text).encode('utf-8'))
            records.append(temp_row)

    for rec in records:  
        elem = dict(zip(county.headers, rec))
        yield elem   
            

# put the functions in a list where the sequence should be in the order that you
# want the bot to crawl through the pages
parse_functions = [parse_page1]
# define the headers for the csv file that will be generated
county.headers = ["Detail Link",
                  "Record Date",
                  "Document",
                  "Doc Type",
                  "GrantoR/E",
                  "Name"]


if __name__ == "__main__":
   
    county.run(parse_functions)
