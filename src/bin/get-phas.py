#!/usr/bin/env python

import webbrowser
import urllib
import urllib2
import os
import sys
import time

# PLEASE RUN THIS WITH https://pic.hud.gov/pic/haprofiles/haprofilelist.asp instead of pictest

states = ['AK', 'AL', 'AR', 'AS', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'GU', 'HI', 'IA', 'ID', 'IL', 'IN',
          'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MH', 'MI', 'MN', 'MO', 'MP', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ',
          'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'PW', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VI', 'VT',
          'WA', 'WI', 'WV', 'WY']

# print states[49:]
# exit()

def format(s):
    s = s.replace("'", '').strip().upper()
    s = s.replace('&NBSP;', ' ')
    return s


APP_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))

sys.path.append(APP_DIR)
PHA_LOCATOR_DIR = os.path.join(os.path.dirname(APP_DIR), 'pha_locator/')
sys.path.append(PHA_LOCATOR_DIR)
#
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pha_locator.settings')

import django

django.setup()

from pha_locator.apps.phas.models import Pha


def get_page(url, data, headers):
    while True:
        try:
            req = urllib2.Request(url, data, headers, True)
            response = urllib2.urlopen(req)
            page = response.read()
            return req, response, page
        except Exception as E:
            print('Exception', E, 'Waiting 15 seconds to re-try')
            time.sleep(15)


