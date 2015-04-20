import mechanize, urllib2
from bs4 import BeautifulSoup

url = "http://foodscores.state.al.us/(S(bcxxpt55pb2zrt45ki3yef55))/Default.aspx"

def mech():
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders =  [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.open(url)
    br.select_form(nr=0)
    states = br.form.controls[8].possible_items()
    br.form.set(True, states[1], br.form.controls[8].name)
    resp2 = br.submit()
    print resp2.read()

if __name__ == "__main__":
    mech()
    pass