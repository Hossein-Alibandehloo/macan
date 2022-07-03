from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account
import requests
import pandas as pd

class BP_Updater:

    SCOPES = None
    creds = None
    sheet_id_target = None
    sheet = None


    def __init__(self):
        # If modifying these scopes, delete the file endless-fire.json.
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        SERVICE_ACCOUNT_FILE = 'endless-fire.json'

        self.creds = None
        self.creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)
        # url = 'https://macanagency.ir/automation/endless-fire.json'
        # response = urlopen(url)

        # data_json = json.loads(response.read())

        # creds = service_account.Credentials.from_service_account_file(data_json, scopes=SCOPES)

        # The ID and range of a sample spreadsheet.
        self.sheet_id_target = '1V35Kr3IhPawZFM5oRUVcneRBRxvXP4bvxjKy3aQyIG0'
        service = build('sheets', 'v4', credentials=self.creds)
        self.sheet = service.spreadsheets()
        # result = sheet.values().get(spreadsheetId=sheet_id_target,
        #                                     range="Sheet1!A1:B5").execute()
        # values = result.get('values', [])

        

    def influencermarketinghub(self, id):
        print(id)
        with requests.Session() as s:
            header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0',}
            Form_data = {
                'action':'insta_calc_new',
                'user_name':id
            }
            res = s.post('https://influencermarketinghub.com/wp-admin/admin-ajax.php', data=Form_data, headers=header)
            dict = res.json()
            if len(dict) > 1:
                res = round(dict['followers']/1000)
                return 1000 * int(res), float(dict['er'])/100
            else:
                return '-', '-'

    def tlg_member(id):
        if '/t.me/joinchat' in id:
            res = requests.get(id)
            xp = html.fromstring(res.text)
            member = xp.xpath("//div[@class='tgme_page_extra']/text()")
            if len(member) > 0:
                return int(member.strip().replace('members','').replace(' ', ''))
            else:
                return '-'
        else:
            res = requests.get('https://ir.tgstat.com/channel/@' + id)
            xp = html.fromstring(res.text)
            member = xp.xpath("//div[@class='align-center']/text()")
            if len(member) > 0:
                return int(member[1].strip().replace(' ',''))
            else:
                return '-'
    def update(self, startRow, lastRow, st, page_type):
        ph = st.empty()
        
        if page_type == 'Business page':
            result = self.sheet.values().get(spreadsheetId=self.sheet_id_target, range="contact business page!B{}:B{}".format(startRow, lastRow)).execute()
            values = result['values']
            id_index = []
            j = startRow
            for value in values:
                if len(value) > 0:
                    id_index.append([value[0], j])
                else:
                    id_index.append(['', j])
                j += 1                
            data = []
            for row in id_index:
                follower_er = self.influencermarketinghub(row[0])
                data.append([follower_er[0], follower_er[1]])
#               ph.metric(row)

            request = self.sheet.values().update(spreadsheetId=self.sheet_id_target,
                                        range="contact business page!E{}:F{}".format(startRow, lastRow), valueInputOption="USER_ENTERED", body={'values':data}).execute()
            print(request)
        elif page_type == 'Influencer':
            progress = st.empty()
            result = self.sheet.values().get(spreadsheetId=self.sheet_id_target, range="Contact influencer!B{}:B{}".format(startRow, lastRow)).execute()
            v = result['values']
            id_index = []
            j = startRow
            for i in v:
                if len(i) > 0:
                    id_index.append([i[0], j])
                else:
                    id_index.append(['', j])
                j +=1                
            data = []
            for k in id_index:
                d = self.influencermarketinghub(k[0])
                data.append([d[0], d[1]])
                progress.markdown(d[0])

            request = self.sheet.values().update(spreadsheetId=self.sheet_id_target,
                                        range="Contact influencer!H{}:I{}".format(startRow, lastRow), valueInputOption="USER_ENTERED", body={'values':data}).execute()
            print(request)
    def get_data(self, name):

#         global sheet, service, sheet_id_target, data_range
        if name == 'contact business page':
            result = self.sheet.values().get(spreadsheetId=self.sheet_id_target, range= "contact business page!B1:F4000").execute()
        elif name == 'Contact influencer':
            result = self.sheet.values().get(spreadsheetId=self.sheet_id_target, range= "Contact influencer!B1:I2000").execute()
        elif name == 'Telegram':
            result = self.sheet.values().get(spreadsheetId=self.sheet_id_target, range= "Telegram!B1:D2000").execute()
        data = result['values']
        
        for l in data:
            max = len(data[0])
            if len(l) < max:
                while True:
                    l.append('')
                    if len(l) == len(data[0]):
                        break
        index = [first[0] for first in data][1:]
        headless_data = data[1:]
        df = pd.DataFrame(headless_data, columns=data[0])

        return df           
            

