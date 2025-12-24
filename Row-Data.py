import requests
import brotli
import zlib
vehicle_number = input("Enter Vehicle Registration Number: ")
base_url = "https://www.acko.com"
vehicle_url = f"{base_url}/asset_service/api/assets/search/vehicle/{vehicle_number}?validate=false&source=vas_fastag"
puc_url = f"{base_url}/vas/api/v1/pucs?registration-number={vehicle_number}"
challan_url = f"{base_url}/vas/api/v1/challans/?registration-number={vehicle_number}&source=CHALLAN_PAGE"
headers = {
    "Host": "www.acko.com",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "accept": "application/json",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "upgrade-insecure-requests": "1",
    "sec-fetch-site": "none",
    "sec-fetch-mode": "navigate",
    "sec-fetch-user": "?1",
    "sec-fetch-dest": "document",
    "cookie": "trackerid=179aa6e9-ca2f-4298-adfb-7a2079f45239; acko_visit=i184eQX5pfoDbAwrkofEuA; _ga=GA1.1.1738483623.1745154975; FPID=FPID2.2.BNactSqBEJYZy0GtFayP4nbw276RJEZO4ZGxgDvWd%2FQ%3D.1745154975; FPAU=1.2.348938027.1745154976; _gtmeec=e30%3D; _fbp=fb.1.1745154976133.1568369174; user_id=eFLS7co3phjxpwDoNIkrPw:1745155002698:e7fdef44ea0065aa6372165a62d91e0b7d8f1440; _ga_W47KBK64MF=GS1.1.1745154975.1.1.1745155051.0.0.203712065; __cf_bm=nkXwQrar2uE2AYsZ3SErkSYFMOZhGstBL4KGaawfcBk-1745234838-1.0.1.1-qCl9aKP2EGODZq8VThqc3uOeYjpF0fvFX53rZj3FShkGG1UVJOC5wassxGuhHNJnhgq.eaEa7mvPNx9_TetCE9i5ef9tlHgtVXRWFTrqLKs",
}
def fetch_data(url):
    response = requests.get(url, headers=headers, stream=True)
    print("Status Code:", response.status_code)
    encoding = response.headers.get("Content-Encoding", "")
    raw = response.raw.read()
    if response.status_code == 404:
        print("Error: 404 Not Found. The resource is unavailable.")
        print("Raw Response (Binary Data):")
        try:
            print(raw)
            if b"html" in raw.lower():
                print("Received HTML, possibly an error page.")
            elif b"image" in raw.lower():
                print("Received image, possibly an error page or a non-JSON response.")
        except Exception as e:
            print("Error printing raw response:", e)
        return
    try:
        if "br" in encoding:
            decoded = brotli.decompress(raw).decode("utf-8")
        elif "gzip" in encoding:
            decoded = zlib.decompress(raw, zlib.MAX_WBITS | 16).decode("utf-8")
        elif "deflate" in encoding:
            decoded = zlib.decompress(raw).decode("utf-8")
        else:
            decoded = raw.decode("utf-8")
        print("Decoded JSON:")
        print(decoded)
        try:
            data = response.json()
            print("Parsed JSON:")
            print(data)
        except Exception as e:
            print("Error decoding JSON:", e)
    except Exception as e:
        print("Decompression failed:", e)
print("\nFetching Vehicle Details from PARIVAHAN...")
fetch_data(vehicle_url)
print("\nFetching POLLUTION Details from PARIVAHAN...")
fetch_data(puc_url)
print("\nFetching Challan Details from PARIVAHAN...")
fetch_data(challan_url)