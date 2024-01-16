from bs4 import BeautifulSoup
import urllib.parse
import urllib.request

def search_tags ( tag_list ):
    for x in tag_list:
        x.number_of_results = scrape_results( x.name )
    return tag_list

""" Abstracted scraper """
def scrape_results ( query ):
    html_to_scrape = get_html ( query )
    number_of_searches = scrape_html( html_to_scrape )
    return number_of_searches

""" Determine if bing will produce the number of results, if not search google then return html version 
    of the page """
def get_html ( query ):
    encoded_query = urllib.parse.quote_plus(query)
    bing_address = "http://www.bing.com/search?q=%s" %  encoded_query
    google_address = "http://www.google.com/search?q=%s" %  encoded_query

    if check_for_results( bing_address ) :
        getRequest = urllib.request.Request( bing_address, None, {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'} )

        urlfile = urllib.request.urlopen(getRequest)
        htmlResult = urlfile.read( 200000 )
        urlfile.close()
        return htmlResult
    else:
        getRequest = urllib.request.Request( google_address, None, {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'} )

        urlfile = urllib.request.urlopen(getRequest)
        htmlResult = urlfile.read( 200000 )
        urlfile.close()
        return htmlResult

""" Check if the total number of results exists in the given html file"""
def check_for_results ( address ):
    testGetRequest = urllib.request.Request( address, None, {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0'} )
    testFile = urllib.request.urlopen( testGetRequest )
    html_to_check = testFile.read( 200000 )

    number_of_searches = scrape_html( html_to_check )

    #if number_of_searches.isdigit() :
    #    return True
    #else:
    #    return False
    try:
        int(number_of_searches)
    except TypeError:
        return False
    except ValueError:
        return False
    else:
        return True

""" Scrape the given html file for the number of results """
def scrape_html ( html_to_scrape) :
    soup = BeautifulSoup( html_to_scrape, 'lxml' )
    resultStatsList = None
    if soup.find( 'div', { 'id': 'b_tween' } ):
        rawResultStats = soup.find( 'div', { 'id': 'b_tween' } ).text
        resultStatsList = rawResultStats.split()
        resultStatsList = str(resultStatsList[0]).replace(',','')
        return resultStatsList
    else:
        return resultStatsList

def get_map_url(tag_list):
    google_maps_base_url = "https://www.google.com/maps/search/"
    temp_tag_list = tag_list
    if len(temp_tag_list) > 0:
        for tag in temp_tag_list:
            if tag.tag_one != 0 and tag.tag_two != 0:
                encoded_query = urllib.parse.quote_plus(tag.dominant_tag().name)
                tag.map_url = google_maps_base_url + encoded_query
            else:
                encoded_query = urllib.parse.quote_plus(tag.name)
                tag.map_url = google_maps_base_url + encoded_query
    tag_list = temp_tag_list

    return tag_list


