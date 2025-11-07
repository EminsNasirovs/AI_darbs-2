import os
from openai import OpenAI
from dotenv import load_dotenv

class ChatbotService:
    def __init__(self):
        # TODO: 1. SOLIS - API atslēgas ielāde
        # load_dotenv(), lai ielādētu mainīgos no .env faila.
        # os.getenv(), lai nolasītu "HUGGINGFACE_API_KEY".

        # TODO: 2. SOLIS - OpenAI klienta inicializācija izmantojot "katanemo/Arch-Router-1.5B" modeli
        self.client = None

        # TODO: 3. SOLIS - Sistēmas instrukcijas definēšana
        self.system_instruction = (
        )

    def get_chatbot_response(self, user_message, chat_history=None):
        if chat_history is None:
            chat_history = []
            
        # TODO: 4. SOLIS - Ziņojumu saraksta izveide masīvā
        # Tajā jābūt sistēmas instrukcijai, visai sarunas vēsture un pēdējai lietotāja ziņa.
        # 1. Sistēmas instrukcija (role: "system")
        # 2. Visa iepriekšējā sarunas vēsture (izmantojot .extend(), lai pievienotu visus elementus no chat_history)
        # 3. Pēdējā lietotāja ziņa (role: "user")
        
        # TODO: 5. SOLIS - HF API izsaukums ar OpenAI bibliotēku, izmantojot chat.completions.create().
        
        # TODO: 6. SOLIS - Atbildes apstrāde un atgriešana
        # chat.completions.create() atgriež objektu ar "choices" sarakstu, tajā jāparbauda, vai ir pieejama atbilde

        # Pagaidu atbilde, kas jāaizvieto ar reālo API atbildi tiklīdz būs implementēts.
        return {"response": "AI API response is not implemented yet."}
