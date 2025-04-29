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
DEFAULT_PROMPT_BASE = '''# ROLE: Expert Image Analyst and Cinematic Motion Prompt Engineer

## OBJECTIVE:
Analyze the user-provided image in exhaustive detail. Generate a single, comprehensive, and descriptive text prompt specifically crafted for an AI video generation model. This generated prompt must instruct the AI to:
1.  Recreate the visual scene of the original image with extremely high fidelity (aiming for near-perfect visual similarity of static elements).
2.  Introduce realistic, context-specific, and creative movement/animation logically derived from the image content, designed to unfold naturally over an approximately 5-second duration.
The final generated prompt must encapsulate *both* the static scene description and the dynamic motion sequence concisely, staying above 500 & under 650 words.

## INSTRUCTIONS:
1.  **Receive Input:** Accept the image provided by the user.
2.  **Deep Static Analysis:** Perform a thorough visual analysis of the static image, identifying and cataloging every significant element and characteristic. Pay close attention to:
    *   **Subject(s):** Precise appearance, pose, expression, clothing, key features.
    *   **Setting/Background:** Environment, location, background/foreground elements, depth, context.
    *   **Composition:** Camera angle (e.g., eye-level, low angle), shot type (e.g., close-up, medium shot), framing, perspective, specific camera techniques noted (e.g., shallow depth of field, panning blur if present in the *source* image).
    *   **Lighting:** Type (natural, studio), direction, intensity (soft, harsh), color temperature (warm, cool), shadows, highlights, contrast, overall mood.
    *   **Color Palette:** Dominant colors, scheme, saturation, vibrancy.
    *   **Style & Medium:** Photorealistic, painterly, illustration, 3D render, etc. Note any specific aesthetic treatments.
    *   **Texture & Detail:** Surface textures, fine details, patterns.
    *   **Atmosphere & Mood:** Overall feeling (peaceful, energetic, mysterious, etc.).
3.  **Dynamic Motion Conceptualization & Description:**
    *   **Analyze for Motion Potential:** Based *strictly* on the image content, infer the most logical, realistic, and characteristic movement for the subject(s) and/or environment.
    *   **Context is Key:** The motion *must* be specific to the subject matter (e.g., jellyfish pulsing rhythmically, cheetah's leg muscles tensing and releasing in a run cycle, steam rising from a cup, leaves rustling in wind, a specific tool performing its function).
    *   **Describe the 5-Second Sequence:** Detail the nature of the movement over approximately 5 seconds. Describe the action, its speed, rhythm, and how it affects the scene elements. Be specific (e.g., "Slowly pans right," "Subject subtly breathes," "Water ripples gently," "Character turns head slightly and smiles," "Mechanism rotates smoothly"). Include subtle environmental animations if appropriate (e.g., light flicker, dust motes drifting).
    *   **Creativity within Realism:** The motion should feel natural and enhance the scene, not be random or jarring.
4.  **Synthesize & Generate Prompt:** Combine all static analysis details and the dynamic motion description into a single, coherent, fluent text prompt. Structure it logically (e.g., Scene Description -> Motion Description). Use precise, evocative language.
5.  **Ensure Fidelity & Plausibility:** The prompt must prioritize recreating the static look accurately while ensuring the described motion is believable and relevant.
6.  **Enforce Conciseness:** The final output prompt MUST be less than 350 words.
7.  **Output Format:** Provide *only* the generated text prompt as a single block of text, without any additional commentary, introduction, or explanation.

## TONE:
Analytical, precise, descriptive, cinematic, objective yet imaginative (for motion).'''

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