from googleapiclient.discovery import build
#from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

class GoogleConnection():

    def getData():

        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        SERVICE_ACCOUNT_FILE = '/home/rodrigo/Desktop/editor-keys.json'
        creds = None
        creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)


        # The ID and range of a sample spreadsheet.
        SAMPLE_SPREADSHEET_ID = '1bL7iZO-L6nRhR8h0LT-C9w5xR9kxC6RyQXBaMY5rtUg'

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range="datos!A1:C4").execute()


        values = result.get('values', [])

        aoa = [[1, 'a'], [2, 'b'], [3, 'c'], [4, 'd']]

        request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="datos2!A1", valueInputOption="USER_ENTERED", body={"values":aoa})
        request.execute()

######################Creo otra hoja

        sheet_nueva = {
                        "requests": [
                            {
                            "addSheet": {
                                "properties": {
                                "title": "MIchael",
                                "tabColor": {
                                    "red": 1.0,
                                    "green": 0.3,
                                    "blue": 0.4
                                }
                                }
                            }
                            }
                        ]
                    }

        #COn esto creo una nueva
        result = sheet.batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=sheet_nueva).execute()

        #############################

        #Con esto busco una hoja
        sheet_metadata = service.spreadsheets().get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()
        sheets = sheet_metadata.get('sheets', '')

        for h in sheets:
            title = h.get("properties", {}).get("title")
            print(title)

        #############################
        #############Borrando datos de la hoja#############
        #rangeAll = '{0}!A1:Z'.format( 'datos2' )
        #body = {}
        #resultClear = service.spreadsheets().values().clear( spreadsheetId=SAMPLE_SPREADSHEET_ID, range=rangeAll, body=body).execute()
                                                                





        return values

