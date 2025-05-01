class ShowTextNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": "", "multiline": True})
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "OUTPUT_TEXT"
    CATEGORY = "utils"
    DESCRIPTION = "Muestra el texto recibido y lo pasa a la siguiente etapa del flujo."

    # Este nodo no retorna nada, solo muestra el texto
    def OUTPUT_TEXT(self, text):
        print("Texto mostrado:", text)
        return ()  # No devuelve valores, solo sirve para visualizar