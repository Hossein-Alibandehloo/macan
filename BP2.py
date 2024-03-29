from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account
import requests
import pandas as pd
from time import sleep
from lxml import html


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
        # try:
        #     service = build('sheets', 'v4', credentials=self.creds, cache_discovery=False)
        # except:
        #     DISCOVERY_SERVICE_URL = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
        #     service = build('sheets', 'v4', credentials=self.creds, cache_discovery=False)
            
        self.sheet = service.spreadsheets()
        # result = sheet.values().get(spreadsheetId=sheet_id_target,
        #                                     range="Sheet1!A1:B5").execute()
        # values = result.get('values', [])

        

    def influencermarketinghub(self, id):
        request_url = "https://hypeauditor.com/instagram/" + id
        response = requests.get(request_url)
        tree = html.fromstring(response.content)
        xpath_expression_followers = "//div[@class='metric metric']/text()"

        data = tree.xpath(xpath_expression_followers)
        # data = [
        #     "",
        #     float(data[1].replace("%",""))/100
        # ]
        if len(data) <1:
            data = [
                'N/A',
                "N/A"
            ]
        else:
            data[1] = float(data[1].replace("%",""))/100
            if 'M' in data[0]:
                data[0] = int(float(data[0].replace("M", "")) * 1000000)
            elif "K" in data[0]:
                data[0] = int(float(data[0].replace("K", "")) * 1000)        
        return data

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
    def tlg_member2(self, id):
        if '/t.me/joinchat' not in id:
            res = requests.get("https://t.me/s/" + id)
            xp = html.fromstring(res.text)
            member = xp.xpath("//span[@class='counter_value']/text()")
            result = 0
            if len(member) > 0:
                if 'M' in member[0]:
                    result = member[0].replace('M', '')
                    result = float(result) * 1000000 
                elif 'K' in member[0]:
                    result = member[0].replace('K', '')
                    result = float(result) * 1000
                    print(result)
                return int(round(result/1000) * 1000) 
            else:
                return 'N/A'
        else:
            res = requests.get(id)
            xp = html.fromstring(res.text)
            member = xp.xpath("//div[@class='tgme_page_extra']/text()")
            if len(member) > 0:
                result = member[0].strip().replace('members','').replace(' ', '')
                return int(round(int(result.replace("subscribers",''))/1000)*1000)
            else:
                return 'N/A'
    def update(self, startRow, lastRow, st, page_type):
#         startRow = startRow + 2
#         lastRow = lastRow + 2
        progress = st.empty()
        
        if page_type == 'Business Pages':
            result = self.sheet.values().get(spreadsheetId=self.sheet_id_target, range="Business Pages!A{}:A{}".format(startRow, lastRow)).execute()
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
            follower_er = ["-", "-"]
            for row in id_index:
                progress.markdown(f'Initial updating row is: {row[1]}')
                try:
                    follower_er = self.influencermarketinghub(row[0])
                except: 
                    sleep(15)
                    try:
                        follower_er = self.influencermarketinghub(row[0])
                    except:
                        data.append(['*', '*'])
                data.append([follower_er[0], follower_er[1]])
                

            request = self.sheet.values().update(spreadsheetId=self.sheet_id_target,
                                        range="Business Pages!C{}:D{}".format(startRow, lastRow), valueInputOption="USER_ENTERED", body={'values':data}).execute()
            print(request)
            progress.markdown('')
        elif page_type == 'Influencers':
            
            result = self.sheet.values().get(spreadsheetId=self.sheet_id_target, range="Influencers!A{}:A{}".format(startRow, lastRow)).execute()
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
            follower_er = ["-", "-"]
            for row in id_index:
                progress.markdown(f'Initial updating row is: {row[1]}')
                try:
                    follower_er = self.influencermarketinghub(row[0])
                except: 
                    sleep(15)
                    try:
                        follower_er = self.influencermarketinghub(row[0])
                    except:
                        data.append(['*', '*'])
                data.append([follower_er[0], follower_er[1]])
                

            request = self.sheet.values().update(spreadsheetId=self.sheet_id_target,
                                        range="Influencers!G{}:H{}".format(startRow, lastRow), valueInputOption="USER_ENTERED", body={'values':data}).execute()
            print(request)
            progress.markdown('')
        elif page_type == "Telegram":
            result = self.sheet.values().get(spreadsheetId=self.sheet_id_target, range="Telegram!A{}:A{}".format(startRow, lastRow)).execute()
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
                progress.markdown(f'Initial updating row is: {row[1]}')
                try:
                    tlg_data = self.tlg_member2(row[0])
                except: 
                    sleep(15)
                    tlg_data = self.tlg_member2(row[0])
                data.append([tlg_data])
            request = self.sheet.values().update(spreadsheetId=self.sheet_id_target,
                                        range="Telegram!C{}:C{}".format(startRow, lastRow), valueInputOption="USER_ENTERED", body={'values':data}).execute()
            print(request)
            progress.markdown('')
            
    def get_data(self, name):

#         global sheet, service, sheet_id_target, data_range
        if name == 'Business Pages':
            result = self.sheet.values().get(spreadsheetId=self.sheet_id_target, range= "Business Pages!A1:F5000").execute()
        elif name == 'Influencers':
            result = self.sheet.values().get(spreadsheetId=self.sheet_id_target, range= "Influencers!A1:I5000").execute()
        elif name == 'Telegram':
            result = self.sheet.values().get(spreadsheetId=self.sheet_id_target, range= "Telegram!A1:C5000").execute()
        data = result['values']
        
        for l in data:
            max = len(data[0])
            if len(l) < max:
                while True:
                    l.append('')
                    if len(l) == len(data[0]):
                        break
#         index = [first[0] for first in data][1:]
        headless_data = data[1:]
        df = pd.DataFrame(headless_data, columns=data[0])
        try:
            del df["Phone"]
        except:
            pass
        if 'PhoneNumber' in data[0]:
            del df['PhoneNumber']
        
        return df 
