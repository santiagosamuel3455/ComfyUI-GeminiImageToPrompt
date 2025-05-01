class ShowGeneratedText:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "generated_text": ("STRING", {"default": "Texto generado...", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("edited_text",)
    FUNCTION = "show_and_edit_text"
    CATEGORY = "utils"
    DESCRIPTION = "Muestra el texto generado y permite editararlo."

    def show_and_edit_text(self, generated_text):
        # Muestra el texto y lo devuelve como salida
        print(f"Texto generado: {generated_text}")
        return (generated_text,)

