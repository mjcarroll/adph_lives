import mechanize, urllib2
from bs4 import BeautifulSoup

url = "http://foodscores.state.al.us/(S(bcxxpt55pb2zrt45ki3yef55))/Default.aspx"

def prep():
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders =  [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.open(url)
    br.select_form(nr=0)
    return br

def find_counties_types():
    br = prep()
    type_control = br.form.find_control(name="ctl00$ContentPlaceHolder1$DrpEstdType")
    county_control = br.form.find_control(name="ctl00$ContentPlaceHolder1$DrpCnty")
    counties = {}
    for county in county_control.items:
        if not county.attrs.has_key('selected'):
            counties[ county.attrs['contents'] ] = county.attrs['value']
    types = {}
    for typ in type_control.items:
        if not typ.attrs.has_key('selected'):
            types[ typ.attrs['contents'] ] = typ.attrs['value']
    return (types, counties)

def parse_entry(tr):
    spans = tr.find_all("span")
    data = []
    for s in spans:
        data.append(s.text)
    links = tr.find_all("a", target="_blank")
    for a in links:
        data.append(a.text)
    return (data, tr.find_next_sibling())

def parse_entries(tr):
    data = []
    while tr != None:
        (dd, tr) = parse_entry(tr)
        data.append(dd)
    return data

def get_establishments( county, estab_type ):
    br = prep()
    type_control = br.form.find_control(name="ctl00$ContentPlaceHolder1$DrpEstdType")
    county_control = br.form.find_control(name="ctl00$ContentPlaceHolder1$DrpCnty")
    br.form.set(True, county, county_control.name)
    br.form.set(True, estab_type, type_control.name)
    resp = br.submit()
    soup = BeautifulSoup(resp)
    tt = soup.find(id="ctl00_ContentPlaceHolder1_DtList")
    if tt is None:
        return None
    else:
        return parse_entries(tt.find("tr"))

if __name__=="__main__":
    (tt, cc) = find_counties_types()

    for (k,v) in tt.iteritems():
        print v
        data = get_establishments(cc['MADISON'], v)
        if data is None:
            continue

        f = open(v + '.txt', 'w')
        for d in data:
            f.write(', '.join([d[0].encode("utf8"), d[1].encode("utf8"),
                               str(int(d[2].strip('-'))), str(int(d[3])), d[4].encode("utf8"),
                               d[5].encode("utf8"), d[6].encode("utf8")]))
            f.write('\n')