class Scraper:
    def __init__(self):
        self.housingAuths = []
        self.cookie = None

    def retrieve_page(self, action, state, hacode, haname, pageno=1):
        url = 'https://pictest.hud.gov/pictest/haprofiles/haprofilelist.asp'
        values = {
            'StateList': state,
            'ViewList': 'State',
            'lstActivity': 'y',
            'lstProgramType': 'ALL',
            'lstSize': 'ALL',
            'optSearch': '1',
            'sizearray': "EL+Extra Large (10,000+);L+Large (1,250 - 9999);MH+Medium High (500 - 1,249);ML+Medium Low (250 - 499);S+Small (50 - 249);VS+Very Small (1 - 49);",
            'strLevel1Label': '',
            'txtAction': action,
            'txtPageNum': str(pageno),
            'txtSearch': '',
            'txtSearchtype': 'RetrieveBtn',
            'txtStrSort': '1',
            'txtTotalPages': str(pageno),
            'txthacode': hacode,
            'txthaname': haname,
        }

        user_agent = 'User-Agent	Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'
        if action == 'HAProfileDetails' or action == 'NxtPrev':
            referer = 'https://pictest.hud.gov/pictest/haprofiles/haprofilelist.asp'
        else:
            referer = 'http://www.google.com/search?q=haprofile+list&ie=utf-8&oe=utf-8&aq=t&rls=org.mozilla:en-US:official&client=firefox-a'
        cookie = self.cookie

        headers = {
            'User-Agent': user_agent,
            'Host': 'pictest.hud.gov',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
            'Connection': 'keep-alive',
            'Referer': referer,
            'Cookie': cookie

        }
        data = urllib.urlencode(values)

        req, response, page = get_page(url, data, headers)

        if self.cookie is None:
            self.cookie = response.headers['set-cookie']

        if action in ['RetrieveSelectedState', 'RetrieveBtn']:
            phas = self.process_list_page(page, state)
            for ha in phas:
                ha_code, ha_name = format(ha[1][0]), format(ha[1][1])
                # if ha_code <= 'IL025':
                # if ha_code <= 'LA075':
                # if ha_code <= 'MA099':
                # if ha_code <= 'MI026':
                # if ha_code <= 'NE106':
                if ha_code <= 'TX535':
                    continue
                (ph, s8) = self.retrieve_page('HAProfileDetails', state, ha_code, ha_name)
                address = self.retrieve_address(state, ha_code, ha_name)
                contact = self.retrieve_contact(state, ha_code, ha_name)
                print state, ha, ph, s8
                pha = Pha.objects.filter(code=ha_code).first()
                if not pha:
                    pha = Pha(state=state, code=ha_code, name=ha_name)
                pha.city = format(ha[1][2])
                pha.program = format(ha[1][3])
                pha.low_rent_units = ph
                pha.section8_units = s8
                pha.line1 = address['line1']
                pha.line2 = address['line2']
                pha.county = address['county']
                pha.zip_code = address['zip']
                pha.phone_number = format(contact['phone'])
                pha.fax_number = contact['fax']
                pha.TTY_Number = contact['tty']
                pha.web_page_address = contact['website']
                pha.email_address = contact['email']
                pha.mayor = ''
                pha.board_chairperson = contact['chairman']
                pha.executive_director = contact['director']
                pha.HUD_field_office = contact['hud']

                pha.save()
            if page.find("""onMouseOver="window.status='Retrieve Next'; return true""") > 0:
                # self.show_in_browser(page)
                self.retrieve_page('RetrieveBtn', state, '', '', pageno + 1)
        else:
            return self.process_detail_page(page)

    def retrieve_address(self, state, code, name):
        url = 'https://pictest.hud.gov/pictest/haprofiles/haprofileaddress.asp'
        values = {
            'StateList': state,
            'ViewList': 'State',
            'lstActivity': 'y',
            'lstProgramType': 'ALL',
            'lstSize': 'ALL',
            'optSearch': '1',
            'sizearray': "EL+Extra Large (10,000+);L+Large (1,250 - 9999);MH+Medium High (500 - 1,249);ML+Medium Low (250 - 499);S+Small (50 - 249);VS+Very Small (1 - 49);",
            'strLevel1Label': '',
            'txtAction': '',
            'txtPageNum': '1',
            'txtSearch': '',
            'txtSearchtype': 'RetrieveBtn',
            'txtStrSort': '1',
            'txtTotalPages': '1',
            'txthacode': code,
            'txthaname': name,
        }

        user_agent = 'User-Agent	Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'
        referer = 'https://pictest.hud.gov/pictest/haprofiles/haprofiledetails.asp'

        headers = {
            'User-Agent': user_agent,
            'Host': 'pictest.hud.gov',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
            'Connection': 'keep-alive',
            'Referer': referer,
            'Cookie': self.cookie
        }

        data = urllib.urlencode(values)
        req, response, page = get_page(url, data, headers)
        # self.show_in_browser(page, 'address.html')

        return self.get_address(page)

    def retrieve_contact(self, state, code, name):
        url = 'https://pictest.hud.gov/pictest/haprofiles/haprofilecontact.asp'
        values = {
            'StateList': state,
            'ViewList': 'State',
            'lstActivity': 'y',
            'lstProgramType': 'ALL',
            'lstSize': 'ALL',
            'optSearch': '1',
            'sizearray': "EL+Extra Large (10,000+);L+Large (1,250 - 9999);MH+Medium High (500 - 1,249);ML+Medium Low (250 - 499);S+Small (50 - 249);VS+Very Small (1 - 49);",
            'strLevel1Label': '',
            'txtAction': '',
            'txtPageNum': '1',
            'txtSearch': '',
            'txtSearchtype': 'RetrieveBtn',
            'txtStrSort': '1',
            'txtTotalPages': '1',
            'txthacode': code,
            'txthaname': name,
        }

        user_agent = 'User-Agent	Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'
        referer = 'https://pictest.hud.gov/pictest/haprofiles/haprofiledetails.asp'
        cookie = self.cookie

        headers = {
            'User-Agent': user_agent,
            'Host': 'pictest.hud.gov',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
            'Connection': 'keep-alive',
            'Referer': referer,
            'Cookie': cookie
        }

        data = urllib.urlencode(values)
        req, response, page = get_page(url, data, headers)
        # self.show_in_browser(page, 'contact.html')
        return self.get_contact(page)

    @staticmethod
    def process_detail_page(page):
        # self.show_in_browser(page)
        details = page
        ph, s8 = 0, 0
        try:
            i = details.find('<TD width="33%">Total</TD>')
            if i > -1:
                details = details[i + len('<TD width="33%">Total</TD>'):]
                # i = details.find('">')
                j = details.find('</TD>')
                details = details[j + 5:]
                i = details.find('">')
                j = details.find('</TD>')
                ph = int(details[i + 2:j].replace(',', ''))

            i = details.find('<TD width="50%"><B><FONT COLOR = "#FFFFFF">Units</FONT></B></TD>')
            if i > 0:
                details = details[i + len('<TD width="50%"><B><FONT COLOR = "#FFFFFF">Units</FONT></B></TD>'):]
                i = details.find('</TD>')
                details = details[i + 5:i + 65]
                i = details.find('">')
                j = details.find('</TD>')
                s8 = int(details[i + 2:j].replace(',', ''))
        except:
            pass

        return ph, s8

    def process_list_page(self, page, state):

        page = page.replace("/pictest/haprofiles/haprofiledetails.asp",
                            "https://pictest.hud.gov/pictest/haprofiles/haprofiledetails.asp")
        page = page.replace('<A HREF="haprofiledetails.asp"',
                            '<A HREF="https://pictest.hud.gov/pictest/haprofiles/haprofiledetails.asp"')
        page = page.replace('<A href="haprofilelist.asp"',
                            '<A HREF="https://pictest.hud.gov/pictest/haprofiles/haprofiledetails.asp"')
        page = page.replace('<A HREF="haprofilelist.asp"',
                            '<A HREF="https://pictest.hud.gov/pictest/haprofiles/haprofilelist.asp""')

        start = """<A HREF="javascript:GetProfileDetails('HAProfileDetails', '""" + state
        whole_info = []
        i = page.find(start)
        if i > 0:
            page = page[i:]
            # print page

            phas = self.get_info(page)
            whole_info = []
            for ha in phas:
                # print state, ha
                whole_info.append((state, ha))

        # self.show_in_browser(page)
        return whole_info

    @staticmethod
    def show_in_browser(page, filename):
        filename = os.path.join(APP_DIR, filename)
        f = open(filename, 'w')
        f.write(page)
        f.close()
        url = "file://" + filename
        webbrowser.open(url)

    @staticmethod
    def get_info(txt):
        phas = []
        js = """<A HREF="javascript:GetProfileDetails('HAProfileDetails', '"""
        start = txt.find(js)
        while start > -1:
            txt = txt[start + len(js):]
            code = txt[:5]

            txt = txt[8:]
            i = txt.find("')")
            name = txt[:i]

            txt = txt[i:]
            i = txt.find('<TD ALIGN = "Center" WIDTH = "10%">')
            txt = txt[i + len('<TD ALIGN = "Center" WIDTH = "10%">'):]
            i = txt.find('</TD>')
            city = txt[:i].upper()
            txt = txt[i:]

            txt = txt[i:]
            i = txt.find('<TD ALIGN = "Center" WIDTH = "15%">')
            txt = txt[i + len('<TD ALIGN = "Center" WIDTH = "15%">'):]
            i = txt.find('</TD>')
            program = txt[:i]
            if program == 'COMBINED':
                program = 'L;S8'
            elif program == 'Low-Rent':
                program = 'L'
            else:
                program = 'S8'
            txt = txt[i:]

            phas.append((code, name, city, program))
            start = txt.find(js)
        return phas

    @staticmethod
    def get_field_address(addr, name):
        i = addr.find(name + ':')
        addr = addr[i:]
        i = addr.find('size="2">') + len('size="2">')
        j = addr.find('</FONT></STRONG>')
        field = addr[i:j].strip()
        addr = addr[j:]
        return field, addr

    def get_address(self, addr):
        line1, addr = self.get_field_address(addr, 'Address Line 1')
        line2, addr = self.get_field_address(addr, 'Address Line 2')
        city, addr = self.get_field_address(addr, 'City/Locality')
        county, addr = self.get_field_address(addr, 'County Name')
        state, addr = self.get_field_address(addr, 'State')
        zipcode, addr = self.get_field_address(addr, 'Zip Code')
        return {
            'line1': line1.strip(),
            'line2': line2.strip(),
            'city': city.strip(),
            'county': county.strip(),
            'state': state,
            'zip': zipcode.strip()
        }

    @staticmethod
    def get_field_contact(addr, name, color):
        i = addr.find(name + ':') + len(name + ':')
        addr = addr[i:]
        template = 'color=%s><B>' % (color,)
        i = addr.find(template) + len(template)
        j = addr.find('</FONT></B>')
        aux = addr.find(':')
        if aux == addr.find('://'):
            rest = addr[aux + 2:]
            aux = aux + rest.find(':')

        if (aux > -1) and (aux < j) and (addr.find('mailto:') + len('mailto') != aux):
            field = ''
        else:
            field = addr[i:j].strip()
            addr = addr[j:]

        return field, addr

    def get_contact(self, contact):

        phone, contact = self.get_field_contact(contact, 'Phone Number', '#330066')
        fax, contact = self.get_field_contact(contact, 'Fax Number', '#330066')
        tty, contact = self.get_field_contact(contact, 'TTY Number', '#330066')
        website, contact = self.get_field_contact(contact, 'Web Page Address', '"#0000ff"')
        email, contact = self.get_field_contact(contact, 'Email Address', '"#0000ff"')
        mayor, contact = self.get_field_contact(contact, 'Mayor', '#330066')
        chairman, contact = self.get_field_contact(contact, 'Board Chairperson', '#330066')

        director, contact = self.get_field_contact(contact, 'Executive Director', '#330066')
        hud, contact = self.get_field_contact(contact, 'HUD Field Office', '#330066')

        return {
            'phone': phone,
            'fax': fax,
            'tty': tty,
            'website': website,
            'email': email,
            'chairman': chairman,
            'director': director,
            'hud': hud
        }


