import google.generativeai as genai

# Mapeo de modelos Gemini compatibles
modelo_ids = {
    "Gemini 2.5 Flash": "gemini-2.5-flash-preview-04-17",
    "Gemini 2.0 Flash": "gemini-2.0-flash",
    "Gemini 2.0 Pro": "gemini-2.0-pro-exp-02-05",
    "Gemini 2.0 Flash Thinking": "gemini-2.0-flash-thinking-exp-01-21",
    "Gemini": "gemini-exp-1206",
    "Gemini 1.5 Pro": "gemini-exp-1206",
    "Gemini 1.5 Flash-8B": "gemini-1.5-flash-8b"
}

# Prompt cinematográfico base
DEFAULT_PROMPT_BASE = 'Generate a detailed and chronological description of a 5-second cinematic clip. Start immediately with the main action in one clear sentence. Include specific movements, gestures, or physical actions (e.g., a hand reaching, a bird taking flight). Describe the protagonist character or object in detail: clothing, colors, style, facial expressions, or textures. Accurately portray the environment or background: urban setting, weather, time of day, interior/exterior. Specify camera angles (close-up, wide shot, low angle), lens movement (zoom in, tracking shot, dolly out), and transitions. Define the lighting type (soft, neon, natural, dramatic) and dominant color tones. Mention any sudden changes (flash of light, shadow movement, motion blur) in sequence. Use technical filmmaking language. Avoid metaphors, abstractions, or vague terms. Keep everything in a single fluid paragraph. Max 200 words.'

class GeminiTextToCinematicPromptNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_text": ("STRING", {"default": "", "multiline": True}),
                "api_key": ("STRING", {"default": "", "multiline": False}),
                "modelo_select": (list(modelo_ids.keys()),),
                "prompt_base": ("STRING", {
                    "default": DEFAULT_PROMPT_BASE,
                    "multiline": True
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "generate_prompt"
    CATEGORY = "Gemini"

    def generate_prompt(self, input_text, api_key, modelo_select, prompt_base):
        try:
            genai.configure(api_key=api_key)
        except Exception as e:
            raise ValueError(f"Error configuring Gemini API: {e}")

        selected_model_id = modelo_ids.get(modelo_select)
        if not selected_model_id:
            raise ValueError(f"Model not found: {modelo_select}")

        model = genai.GenerativeModel(selected_model_id)
        full_prompt = f"{prompt_base}\n\nInput Text:\n{input_text}"

        try:
            response = model.generate_content(full_prompt)
        except Exception as e:
            raise ValueError(f"Error during Gemini content generation: {e}")

        # Validación robusta del contenido
        try:
            generated_prompt = response.candidates[0].content.parts[0].text
        except (IndexError, AttributeError):
            generated_prompt = "No valid prompt was generated."
        print(generated_prompt)
        return (str(generated_prompt),)
