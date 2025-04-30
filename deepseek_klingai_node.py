import requests
import os
import json

# Definición de modelos disponibles
moodel_originals = {
    "Text to Image": "t2i",
    "Text to Video": "t2v",
    "Image To Video": "i2v_tail"
}

class DeepseekR1KlingAINode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # Campo editable: Email
                "email": ("STRING", {"default": "almacenamientodrive81@gmail.com", "multiline": False}),
                
                # Campo oculto: Contraseña
                "password": ("STRING", {"default": "karAr3544_a334", "multiline": False, "display": "password"}),
                
                # Prompt configurable
                "prompt": ("STRING", {"default": "un auto de color rojo", "multiline": True}),
                
                # Modelo seleccionable desde lista desplegable
                "model": (list(moodel_originals.keys()), {}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")  # Respuesta + Puntos/Rewards
    RETURN_NAMES = ("generated_text", "user_points")
    FUNCTION = "generate_prompt"
    CATEGORY = "KlingAI"

    def generate_prompt(self, email, password, prompt, model):
        """
        Función principal ejecutada al llamar al nodo.
        Genera un prompt usando la API de Kling AI después de autenticar al usuario.
        """
        selected_model_id = moodel_originals.get(model)
        if not selected_model_id:
            raise ValueError(f"Modelo no encontrado: {model}")

        # Cargar credenciales guardadas o iniciar sesión
        portal_st = os.environ.get("PORTAL_ST")
        portal_ph = os.environ.get("PORTAL_PH")
        user_id = os.environ.get("USER_ID")

        # Si faltan credenciales, hacer login
        if not all([portal_st, portal_ph, user_id]):
            print("Faltan credenciales. Iniciando sesión...")
            portal_st, user_id, portal_ph, _ = self.login_pre(email, password)

            # Guardar en variables de entorno si el login fue exitoso
            if portal_st and user_id and portal_ph:
                os.environ["PORTAL_ST"] = portal_st
                os.environ["PORTAL_PH"] = portal_ph
                os.environ["USER_ID"] = str(user_id)
            else:
                raise Exception("No se pudo iniciar sesión. Verifica tus credenciales.")

        # Generar el prompt usando el modelo seleccionado
        generated_text = self.create_chat_session(user_id, portal_st, portal_ph, prompt, selected_model_id)

        # Obtener puntos del usuario actualizados
        total_points = self.obtener_puntos_y_tickets(portal_st, user_id, portal_ph) or "N/A"

        return (generated_text, total_points)

    def create_chat_session(self, user_id, portal_st, portal_ph, prompt, selected_original_id):
        url = "https://api-app-global.klingai.com/api/tools/chat/session/create"
        params = {
            "__NS_hxfalcon": "HUDR_sFnX-FFuAW5VsfDNK0XOP6snthhLcvMxjhNz8_v61ETYFIY7AGWHwcilbvTy_pkF5Sf2Bz8EKKEbay4e2NmWuUQYvOMDylMlJU6FABi__gHaiFm-JIp2bntv2Ig4FT5CIbQSVBLOio_UbX8unwSMWC2tuBYJ0JxYsJcW4GrUhtAdqcEKLSTvnBU_9kW0-ltMSRxIt8N8DdeY1ntYXOb955wKLh87pmSbasl2ybtsxdnHT_wREYeFabFLe1-NHFGdjXfLR803wy-eibsNBmgqesEnJyTBi7F7lT_okwZHGksAydmQKsm0vPqm17-Fdz-dy63dDaU9PL_eSz3tXXpVmCGNOsyakre0A8J2v8Mxc4S1TZim9Us9qDe1nmnUu0llAbaqJ8UPqKMwVB8v5dPXNESn2beq8r3n-OTT2u2OKs81cMZAYRcNtHfC6FXScqv3hpQhjaSwld82SSxu3sLy65lrmmmCgBT__6-J8Oe3AlSEvJMg4O8tIj3H4RKgkb5eYZbvS8XaKWtt6Dbtl0rdX2lUz7Y-NJBzynFFDhu2Fc5wyP1zSoMJcUWNKzju8IrwoS7mW9wXFhGD6rc1-o8BMm4XRJNl5i9W5dgrOHKfERqHB7naZ40kkq3ya-K_LBLyU-WuSoANYDLcXWMJPquGPvt_OlFsJS6hpeyoA91wumgeq7AXbkvNp-WCmTguurEAfex8ICkO8UqMJ-7bJ6iw8ANPdem-jU4v0BQe0avC8g..$HE_c2dd452022a19777dd1f88b8c38a60a39b8889898988c91125339e07fb6c8b87ef141f8812dfb753f2dfb76189&caver=2"
        }
        headers = {
            "Host": "api-app-global.klingai.com",
            "Connection": "keep-alive",
            "sec-ch-ua-platform": "Windows",
            "Time-Zone": "America/Buenos_Aires",
            "Accept-Language": "en",
            "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?0",
            "ktrace-str": "3|My42NjQ1NzA2OTQ1NjU3Mzc5LjMzNjg2NDc3LjE3NDUxODU3MjQ3NjYuMTk5MQ==|My42NjQ1NzA2OTQ1NjU3Mzc5LjIzNTE0NDc1LjE3NDUxODU3MjQ3NjYuMTk5MA==|0|aigc-kling-web-fe-aio|aigc|true|src:Js,seqn:2333,rsi:f4e78e41-2279-4210-bfbb-505fc1d86080,path:/global/text-to-image/277154724527845,rpi:5a39174a1m",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://app.klingai.com",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://app.klingai.com/",
            "Cookie": f"__risk_web_device_id=abce1c131745180286835181; did=web_307dd541810b3df30892a7f89eb88e269558; userId={user_id}; ksi18n.ai.portal_st={portal_st}; ksi18n.ai.portal_ph={portal_ph}",
            "Accept-Encoding": "gzip, deflate"
            }

        payload = {
            "modelType": "deepseek",
            "referPageCode": selected_original_id
        }

        try:
            response = requests.post(url, headers=headers, json=payload, params=params)
            if response.status_code == 200:
                data = response.json()
                chatSessionId = data['data']['chatSessionId']
                return self.generate_youtuber_prompt(user_id, portal_st, portal_ph, chatSessionId, prompt, selected_original_id)
            else:
                return f"Error: {response.status_code}"
        except Exception as e:
            return f"Exception: {str(e)}"

    def generate_youtuber_prompt(self, user_id, portal_st, portal_ph, chatSessionId, prompt, refer_pagecode):
        url = "https://api-app-global.klingai.com/api/tools/chat/completion"
        headers = {
            "Host": "api-app-global.klingai.com",
            "Connection": "keep-alive",
            "sec-ch-ua-platform": "Windows",
            "Cache-Control": "no transform",
            "X-Accel-Buffering": "no",
            "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?0",
            "ktrace-str": "3|My42NjQ1NzA2OTQ1NjU3Mzc5LjY1MzQ0MzY4LjE3NDUxODU3MjU0OTQuMTk5Mw==|My42NjQ1NzA2OTQ1NjU3Mzc5LjM0OTc1MjI0LjE3NDUxODU3MjU0OTQuMTk5Mg==|0|aigc-kling-web-fe-aio|aigc|true|src:Js,seqn:2333,rsi:f4e78e41-2279-4210-bfbb-505fc1d86080,path:/global/text-to-image/277154724527845,rpi:5a39174a1m",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "accept": "text/event-stream",
            "Content-Type": "application/json",
            "Origin": "https://app.klingai.com",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://app.klingai.com/",
            "Accept-Language": "es-ES,es;q=0.9",
            "Cookie": f"__risk_web_device_id=abce1c131745180286835181; did=web_307dd541810b3df30892a7f89eb88e269558; userId={user_id}; ksi18n.ai.portal_st={portal_st}; ksi18n.ai.portal_ph={portal_ph}",
            "Accept-Encoding": "gzip, deflate"
        }

        payload = {
            "prompt": prompt,
            "modelType": "deepseek",
            "referPageCode": refer_pagecode,
            "chatSessionId": chatSessionId
        }

        try:
            response = requests.post(url, headers=headers, json=payload, stream=True)
            full_response = ""
            for line in response.iter_lines(decode_unicode=True):
                if line.startswith("data:"):
                    try:
                        data = json.loads(line[5:].strip())
                        content = data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                        full_response += content
                    except Exception:
                        pass
            return full_response.strip()
        except Exception:
            return "Failed to get response."

    def login_pre(self, email, password):
        url = "https://id.klingai.com/pass/ksi18n/web/login/emailPassword"
        headers = {
            "Host": "id.klingai.com",
            "Connection": "keep-alive",
            "sec-ch-ua-platform": "\"Windows\"",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
            "Content-type": "application/x-www-form-urlencoded",
            "sec-ch-ua-mobile": "?0",
            "Accept": "*/*",
            "Origin": "https://klingai.com",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://klingai.com/",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate"
        }

        data = {
            "sid": "ksi18n.ai.portal",
            "email": email,
            "password": password,
            "language": "en"
        }

        try:
            response = requests.post(url, headers=headers, data=data)
            if response.status_code == 200:
                response_data = response.json()
                portal_st = response_data.get("ksi18n.ai.portal_st")
                user_id = response_data.get("userId")
                portal_ph = response_data.get("ksi18n.ai.portal_ph")
                return portal_st, user_id, portal_ph, True
            else:
                return None, None, None, False
        except Exception:
            return None, None, None, False

    def get_pay_reward2(self, portal_st, user_id, portal_ph):
        url = "https://api-app-global.klingai.com/api/pay/reward"
        headers = {
            "Host": "api-app-global.klingai.com",
            "Connection": "keep-alive",
            "sec-ch-ua-platform": "Windows",
            "Time-Zone": "America/Buenos_Aires",
            "Accept-Language": "en",
            "Accept": "application/json, text/plain, */*",
            "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "sec-ch-ua-mobile": "?0",
            "Origin": "https://app.klingai.com",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://app.klingai.com/",
            'Cookie': f'weblogger_did=web_5931339371593BA8; _gcl_au=1.1.1761745921.1736101477; _ga=GA1.1.1592685728.1736101477; _ga_MWG30LDQKZ=GS1.1.1736101476.1.0.1736101477.59.0.1150361734; did=web_9bd9693ae0f8cefd617435a586eeb2053025; trial-package-dialog=true; _clck=1clzkmg%7C2%7Cfsb%7C0%7C1831; _clsk=hk1o5e%7C1736101482896%7C1%7C0%7Co.clarity.ms%2Fcollect; userId={user_id}; ksi18n.ai.portal_st={portal_st}; ksi18n.ai.portal_ph={portal_ph}; _uetsid=51d4a9a0cb9211efbd095120939e236b; _uetvid=51d4c5a0cb9211ef8e2661698d74a2c5',
            "Accept-Encoding": "gzip, deflate"
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get("message") == "Success":
                    totals = self.obtener_puntos_y_tickets(portal_st, user_id, portal_ph)
                    total_str = str(totals)
                    return total_str[:-2] + '.' + total_str[-2:]
                return "0"
            return "0"
        except:
            return "0"

    def obtener_puntos_y_tickets(self, portal_st, user_id, portal_ph):
        url = "https://klingai.com/api/account/pointAndTicket"
        headers = {
            'Host': 'klingai.com',
            'Connection': 'keep-alive',
            'sec-ch-ua-platform': '"Windows"',
            'Accept-Language': 'en',
            'Accept': 'application/json, text/plain, */*',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://klingai.com/',
            'Cookie': f'weblogger_did=web_5931339371593BA8; _gcl_au=1.1.1761745921.1736101477; _ga=GA1.1.1592685728.1736101477; _ga_MWG30LDQKZ=GS1.1.1736101476.1.0.1736101477.59.0.1150361734; did=web_9bd9693ae0f8cefd617435a586eeb2053025; trial-package-dialog=true; _clck=1clzkmg%7C2%7Cfsb%7C0%7C1831; _clsk=hk1o5e%7C1736101482896%7C1%7C0%7Co.clarity.ms%2Fcollect; userId={user_id}; ksi18n.ai.portal_st={portal_st}; ksi18n.ai.portal_ph={portal_ph}; _uetsid=51d4a9a0cb9211efbd095120939e236b; _uetvid=51d4c5a0cb9211ef8e2661698d74a2c5',
            'Accept-Encoding': 'gzip, deflate'
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data['data']['total']
            return None
        except:
            return None
