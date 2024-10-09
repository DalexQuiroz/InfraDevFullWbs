import requests
import time

class FullTrackService:
    def __init__(self, api_key, secret_key):
        self.api_url = f"https://ws.fulltrack2.com/events/all/apiKey/{api_key}/secretKey/{secret_key}"

    def fetch_data(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching data: {response.status_code}")

    def extract_values(self, data):
        if data.get('status'):
            eventos = data.get('data', [])
            extracted_data = []

            for evento in eventos:
                input_value = evento.get("ras_eve_input", [])
                input_value_2 = input_value[2] if len(input_value) > 2 else None  
                input_value_3 = input_value[3] if len(input_value) > 3 else None  

                extracted_data.append({
                    "proveedor": "Fulltime",
                    "nombremovil": evento.get("ras_vei_veiculo"),
                    "patente": evento.get("ras_vei_placa"),
                    "fecha": evento.get("ras_eve_data_gps"),
                    "latitud": evento.get("ras_eve_latitude"),
                    "longitud": evento.get("ras_eve_longitude"),
                    "direccion": evento.get("ras_eve_direcao"),
                    "velocidad": evento.get("ras_eve_velocidade"),
                    "ignicion": evento.get("ras_eve_ignicao"),
                    "GPSLinea": 1,
                    "LOGGPS": 0,
                    "puerta1": input_value_2,
                    "evento": input_value_3
                })

            return extracted_data
        else:
            raise Exception(f"Error in response: {data.get('message')}")


def main():
    api_key = "e6ade765dd9ecb3d0e33a09f18d1fca2ea2ab35f"
    secret_key = "5e5b61ac28f7155d0ad1b66861e83eac3d31bedb"

    service = FullTrackService(api_key, secret_key)

    while True:
        try:
            data = service.fetch_data()
            extracted_data = service.extract_values(data)

            for item in extracted_data:
                print("Respuesta del servidr Fulltrack")
                print(f"proveedor: {item['proveedor']}, nombremovil: {item['nombremovil']}, patente: {item['patente']}, fecha: {item['fecha']}, latitud: {item['latitud']}, longitud: {item['longitud']}, direccion: {item['direccion']}, velocidad: {item['velocidad']}, ignicion: {item['ignicion']}, GPSLinea: {item['GPSLinea']}, LOGGPS: {item['LOGGPS']}, puerta1: {item['puerta1']}, evento: {item['evento']}")
        
        except Exception as e:
            print(f"Ocurrió un error: {e}")

        time.sleep(180)  

