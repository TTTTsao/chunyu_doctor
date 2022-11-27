from bs4 import BeautifulSoup

def is_404(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        # doctor detail info is deleted
        if '抱歉，你所访问的网页不存在了，请返回主页' in html:
            print("404")
            return True
        elif html == '':
            return True
        else:
            return False
    except AttributeError:
        return False

