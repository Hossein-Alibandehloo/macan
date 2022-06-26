from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account
import requests


class BP_Updater:
    start_row = 5
    last_row = 15

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

    def update(self, start_row, last_row, st, page_type):
        if self.page_type == 'Business page'
            result = self.sheet.values().get(spreadsheetId=self.sheet_id_target, range="contact business page!B{}:B{}".format(start_row, last_row)).execute()
            v = result['values']
            id_index = []
            j = self.start_row
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
                st.write(k[1])

            request = self.sheet.values().update(spreadsheetId=self.sheet_id_target,
                                        range="contact business page!E{}:F{}".format(start_row, last_row), valueInputOption="USER_ENTERED", body={'values':data}).execute()
            print(request)
        else:
            result = self.sheet.values().get(spreadsheetId=self.sheet_id_target, range="Contact influencer!B{}:B{}".format(start_row, last_row)).execute()
            v = result['values']
            id_index = []
            j = self.start_row
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
                st.write(k[1])

            request = self.sheet.values().update(spreadsheetId=self.sheet_id_target,
                                        range="contact business page!H{}:I{}".format(start_row, last_row), valueInputOption="USER_ENTERED", body={'values':data}).execute()
            print(request)
            

