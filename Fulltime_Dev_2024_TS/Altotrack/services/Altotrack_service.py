import requests
import time
import xml.etree.ElementTree as ET
from services.fulltrack_service import FullTrackService
from datetime import datetime

class AltotrackService:
    def __init__(self, url):
        self.url = url

    def process_xml(self, soap_envelope):
        headers = {
            'Connection': 'Keep-Alive',
            'X-Powered-By': 'ASP.NET',
            'Content-Type': 'text/xml;charset=UTF-8',
            'Accept-Encoding': 'gzip,deflate',
            'Accept': '*/*',
            'Host': 'ws4.altotrack.com',
            'SOAPAction': 'http://tempuri.org/IServicePositions/ProcessXML'
        }
        response = requests.post(self.url, data=soap_envelope, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Error sending data: {response.status_code}")


    def create_xml_string(self, item):
        xml_string = f"""
        <registro>
            <movil>
                <proveedor>{item['proveedor']}</proveedor>
                <nombremovil>{item['nombremovil']}</nombremovil>
                <patente>{item['patente']}</patente>
                <fecha>{datetime.strptime(item['fecha'], '%d/%m/%Y %H:%M:%S').strftime('%d-%m-%Y %H:%M:%S')}</fecha>
                <latitud>{float(item['latitud']):.6f}</latitud>
                <longitud>{float(item['longitud']):.6f}</longitud>
                <direccion>{item['direccion']}</direccion>
                <velocidad>{item['velocidad']}</velocidad>
                <ignicion>{item['ignicion']}</ignicion>
                <GPSLinea>{int(item['GPSLinea'])}</GPSLinea>
                <LOGGPS>{item['LOGGPS']}</LOGGPS>
                <puerta1>{item['puerta1']}</puerta1>
                <evento>{int(item['evento'])}</evento>
            </movil>
        </registro>
        """
        return xml_string.strip()


    def create_soap_envelope(self, xml_serializado):
        soap_template = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
        <soapenv:Header/>
        <soapenv:Body>
            <tem:ProcessXML>
                <tem:xmlSerializado>
                    <![CDATA[
                    {xml_serializado}
                    ]]>
                </tem:xmlSerializado>
            </tem:ProcessXML>
        </soapenv:Body>
        </soapenv:Envelope>
        """
        return soap_template


def Altotrack_service():
    altotrack_service = AltotrackService("http://ws4.altotrack.com/WSPosiciones_Chep/WSPosiciones_Chep.svc")
    
    fulltrack_service = FullTrackService("e6ade765dd9ecb3d0e33a09f18d1fca2ea2ab35f", "5e5b61ac28f7155d0ad1b66861e83eac3d31bedb")

    while True:
        try:
            
            data = fulltrack_service.fetch_data()
            extracted_data = fulltrack_service.extract_values(data)
            
            print("Esperando 30 segundos antes de enviar los datos a Altotrack...")
            time.sleep(30)

            for item in extracted_data:
                xml_data = altotrack_service.create_xml_string(item)
                soap_envelope = altotrack_service.create_soap_envelope(xml_data)
                print(f"Enviando SOAP Envelope a Altotrack:\n{soap_envelope}")
                response = altotrack_service.process_xml(soap_envelope)
                print(f"Respuesta del servidor Altotrack: {response}")

        except Exception as e:
            print(f"Ocurrió un error: {e}")

        time.sleep(180)
