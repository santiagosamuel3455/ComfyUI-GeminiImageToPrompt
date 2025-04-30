# __init__.py

# Importar los nodos personalizados
from .gemini_prompt_node import GeminiImageToPromptNode
from .gemini_text_to_prompt_node import GeminiTextToCinematicPromptNode

# Mapeo interno de clases de nodos para ComfyUI
NODE_CLASS_MAPPINGS = {
    "GeminiImageToPromptNode": GeminiImageToPromptNode,
    "GeminiTextToCinematicPromptNode": GeminiTextToCinematicPromptNode
}

# Nombres que mostrará la UI de ComfyUI para estos nodos
NODE_DISPLAY_NAME_MAPPINGS = {
    "GeminiImageToPromptNode": "Gemini Image to Prompt",
    "GeminiTextToCinematicPromptNode": "Gemini Text to Cinematic Prompt"
}
