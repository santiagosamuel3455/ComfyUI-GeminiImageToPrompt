import requests
import os
import json

class DeepseekR1KlingAINode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "email": {"type": "STRING", "default": "lufimu.ci.s@gmail.com"},
                "password": {"type": "STRING", "default": "Mocomoco1", "multiline": False},
                "prompt": {"type": "STRING", "default": "a red car", "multiline": True},
                "mode": {"type": "BOOLEAN", "default": True,
                         "display": "checkbox",
                         "label_on": "Text to Video",
                         "label_off": "Image to Video"}
            }
        }

    RETURN_TYPES = ("STRING",)  # Retorna el resultado generado por la API
    FUNCTION = "generate_prompt"
    CATEGORY = "KlingAI"

    def generate_prompt(self, email, password, prompt, mode):
        """
        Esta función se ejecuta cuando el nodo se procesa.
        Hace login y genera una respuesta desde la API.
        """

        # Cargar credenciales desde variables de entorno si existen
        portal_st = os.environ.get("PORTAL_ST")
        portal_ph = os.environ.get("PORTAL_PH")
        user_id = os.environ.get("USER_ID")

        # Si no están disponibles, hacer login
        if not all([portal_st, portal_ph, user_id]):
            print("Faltan credenciales. Iniciando sesión...")
            portal_st, user_id, portal_ph, _ = self.login_pre(email, password)
            if portal_st and user_id and portal_ph:
                os.environ["PORTAL_ST"] = portal_st
                os.environ["PORTAL_PH"] = portal_ph
                os.environ["USER_ID"] = str(user_id)
            else:
                raise Exception("No se pudo iniciar sesión. Verifica tus credenciales.")

        # Seleccionar el modo
        selected_original_id = "t2v" if mode else "i2v_tail"

        # Llamar a la función de chat
        response = self.create_chat_session(user_id, portal_st, portal_ph, prompt, selected_original_id)

        return (response,)  # Devuelve la respuesta al siguiente nodo

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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://app.klingai.com",
            "Cookie": f"userId={user_id}; ksi18n.ai.portal_st={portal_st}; ksi18n.ai.portal_ph={portal_ph}",
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
            "User-Agent": "Mozilla/5.0",
            "accept": "text/event-stream",
            "Content-Type": "application/json",
            "Origin": "https://app.klingai.com",
            "Cookie": f"userId={user_id}; ksi18n.ai.portal_st={portal_st}; ksi18n.ai.portal_ph={portal_ph}"
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
            "User-Agent": "Mozilla/5.0",
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "Origin": "https://klingai.com"
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
