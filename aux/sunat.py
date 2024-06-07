import requests
import time
import json
import logging

def send_request(partida_val,start_date,end_date):
    # start_date must be 'dd/mm/YYYY'
    # end_date must be 'dd/mm/YYYY'
    url = "http://www.aduanet.gob.pe/cl-ad-itestdesp/SEGrabaReq"
    headers = {
        'Host': 'www.aduanet.gob.pe',
        'Connection': 'keep-alive',
        'Content-Length': '106',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'http://www.aduanet.gob.pe',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://www.aduanet.gob.pe/cl-ad-itestdesp/FrmConsultaSumin.jsp?tcon=N',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    req_body = 'lcnan='+partida_val+'&fini='+start_date+'&ffin='+end_date+'&ltotaduana=T&ltotpais=T&tipo=DBF&tcon=N&regi=Impo'
    logging.getLogger('sunat.send_request').info(req_body)
    response = requests.request('POST', url, headers = headers, data = req_body)
    return response

def search_id(search_text):
    url = 'http://www.aduanet.gob.pe/itarancel/arancelS01Alias/?'

def get_request(request_id, date_of_request, time_of_request):
    # date_of_request must be 'YYYYMMDD'
    # time_of_request must be 'HHMMSS'
    url = 'http://www.aduanet.gob.pe/cl-ad-itsuministro/descargaS01Alias'
    headers = {
        'Host': 'www.aduanet.gob.pe',
        'Connection': 'keep-alive',
        'Content-Length': '81',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'http://www.aduanet.gob.pe',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://www.aduanet.gob.pe/cl-ad-itsuministro/descargaS01Alias?accion=cargarFrmDescargarResultado',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    req_body = 'accion=descargarArchivo&filename='+request_id+'.ZIP&fregistro='+date_of_request+'&hregistro='+time_of_request
    #print(req_body)
    retries_cnt = 0
    max_retries = 5
    is_zip = False
    while(True):
        response = requests.request('POST', url, headers = headers, data = req_body)
        response_headers = json.loads(json.dumps(dict(response.headers)))
        if response.status_code == 200 and response_headers['Content-Type'] == 'application/zip':
            is_zip = True
            break
        elif response.status_code == 200 and response_headers['Content-Type'] == 'text/html; charset=ISO-8859-1':
            if retries_cnt <= max_retries:
                retries_cnt += 1
                req_body = 'accion=descargarArchivo&filename='+request_id+'.ZIP&fregistro='+date_of_request+'&hregistro='+time_of_request[:-2]+str(int(time_of_request[-2:])+1)
                time.sleep(5)
                continue
            else:
                logging.getLogger().error('Max retries for request {} reached'.format(req_body))
                break
        else:
            logging.getLogger('sunat.get_request').error('Failed to fetch request {}'.format(req_body))
            logging.getLogger('sunat.get_request').error(response.headers)
            logging.getLogger('sunat.get_request').error(response.content)
            break
    return response,is_zip
