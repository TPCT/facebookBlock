import csv
class block:
    def __init__(self, username, password):
        import werkzeug
        werkzeug.cached_property = werkzeug.utils.cached_property
        from robobrowser import RoboBrowser
        from requests import Session
        from warnings import simplefilter
        simplefilter('ignore', UserWarning)
        self.username = username
        self.password = password
        self.browser = RoboBrowser
        self.Session = Session
        self.userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
        self.Browser = None
        self.session = None
        self.login()
        self.friend_list_gen()

    def login(self):
        self.session = self.Session()
        headers = '''Host: m.facebook.com
                     User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0
                     Accept-Language: en-US,en;q=0.5
                     Connection: keep-alive
                     TE: Trailers'''
        for header in headers.split('\n'):
            header = header.split(': ')
            self.session.headers[header[0].strip()] = header[1].strip()
        self.Browser = self.browser(session=self.session,
                                    user_agent=self.userAgent,
                                    cache=True)
        self.Browser.open('https://m.facebook.com/login')
        loginForm = self.Browser.get_form('login_form')
        loginForm['email'].value = self.username
        loginForm['pass'].value = self.password
        self.Browser.submit_form(loginForm, submit=loginForm['login'])
        self.Browser.open('https://m.facebook.com/login/save-device/cancel/'
                          '?flow=interstitial_nux&nux_source=regular_login')
        if self.Browser.get_form('mbasic-composer-form'):
            self.Browser.open('https://m.facebook.com/profile.php')
            return True
        return False

    def friend_list_gen(self):
        Friends = list()
        checked = list()
        self.Browser.open(
            'https://m.facebook.com/friends/center/friends/?fb_ref=fbm&ref_component=mbasic_bookmark&ref_page=XMenuController')
        with open('accounts.txt', 'a+') as csv_file:
            csv_file.seek(0)
            reader = csv.reader(csv_file, delimiter=',')
            for row in reader:
                checked.append('->'.join(row))
            while '/friends/center/friends/?ppk=' in str(self.Browser.parsed):
                for x in self.Browser.find_all('a'):
                    if '/friends/center/friends/?ppk=' in x['href']:
                        for friend in Friends:
                            try:
                                friend = friend.split('->')
                                print('Blocking', friend[0])
                                self.Browser.open(friend[1])
                                blockForm = self.Browser.get_forms()[1]
                                self.Browser.submit_form(blockForm, submit=blockForm['confirmed'])
                            except:
                                pass
                        Friends = list()
                        self.Browser.open('https://m.facebook.com' + x['href'])
                        break
                    elif '/friends/hovercard/mbasic/?uid=' in x['href']:
                        data = x.text, x['href'].split('uid=')[1].split('&')[0]
                        if '->'.join(data) not in checked:
                            print(data[0], 'https://m.facebook.com/messages/read/?fbid=' + data[1], sep='\n')
                            block = input('do you want to block this account')
                            print('-' * 50)
                            if block:
                                Friends.append(data[0] + '->https://m.facebook.com/privacy/touch/block/confirm/?bid=' + data[1])
                            else:
                                dataWriter = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                                dataWriter.writerow(data)
                                checked.append('->'.join(data))