def fix_phones():
    for pha in Pha.objects.all():
        if 'NBSP' in pha.phone_number:
            pha.phone_number = format(pha.phone_number)
        pha.save()


def main():
    scraper = Scraper()
    # Pha.objects.all().delete()
    # fix_phones()
    for state in states[49:]:
        scraper.retrieve_page('RetrieveSelectedState', state, '', '', 1)


def main1():
    # import requests
    data = {
        'txthacode': 'AK001',
        'txthaname': 'AK001 AHFC - MTW PH',
        'action': 'HAProfileDetails',
    }
    headers = {
        'Host': 'pictest.hud.gov',
        'Connection': 'keep-alive',
        'Origin': 'https://pictest.hud.gov',
        'Upgrade-Insecure-Requests': '1',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://pictest.hud.gov/pictest/haprofiles/haprofilelist.asp',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.8,es;q=0.6',
        'cookie': '_ga=GA1.2.1498132217.1508859127; ASPSESSIONIDQERCCTQA=MPCOONFDBAJPEAILOIKEBLFB; ASPSESSIONIDQGTBCTRA=AAHBPJCAPFBDJCLHKEHKOPFF'
    }
    resp = requests.post('https://pictest.hud.gov/pictest/haprofiles/haprofiledetails.asp', data=data, headers=headers)
    print resp.status_code

    Scraper().show_in_browser(resp.content, 'details.html')


if __name__ == '__main__':
    main()
