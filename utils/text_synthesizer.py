import google.generativeai as genai


class TextSynthesizer:
    """
    A class to interface with the Gemini API for text synthesis.

    Attributes:
        google_api_key (str): The API key for accessing Google's Gemini API.
        model (GenerativeModel): The Gemini generative model.
    """

    def __init__(self, google_api_key):
        """
        Initializes the TextSynthesizer with the necessary API configuration.

        Args:
            google_api_key (str): The API key for Google's Gemini API.
        """
        generation_config = {
            "temperature":0.5,
            "top_p":1,
            "top_k":1,
            "max_output_tokens":400
        }
        safetty_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]
        self.google_api_key = google_api_key
        genai.configure(api_key=self.google_api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-pro",
            generation_config=generation_config,
            safety_settings=safetty_settings
            )

    def synthesize_text(self, text):
        """
        Synthesizes a summary of the given text using the Gemini API.

        The method appends predefined instructions to the input text and 
        sends it to the Gemini API for synthesis. It returns the synthesized text 
        or None if the process fails.

        Args:
            text (str): The text to be summarized.

        Returns:
            str or None: The synthesized text summary or None if synthesis fails.
        """
        instructions = (
            "Crea un resumen en dos oraciones, ingenioso y atractivo "
            "en estilo argentino para la noticia que te presento a continuación. "
            "Utiliza un estilo de escritura irónico y canchero. "
            "Incluye al menos 4 hashtags relevantes al final del resumen. "
            "El resumen debe ser conciso y llamativo, con un límite máximo "
            "de 280 caracteres y mínimo de 160, para dejar espacio para el enlace del tweet. "
            "Noticia: "
        )

        text_with_instructions = instructions + text
        response = self.model.generate_content(text_with_instructions)
        try:
            return response.text
        except:
            return None
