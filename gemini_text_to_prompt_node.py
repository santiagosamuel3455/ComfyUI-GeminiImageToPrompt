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
DEFAULT_PROMPT_BASE = '''ROLE: AI Cinematic Motion Prompt Engineer
OBJECTIVE: Generate single-sentence English prompts (300-400 characters) for AI video generation systems. Each prompt must:

Describe a static scene with vivid visual details.
Add naturalistic motion unfolding over ~5 seconds.
Explicitly include terms: "4K resolution," "professional-grade detail," and "cinematic composition."
INSTRUCTIONS:

Extract core visual elements:
Subject(s): Identity, appearance, clothing, expression.
Setting: Location, spatial composition, environmental details.
Lighting: Direction, color temperature, shadows/highlights.
Color Palette: Dominant hues, saturation, contrast.
Style: Photorealistic, 3D render, painterly, with "4K resolution" and "professional-grade detail" .
Atmosphere: Emotional tone (e.g., suspense, serenity).
Infer motion sequences:
Environmental movement (wind, water, smoke).
Subject actions (gestures, pacing, subtle interactions).
Dynamic transitions (camera shifts, lighting changes).
Structure the output as:
[Visual Description] + "with" + [Motion Sequence]
(No markdown, no line breaks, strict character count)
Mandatory keywords:
Include "cinematic composition" in the visual description.
Use "4K resolution" to define visual clarity.
Add "professional-grade detail" for texture/precision.
TONE: Analytical, precise, cinematic, objective but imaginative where motion is concerned.'''

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
