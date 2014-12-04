import scrapy
from scrapy.http.cookies import CookieJar
from scrapy.shell import inspect_response
from pprint import pprint
import urllib
import urlparse
import json
from zoho.items import Contact, EmailRecord, Note
from scrapy.exceptions import CloseSpider
import re

class zapper(scrapy.Spider):
    name = "zoho"
    allowed_domains = ["crm.zoho.com", "accounts.zoho.com"]
    start_urls = [
            #"https://crm.zoho.com/crm/ShowTab.do?module=Contacts",
            "https://crm.zoho.com/crm/ShowDetails.do?module=Contacts&toolTip=Home&isload=true",
    ]


    def start_requests(self):
        return [
            scrapy.Request(
                #"https://www.zoho.com/crm/lp/login.html",
                "https://accounts.zoho.com/login?servicename=ZohoCRM&serviceurl=/crm/ShowHomePage.do&hide_signup=true&css=https://www.zoho.com/css/plogin.css",
                callback=self.do_login
                )
        ]

    def do_login(self, response):
        # extract csrf token
        cookiejar = response.meta.setdefault('cookie_jar', CookieJar())
        cookiejar.extract_cookies(response, response.request)
        iamcsr = cookiejar._cookies['accounts.zoho.com']['/']['iamcsr'].value
        iamcsroo = urllib.quote(iamcsr.encode("utf-8"))
        return [
                scrapy.FormRequest(
                    "https://accounts.zoho.com/login?servicename=ZohoCRM&serviceurl=/crm/ShowHomePage.do&hide_signup=true&css=https://www.zoho.com/css/plogin.css",
                    formdata={
                        'LOGIN_ID': 'hef+zohobot@pbrfrat.com',
                        'PASSWORD': 'phe8suz4hahzeep4Eeng3taeXiephee2',
                        'IS_AJAX': 'false',
                        'remember': '-1',
                        'iamcsrcoo': iamcsroo
                    },
                    callback=self.start_requests_after_login,
                )
        ]

    def start_requests_after_login(self, response):
        url = "https://crm.zoho.com/crm/ShowDetails.do?module=Contacts&toolTip=Home&isload=true"
        yield scrapy.Request(url, callback=self.parse_cvid)


    def parse_cvid(self, response):
        cvid = response.xpath('//input[@id="cvid"]/@value').extract()[0]
        url = "https://crm.zoho.com/crm/RecordsCount.do?step=step2&cvId={}&module=Contacts".format(cvid)

        # This contains the first contact page, so parse it
        self.log("starting to call other")
        for i in self.parse_contact_list(response):
            yield i
        self.log("ending to call other")

        # and use the cvid to get the total pages
        request = scrapy.Request(url, callback=self.parse_total_count)
        request.meta['cvid'] = cvid
        yield request

    def parse_total_count(self, response):
        count = int(response.body)
        cvid = response.meta['cvid']

        # starting at 101 since 1-100 should already be handled in parse_cvid
        for start in xrange(101,count,100):
            params = {}
            params['module'] = 'Contacts'
            params['fromIndex'] = start
            params['nav'] = 'true'
            params['fromListView'] = 'true'
            params['fromApproval'] = 'false'
            params['massActions'] = 'false'
            params['cvid'] = cvid
            params['currentOption'] = '100'
            params['OnSelect'] = 'true'
            params['toIndex'] = start + 99
            params['rangeValue'] = '100'
            params['previous_sort_order'] = 'sort_desc'
            params['previous_sort_column'] = 'CONTACTID'
            params['toolTip'] = 'Contacts'
            params['isFromBack'] = 'true'
            params['fileName'] = '/crm/ShowSelectedCustomView.do'
            params['mod'] = 'true'
            params['isload'] = 'true'
            param_string = urllib.urlencode(params)
            url = "https://crm.zoho.com/crm/NavigateByRecords.do?" + param_string
            yield scrapy.Request(url, callback=self.parse_contact_list)

    def parse(self, response):
        self.log("default parse")
        raise CloseSpider("shouldn't get here")

    def parse_contact_list(self, response):
        #https://crm.zoho.com/crm/ShowEntityInfo.do?module=Contacts&lookback=true&id=794999000000074645&recordNum=1&toolTip=Search%20Results&pfrom=cv
        for extracted_data in response.xpath('//a[@data-cid="detailView"]/@data-params').extract():
            json_data = json.loads(extracted_data)
            contact_id = json_data['id']
            url = "https://crm.zoho.com/crm/ShowEntityInfo.do?module=Contacts&id={}".format(contact_id)
            yield scrapy.Request(url, callback=self.parse_contact_detail)
            
            # Get Email Lost
            for i in self.request_email_list(contact_id, 1):
                yield i

            # Collect notes
            # It appears that the max notes returned is (Idx + 10), so the
            # following line tries to get 1,000,010 notes
            # I do not know what the max the server will actually return is.
            url = "https://crm.zoho.com/jsp/common/getRelatedNotesForDetails.jsp?entityId={}&module=Contacts&tIdx=1000000".format(contact_id)
            request = scrapy.Request(url, callback=self.parse_notes)
            request.meta['contact_id'] = contact_id
            yield request
            
    def request_email_list(self, contact_id, start):
        # https://crm.zoho.com/crm/RelatedList.do?action=relatedlist&messageValue=null&module=Contacts&id=794999000000074645&cvid=null&recordNum=null&nav=false&neid=794999000000074645
        # https://crm.zoho.com/crm/NavigateByRecords.do?totalRecords=-1&fileName=/crm/RelatedList.do?action=relatedlist&previous_sort_column=null&previous_sort_order=null&module=Contacts&id=794999000000074645&mod_EMAILSPERSONALITY=true&toIndex=10&fromIndex=1&currentOption=10&next.x=x&pname=EMAILSPERSONALITY
        # https://crm.zoho.com/crm/NavigateByRecords.do?totalRecords=-1&fileName=/crm/RelatedList.do?action=relatedlist&previous_sort_column=null&previous_sort_order=null&module=Contacts&id=794999000000074645&mod_EMAILSPERSONALITY=true&toIndex=20&fromIndex=11&currentOption=10&next.x=x&pname=EMAILSPERSONALITY
        # https://crm.zoho.com/crm/NavigateByRecords.do?totalRecords=-1&fileName=/crm/RelatedList.do?action=relatedlist&previous_sort_column=null&previous_sort_order=null&module=Contacts&id=794999000000074645&mod_EMAILSPERSONALITY=true&toIndex=30&fromIndex=21&currentOption=10&next.x=x&pname=EMAILSPERSONALITY
        # https://crm.zoho.com/crm/NavigateByRecords.do?totalRecords=-1&fileName=/crm/RelatedList.do?action=relatedlist&previous_sort_column=null&previous_sort_order=null&module=Contacts&id=794999000000074645&mod_EMAILSPERSONALITY=true&toIndex=40&fromIndex=31&currentOption=10&next.x=x&pname=EMAILSPERSONALITY
        # https://crm.zoho.com/crm/NavigateByRecords.do?totalRecords=-1&fileName=/crm/RelatedList.do?action=relatedlist&previous_sort_column=null&previous_sort_order=null&module=Contacts&id=794999000000074477&mod_EMAILSPERSONALITY=true&toIndex=20&fromIndex=&currentOption=10&next.x=x&pname=EMAILSPERSONALITY

        # single page example: https://crm.zoho.com/crm/EntityInfo.do?module=Contacts&id=794999000000702049

        self.log("building request for {} starting at page {}".format(contact_id, start))

        if start == 1:
            url = "https://crm.zoho.com/crm/RelatedList.do"
            url += "?action=relatedlist"
            url += "&messageValue=null"
            url += "&module=Contacts"
            url += "&id={}".format(contact_id)
            url += "&cvid=null"
            url += "&recordNum=null"
            url += "&nav=false"
            url += "&neid={}".format(contact_id)
        else:
            url = "https://crm.zoho.com/crm/NavigateByRecords.do"
            url += "?totalRecords=-1"
            url += "&fileName=/crm/RelatedList.do"
            url += "?action=relatedlist"
            url += "&previous_sort_column=null"
            url += "&previous_sort_order=null"
            url += "&module=Contacts"
            url += "&id={}".format(contact_id)
            url += "&mod_EMAILSPERSONALITY=true"
            url += "&toIndex={}".format(start - 1)
            url += "&fromIndex={}".format(start - 10)
            url += "&currentOption=10"
            url += "&next.x=x"
            url += "&pname=EMAILSPERSONALITY"

        request = scrapy.Request(url, callback=self.parse_email_list)
        request.meta['contact_id'] = contact_id
        request.meta['start'] = start
        return [request]

    def parse_contact_detail(self, response):
        # the values for the fields are stashed in a json object
        contact_data = json.loads(response.xpath('//input[@id="mapValues"]/@value').extract()[0])
        response.meta['contact_data'] = contact_data
        item = Contact()
        item['date_of_birth'] = contact_data.get('Date of Birth', None)
        item['first_name'] = contact_data.get('First Name', None)
        item['full_name'] = contact_data.get('Full Name', None)
        item['last_name'] = contact_data.get('Last Name', None)
        item['mailing_city'] = contact_data.get('Mailing City', None)
        item['mailing_country'] = contact_data.get('Mailing Country', None)
        item['mailing_state'] = contact_data.get('Mailing State', None)
        item['mailing_street'] = contact_data.get('Mailing Street', None)
        item['mailing_zip'] = contact_data.get('Mailing Zip', None)
        item['membership_start_date'] = contact_data.get('Membership Start Date', None)
        item['membership_end_date'] = contact_data.get('Membership end Date', None)
        item['membership_status'] = contact_data.get('Membership Status', None)
        item['payment_type'] = contact_data.get('Payment Type', None)
        item['salutation'] = contact_data.get('Salutation', None)
        item['secondary_email'] = contact_data.get('EntMail', None)
        item['primary_email'] = contact_data.get('priEmail', None)
        item['contact_id'] = contact_data.get('system_sales_entity_id', None)
        item['payment_type'] = contact_data.get('Payment Type', None)
        return [item]

    def parse_notes(self, response):
        """ Parses notes """
        # Fill in the notes
        for note_selector in response.xpath('//div[@id="actnotes"]/div'):
            note = Note()
            note['note_id'] = note_selector.xpath('@id').extract()[0]
            try:
                note['title'] = note_selector.xpath('b/span/text()').extract()[0]
            except IndexError:
                note['title'] = None
            note['body'] = note_selector.xpath('pre[starts-with(@id,"noteContWithRegex")]/text()').extract()[0]
            note['parent_contact_id'] = response.meta['contact_id']
            note['created_at'] = note_selector.xpath('span//@data-title').extract()[0]
            try:
                note['by'] = note_selector.xpath('//span[@data-title]/../text()').extract()[0].encode('windows-1252').split('\xa0')[1]
            except:
                inspect_response(response)
            yield note

        
    def parse_email_list(self, response):
        # Load the email pages
        pattern = "JavaScript:viewMail\('(?P<msgid>\w+)','(?P<mailType>\w+)','(?P<closeStr>\w+)','(?P<sentOrReceived>\w+)', (?P<ismailkanbanview>\w+)\)"
        count = 0
        for href in response.xpath('//a[@class="f12" and starts-with(@href,"JavaScript:viewMail")]/@href').extract():
            view_mail_params = {}
            m = re.match(pattern, href)
            if not m:
                self.log("no match")
                inspect_response(response)
            count += 1
            view_mail_params = m.groupdict()
            params = {}
            params['action'] = 'viewMail'
            params['msgid'] = view_mail_params['msgid']
            params['user_id'] = 'null'
            params['module'] = 'Contacts'
            params['entId'] = response.xpath('//input[@id="entityID"]/@value').extract()[0]
            params['mailType'] = view_mail_params['mailType']
            params['sentOrReceived'] = view_mail_params['sentOrReceived']
            #params['entEmailId'] = yy
            params['flag'] = 'false'
            param_string = urllib.urlencode(params)
            url = "https://crm.zoho.com/crm/EntReply.do?" + param_string
            request = scrapy.Request(url, callback=self.parse_email)

            # The entId is not contained in the response, but is still needed
            request.meta['entId'] = params['entId']
            
            if not (
                view_mail_params['mailType'] == 'DMAIL' and
                view_mail_params['closeStr'] == 'Close' and 
                view_mail_params['sentOrReceived'] == 'Sent' and
                (
                    view_mail_params['ismailkanbanview'] == '15' or
                    view_mail_params['ismailkanbanview'] == '35' or
                    view_mail_params['ismailkanbanview'] == '40'
                )
            ):
                response.meta['xx_params'] = view_mail_params
                #inspect_response(response)

            yield request
        response.meta['count'] = count
        for i in self.check_for_more_email(response):
            yield i

    def check_for_more_email(self, response):
        if response.meta['count'] == 10:
            #inspect_response(response)
            pass

        # check for paginated emails
        contact_id = response.meta['contact_id']
        range_selector = response.xpath('//span[@class="dim"]')
        if len(range_selector) > 0:
            start_page = int(range_selector.xpath('../text()')[0].extract())
            end_page = int(range_selector.xpath('../text()')[1].extract())
            # the logic here is weird
            if start_page - response.meta['start'] == 10:
                inspect_response(response)

            if end_page - start_page == 9:
                for i in self.request_email_list(contact_id, end_page + 1):
                    yield i
        elif (
                len(response.xpath('//table[@class="norec"]//div/text()')) > 0 and
                response.xpath('//table[@class="norec"]//div/text()').extract()[0] == "No records found"
             ):
            #self.log("email list for {} (2) No records found".format(contact_id))
            pass
        else:
            pass
            #self.log("email list for {} (2) of {}".format(contact_id, count))
            #inspect_response(response)

    def parse_email(self, response):
        email_record = EmailRecord()
        email_record['contact_zoho_crm_id'] = response.meta['entId']
        email_record['msg_id'] = response.xpath('//input[@id="msgid"]/@value').extract()[0]
        email_record['from_email'] = response.xpath('//div[@id="fromDiv"]/div[@class="composeRightDiv"]/text()').extract()[0]
        email_record['to_email'] = response.xpath('//div[@id="toDiv"]/div[@class="composeRightDiv"]/text()').extract()[0]
        email_record['sent_time'] = response.xpath('//div[@id="mailSentTime"]/text()').extract()[0]
        email_record['subject'] = response.xpath('//div[@id="subjectDiv"]/div[@class="composeRightDiv"]/text()').extract()[0]

        # the body is contained in javascript
        javascript = response.xpath('/html/body/script').extract()[0]
        m = re.search('iframeDoc.writeln\("(.+)"\);', javascript)
        escaped_body = m.group(1)
        email_record['body'] = escaped_body.decode('string-escape')
        return [email_record]

