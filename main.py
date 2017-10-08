from scraper.sunbiz import link_extract

def main():
    """
    passes the sunbiz URL to the link extract function
    and returns active businesses to the database. 
    """

    link = 'http://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults?InquiryType=' \
           'EntityName&inquiryDirectionType=ForwardList&searchNameOrder=9XDATASERVICES%20M130000030960&' \
           'SearchTerm=a&entityId=M13000003096&listNameOrder=9VIRTUOUSWOMEN%20P030001044920'

    link_extract(link)


if __name__ == "__main__":
    # runs the main function
    main()
