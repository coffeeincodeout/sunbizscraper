import requests
import lxml.html
import itertools
import datetime
import re
from scraper.Database import Database


def link_extract(url_enter):
    # download and parse page
    base_url = 'http://search.sunbiz.org'
    sunbiz_url = url_enter
    last_page = "http://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults?InquiryType=" \
                "EntityName&inquiryDirectionType=ForwardList&searchNameOrder=9XDATASERVICES%20M130000030960&" \
                "SearchTerm=a&entityId=M13000003096&listNameOrder=9VIRTUOUSWOMEN%20P030001044920"
    while True:
        user_login = "dbname='buzpro_db' user='root' host='localhost' password='motifes6'"
        db = Database()
        db.connection(user_login)
        db.cursor()
        page_html = requests.get(sunbiz_url)  # Turns HTML to text for scraping
        data = lxml.html.fromstring(page_html.text)
        # parser for page
        status = data.xpath('//*[@id="search-results"]/table/tbody/tr/td[@class="small-width"]/text()')
        active_link = data.xpath('//*[@id="search-results"]/table/tbody/tr/td[@class="large-width"]/a/@href')

        # gets URL for the following page
        next_page_link = data.xpath(
            '//*[@id="maincontent"]/div[3]/div[1]/span[2]/a/@href')  # if next page equals none break
        for next_page in next_page_link:
            sunbiz_url = base_url + next_page

        if sunbiz_url == last_page:
            break

        # Loops through all the companies on a page
        for stat, link in itertools.zip_longest(status, active_link):
            if stat == 'Active':  # return active_company_link_list
                # returns the data in list format
                company_profile_url = base_url + link
                profile_link_get = requests.get(company_profile_url)
                company_profile_data = lxml.html.fromstring(profile_link_get.text)
                company_type = company_profile_data.xpath('//*[@id="maincontent"]/div[2]/div[1]/p[1]/text()')
                company_name = company_profile_data.xpath('//*[@id="maincontent"]/div[2]/div[1]/p[2]/text()')
                agent_name = company_profile_data.xpath('//*[@id="maincontent"]/div[2]/div[5]/span[2]/text()')
                date_filed = company_profile_data.xpath(
                    '//*[@id="maincontent"]/div[2]/div[2]/span[2]/div/span[3]/text()')
                address = company_profile_data.xpath('//*[@id="maincontent"]/div[2]/div[3]/span[2]/div/text()[1]')
                city_state_zip = company_profile_data.xpath(
                    '//*[@id="maincontent"]/div[2]/div[3]/span[2]/div/text()[2]')
                address_additional = company_profile_data.xpath(
                    '//*[@id="maincontent"]/div[2]/div[3]/span[2]/div/text()[3]')
                # Pattern matches for city, state and zip
                pattern = re.compile(r'([A-Z]\w+\s[A-Z]\w+|[A-Z]\w+), ([A-Z]{2}) (\d{5}$)')
                # Loops through the list of data
                for c_type, c_name, a_name, c_date, address, cityStateZip, add2 in itertools.zip_longest(
                        company_type, company_name, agent_name, date_filed, address,
                        city_state_zip, address_additional):
                    # pattern matches and converts to string
                    csz = pattern.search(str(cityStateZip))
                    csz2 = pattern.search(str(add2))
                    try:
                        # Connect to Database
                        date = datetime.datetime.strptime(c_date.strip(), '%m/%d/%Y').date()
                        if add2.isspace() is True and csz is not None:
                            db.insert(c_type.strip(), a_name.strip(), c_name.strip(), date.strftime("%m/%d/%Y"),
                                      address.strip(), csz.group(1), csz.group(2), csz.group(3))
                            db.commit()

                        elif add2.isspace() is not True and csz2 is not None:
                            db.insert(c_type.strip(), a_name.strip(), c_name.strip(), date.strftime("%m/%d/%Y"),
                                      address.strip(), csz2.group(1), csz2.group(2), csz2.group(3))
                            db.commit()

                    except Exception as e:
                        print(e)
        # closes database once done
        db.close()


# TODO: setup scheduler so the script runs automatically
# TODO: build script that checks if item already exists
