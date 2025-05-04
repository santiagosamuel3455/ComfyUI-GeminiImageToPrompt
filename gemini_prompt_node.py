import torch
import numpy as np
from PIL import Image
import google.generativeai as genai

# Mapeo de modelos Gemini
modelo_ids = {
    "Gemini 2.5 Flash": "gemini-2.5-flash-preview-04-17",
    "Gemini 2.0 Flash": "gemini-2.0-flash",
    "Gemini 2.0 Pro": "gemini-2.0-pro-exp-02-05",
    "Gemini 2.0 Flash Thinking": "gemini-2.0-flash-thinking-exp-01-21",
    "Gemini": "gemini-exp-1206",
    "Gemini 1.5 Pro": "gemini-exp-1206",
    "Gemini 1.5 Flash-8B": "gemini-1.5-flash-8b"
}

# Prompt base por defecto (ahora se puede sobrescribir desde la UI)
DEFAULT_PROMPT_BASE = 'Analyze the provided image and generate a detailed 5-second cinematic video description based on it. Start with the main action in a single sentence. Describe visible movements, gestures, or dynamics (e.g., someone blinking, a door creaking shut). Detail the physical appearance of key characters or objects: clothing, expressions, colors, and textures. Include background elements such as weather, architecture, natural or artificial features. Specify the camera angle (low angle, close-up, wide shot) and any lens movement (smooth zoom, dolly, tracking shot). Describe the lighting type (golden-hour sunlight, cold neon, harsh indoor light) and dominant color palette. Mention any sudden visual changes (flickering lights, moving shadows, motion blur) in chronological order. Keep everything in a single fluid paragraph, technical and visually precise. Max 200 words.'

class GeminiImageToPromptNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {"default": "", "multiline": False}),
                "modelo_select": (list(modelo_ids.keys()),),
                "prompt_base": ("STRING", {
                    "default": DEFAULT_PROMPT_BASE,
                    "multiline": True
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_prompt"
    CATEGORY = "Gemini"

    def generate_prompt(self, image, api_key, modelo_select, prompt_base):
        # Configurar Gemini
        try:
            genai.configure(api_key=api_key)
        except Exception as e:
            raise ValueError(f"Error configurando Gemini API: {e}")

        selected_mod_id = modelo_ids.get(modelo_select)
        if not selected_mod_id:
            raise ValueError(f"Modelo no encontrado: {modelo_select}")

        model = genai.GenerativeModel(selected_mod_id)

        # Convertir el tensor en una imagen PIL
        i = 255. * image[0].cpu().numpy()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

        # Generar contenido usando el prompt_base editable
        try:
            response = model.generate_content([prompt_base, img])
        except Exception as e:
            raise ValueError(f"Error generando contenido con Gemini: {e}")

        # Extraer texto
        if response.candidates and len(response.candidates) > 0:
            text = response.candidates[0].content.parts[0].text
        else:
            text = "No se generó texto en la respuesta."

        print(text)
        return (text,)
