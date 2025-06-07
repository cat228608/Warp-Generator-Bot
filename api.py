import requests
import json
import base64

prefix = 'mafiozi'

def create_conf_file(user_id, base64_string):
    random_filename = f"{user_id}_cgv.conf"
    decoded_content = base64.b64decode(base64_string).decode('utf-8')
    with open(random_filename, 'w') as conf_file:
        conf_file.write(decoded_content)
    
    return random_filename

def requests_wg(types):
    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'dnt': '1',
        'priority': 'u=1, i',
        'referer': 'https://warp-gen.vercel.app/',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    }
    try:
        response = requests.get('https://warp-gen.vercel.app/generate-config', headers=headers)
        response_data = response.json()
        if types == 'url':
            return response_data['encodedVpnString']
        else:
            with open(f"{prefix}_cgv.conf", "w") as file:
                file.write(response_data['config'])
                return 'good'
    except Exception as er:
        print(er)
        return 'error'

def warp_limonix(device):
    cookies = {
        '_ym_uid': '1741101037696160966',
        '_ym_d': '9742101036',
        '_ym_isad': '1',
        '_ym_visorc': 'w',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://warp.llimonix.pw',
        'priority': 'u=1, i',
        'referer': 'https://warp.llimonix.pw/',
        'sec-ch-ua': '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
    }
    
    if device == 'computer':
        json_data = {
            'selectedServices': [],
            'siteMode': 'all',
            'deviceType': 'computer',
        }

        try:
            response = requests.post('https://warp.llimonix.pw/api/warp', cookies=cookies, headers=headers, json=json_data)
            response_data = response.json()
            config_base64 = response_data['content']['configBase64']
            names = create_conf_file(prefix, config_base64)
            return names
        except Exception as er:
            print(er)
            return 'error'
    else:
        json_data = {
            'selectedServices': [],
            'siteMode': 'all',
            'deviceType': 'phone',
        }

        try:
            response = requests.post('https://warp.llimonix.pw/api/warp', cookies=cookies, headers=headers, json=json_data)
            response_data = response.json()
            config_base64 = response_data['content']['configBase64']
            names = create_conf_file(prefix, config_base64)
            return names
        except Exception as er:
            print(er)
            return 'error'
            
def warp_str(device):
    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://warp-vless.vercel.app',
        'priority': 'u=1, i',
        'referer': 'https://warp-vless.vercel.app/',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    }
    
    if device == 'computer':
        json_data = {
            'selectedServices': [],
            'siteMode': 'all',
            'deviceType': 'computer',
        }

        try:
            response = requests.post('https://warp-vless.vercel.app/api/warp', headers=headers, json=json_data)
            response_data = response.json()
            config_base64 = response_data['content']['configBase64']
            names = create_conf_file(prefix, config_base64)
            return names
        except Exception as er:
            print(er)
            return 'error'
    else:
        json_data = {
            'selectedServices': [],
            'siteMode': 'all',
            'deviceType': 'phone',
        }

        try:
            response = requests.post('https://warp-vless.vercel.app/api/warp', headers=headers, json=json_data)
            response_data = response.json()
            config_base64 = response_data['content']['configBase64']
            names = create_conf_file(prefix, config_base64)
            return names
        except Exception as er:
            print(er)
            return 'error'