def location_bias_gsearch(query, location):
    query = re.sub(r"\s+", '-', query)
    # print('query: ', query)
    geolocator = Nominatim(user_agent = 'myapplication')
    location = geolocator.geocode(location)
    # print('lat, long: ', (location.latitude, location.longitude))
    address = []
    address.append('https://maps.googleapis.com/maps/api/place/autocomplete/xml?input=')
    address.append(query)
    address.append('&types=establishment&location=')
    address.append(str(location.latitude))
    address.append(',')
    address.append(str(location.longitude))
    address.append('&radius=5000&strictbounds&key=') # radius is currently 3 miles
    address.append(GOOGLE_SEARCH_API_KEY)
    s = ''.join(address)
    print(s)
    request = urllib2.Request(s, None, {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})
    urlfile = urllib2.urlopen(request)
    page = urlfile.read()
    soup = BeautifulSoup(page)
    print('soup: ', soup)
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    print('links: ', links)

def get_maps_address(place_id):
    url = 'https://www.google.com/maps/search/?api=1&query=Google&query_place_id=' + place_id
    return url

def get_phone_number(url):
    page = get_soup(url)
    page_text = page.get_text()
    phone_nums = list(set(re.findall(PHONE_REGEX, page_text)))
    phone_nums = [re.sub("[^0-9]", "", num) for num in phone_nums]
    return phone_nums


def get_yelp_phone_number(url):
    page = get_soup(url)
    phone_dom_element = page.select(YELP_PHONE_DOM_REGEX)
    phone_dom_element = str(phone_dom_element)
    phone = re.sub("[^0-9]", "", phone_dom_element)
    return phone

def get_phone_from_listing(urls_with_listings):
    phones = []
    for url in urls_with_listings:
        phones.extend(get_phone_number(url))
    phones = list(dict.fromkeys(phones))
    return phones
