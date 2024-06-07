from fastapi import FastAPI, HTTPException
from aux import sunat
from bs4 import BeautifulSoup
from pytz import timezone
from datetime import datetime
import re, json



app = FastAPI(
    title="API no-oficial Aduanet",
    #description=description,
    summary="API wrapper to easily source data on imports to Perú, data sourced from SUNAT - Aduanet service.",
    version="0.0.1",
    contact={
        "name": "Jose Quispe",
        "email": "jcarlos.quispe@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

@app.get("/solicitud/")
async def request_data(id_partida: int = 1111111111,start_date: str = '01/01/2000', end_date: str = '31/01/2000'):
    try: 
        r = sunat.send_request(str(id_partida), start_date, end_date)
        soup = BeautifulSoup(r.content, 'lxml')
        finds = soup(text = re.compile('REQUERIMIENTO'))
        if r.status_code == 200 and len(finds) > 0:
            temp = finds[0].split(' : ')
            temp = temp[1].split('.')
            temp2 = json.loads(json.dumps(r.headers))
            response = {'id-solicitud':     int(temp[0]), 
                        'fecha-solicitud':  datetime.strptime(temp2['Date'], "%a, %d %b %Y %H:%M:%S %Z").astimezone(timezone('America/Lima')).strftime("%Y%m%d"),
                        'hora-solicitud':   str(datetime.strptime(temp2['Date'], "%a, %d %b %Y %H:%M:%S %Z").astimezone(timezone('America/Lima')).strftime("%H%M%S"))}
        else:
            raise HTTPException(status_code = r.status_code, detail = r.text)
        return response
    except:
        raise HTTPException(status_code = '400', detail = 'Bad request')
    
@app.post("/resultados")
async def request_results(id_resultado: int = 11111111, date_request: str = 'DDMMYYYY', time_request: str = 'HHMM'):
    response = {}
    return response