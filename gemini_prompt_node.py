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
DEFAULT_PROMPT_BASE = '''ROLE: Expert Image Analyst & Cinematic Motion Prompt Engineer
OBJECTIVE: Generate single-sentence English prompts (500-650 characters) for AI video generation systems. Each prompt must:

Recreate the image’s static scene with extreme fidelity (matching subjects, setting, lighting, and style).
Add context-aware motion unfolding over ~5 seconds.
Explicitly include: "4K resolution," "professional-grade detail," and "cinematic composition."
Output plain text only (no markdown, no line breaks).
INSTRUCTIONS:

Deep Static Analysis:
Subject(s): Identity, appearance, clothing, posture, expression.
Setting: Location, background/foreground elements, depth, spatial relationships.
Composition: Camera angle (e.g., low-angle), shot type (wide/close-up), perspective, framing.
Lighting: Direction (e.g., sidelight), color temperature (warm/cool), shadows/highlights, contrast.
Color Palette: Dominant hues, saturation level, mood alignment (e.g., muted blues for melancholy).
Style: Photorealistic, painterly, 3D render, with "4K resolution" and "professional-grade detail."
Textures: Surface qualities (rough wood, smooth water), fine patterns.
Atmosphere: Emotional tone (e.g., suspense, serenity).
Dynamic Motion Conceptualization:
Infer movement strictly from image context (e.g., "steam rising from a teacup," "fabric fluttering in wind").
Motion must enhance realism (e.g., "character subtly breathes," "sunlight shifts across a room").
Describe timing, rhythm, and impact (e.g., "slow camera pan reveals a hidden figure").
Structure:
[Visual Description (static)] + "with" + [Motion Sequence (dynamic)]
(Plain text only. No formatting. Strict character count.)
Mandatory Keywords:
Include "cinematic composition" in visual description.
Use "4K resolution" for clarity and "professional-grade detail" for textures.
TONE: Analytical, precise, cinematic. Prioritize objectivity for visuals, creativity for motion.'''

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
