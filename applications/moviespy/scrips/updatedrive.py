from googleapiclient.discovery import build
from google.oauth2 import service_account
from ..models import Dia, Funcion
from datetime import datetime


def comprobarDia():
    shortDate = datetime.today().strftime('%Y-%m-%d')
    dia = Dia.objects.filter(dia = shortDate)
    existe = False
    if dia:
        existe = True   
    return existe

def getDatosDia(fecha):
    funciones =  Funcion.objects.filter(fecha__dia = fecha)
    funcion = []
    lista = []
    lista.append(['id', 'pelicula', 'sucursal', 'Funcion', 'hora', 'sala', '# asientos', 'activo'])
    for f in funciones:
        funcion=[f.id, f.pelicula, f.sucursal.nombre, f.tipo_funcion, f.hora, f.sala, f.asientos, f.activo]
        lista.append(funcion)
    return lista

def guardar():
    if comprobarDia():
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        SERVICE_ACCOUNT_FILE = '/home/rodrigo/Desktop/editor-keys.json'
        creds = None
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        # The ID and range of a sample spreadsheet.
        SAMPLE_SPREADSHEET_ID = '1bL7iZO-L6nRhR8h0LT-C9w5xR9kxC6RyQXBaMY5rtUg'
        service = build('sheets', 'v4', credentials=creds)

        #BUSCO SI EXISTE LA HOJA
        sheet_metadata = service.spreadsheets().get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()
        sheets = sheet_metadata.get('sheets', '')

        shortDate = datetime.today().strftime('%Y-%m-%d')
        ok = False
        for h in sheets:
            title = h.get("properties", {}).get("title")
            if title == shortDate:
                ok = True

        if ok:
            #Se obtienen los datos
            lista = getDatosDia(shortDate)
            #Se borra el contenido de la hoja
            rangeAll = '{0}!A1:Z'.format(shortDate)
            body = {}
            resultClear = service.spreadsheets().values().clear( spreadsheetId=SAMPLE_SPREADSHEET_ID, range=rangeAll, body=body).execute()

            #Se escribe en la hoja
            sheet = service.spreadsheets()
            request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=shortDate +"!A1", valueInputOption="USER_ENTERED", body={"values":lista})
            request.execute()
        else:
            sheet_nueva = {
                        "requests": [
                            {
                            "addSheet": {
                                "properties": {
                                "title": shortDate,
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
            sheet = service.spreadsheets()
            result = sheet.batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=sheet_nueva).execute()
            lista = getDatosDia(shortDate)
            request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=shortDate +"!A1", valueInputOption="USER_ENTERED", body={"values":lista})
            request.execute()

def iniciar():
    guardar()

