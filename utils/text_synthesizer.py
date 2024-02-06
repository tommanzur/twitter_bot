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
            "Crea un mensaje de twitter ingenioso y muy gracioso "
            "para la noticia que te presento a continuación. "
            "Utiliza un estilo de escritura irónico, sobrador y canchero. "
            "Un estilo de escritura que se corresponda con un joven argentino. "
            "Incluye al menos 4 hashtags relevantes al final del mensaje. "
            "El mensaje debe ser gracioso y con clara orientación política, "
            "además debe estar estructurado como un chiste. Que tenga un límite máximo "
            "de 280 caracteres incluyendo los hashtags. "
            "Noticia: "
        )

        text_with_instructions = instructions + text
        response = self.model.generate_content(text_with_instructions)
        try:
            return response.text
        except:
            return None


    def synthesize_reply(self, comment_text):
        """
        Generates a witty and engaging reply for a given comment using the Gemini API.

        The method appends predefined instructions to the input comment text and 
        sends it to the Gemini API for synthesis. It returns the synthesized reply 
        or None if the process fails.

        Args:
            comment_text (str): The text of the comment to reply to.

        Returns:
            str or None: The synthesized reply or None if synthesis fails.
        """
        instructions = (
            "Genera una respuesta ingeniosa y atractiva para el siguiente comentario. "
            "La respuesta debe ser respetuosa, divertida y al mismo tiempo informativa, "
            "reflejando una postura amigable y positiva. "
            "Que tenga un límite máximo de 280 caracteres. "
            "Comentario: "
        )

        text_with_instructions = instructions + comment_text
        response = self.model.generate_content(text_with_instructions)
        try:
            return response.text
        except:
            return None