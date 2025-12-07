import os
from openai import OpenAI
from dotenv import load_dotenv

class ChatbotService:
    def __init__(self, product_list_str=""):
        # TODO: 1. SOLIS - API atslēgas ielāde (Jau paveikts)
        load_dotenv()
        api_key = os.getenv("HUGGINGFACE_API_KEY")
        
        # TODO: 2. SOLIS - OpenAI klienta inicializācija (Jau paveikts)
        # Piezīme: Ja šo servisu inicializēs vairākas reizes ar dažādiem product_list_str, 
        # API atslēga un klients tiks inicializēts katru reizi. 
        # Ātrākai darbībai klientu varētu inicializēt ārpus klases vai vienreizēji (singleton).
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://router.huggingface.co/v1"
        )
        # Produkta saraksts tiek saglabāts
        self.product_list_str = product_list_str
        
        # TODO: 3. SOLIS - Sistēmas instrukcijas definēšana (Atjaunināts, lai iekļautu produktu sarakstu)
        self.system_instruction = self._define_system_instruction()

    def _define_system_instruction(self):
        """Definē sistēmas instrukciju, iekļaujot produktu sarakstu."""
        instruction = (
            "You are a helpful and **STRICT** e-commerce **CUSTOMER SUPPORT** assistant. "
        "Your sole purpose is to answer questions that are **DIRECTLY** related to the products available in the e-shop (pricing, descriptions, stock availability) or general e-shop services (shipping, orders). "
        "**You MUST NOT answer any general, philosophical, historical, or unrelated questions.** "
        "If the user asks about an off-topic subject, **RESPOND ONLY WITH THIS EXACT SENTENCE:** 'I apologize, I can only answer questions about our e-shop products and services. Please ask about a specific product or service.' "
        )
        
        # Pievienojam produktu sarakstu, ko padodam inicializatoram
        instruction += "\n" + (self.product_list_str if self.product_list_str else "Nav pieejama informācija par produktiem.")
            
        return instruction

    def get_chatbot_response(self, user_message, chat_history=None):
        response = self.client.chat.completions.create(
            model="katanemo/Arch-Router-1.5B",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        if chat_history is None:
            chat_history = []
            
        # Pārliecināmies, ka instrukcija ir atjaunināta ar jaunākajiem produktiem
        current_system_instruction = self._define_system_instruction()
            
        # TODO: 4. SOLIS - Ziņojumu saraksta izveide masīvā
        messages = [
            # 1. Sistēmas instrukcija (role: "system")
            {"role": "system", "content": current_system_instruction},
        ]
        
        # 2. Visa iepriekšējā sarunas vēsture (chat_history ir jābūt formātā [{"role": ..., "content": "..."}]
        messages.extend(chat_history)
        
        # 3. Pēdējā lietotāja ziņa (role: "user")
        messages.append({"role": "user", "content": user_message})

        try:
            # TODO: 5. SOLIS - HF API izsaukums ar OpenAI bibliotēku
            response = self.client.chat.completions.create(
                model="katanemo/Arch-Router-1.5B", 
                messages=messages,
                max_tokens=300, # Ieteicams ierobežot
                temperature=0.7 
            )
            
            # TODO: 6. SOLIS - Atbildes apstrāde un atgriešana
            if response.choices and response.choices[0].message:
                # Atgriežam modeļa atbildes tekstu
                return {"response": response.choices[0].message.content}
            else:
                # Ja atbildes nav (piemēram, tukša choices masīvs)
                return {"response": "Atbilde no modeļa nav saņemta. Lūdzu, mēģiniet vēlreiz."}

        except Exception as e:
            # Kļūdas apstrāde, piemēram, ja nav interneta vai nepareiza API atslēga
            print(f"Kļūda HF/OpenAI API izsaukumā: {e}")
            return {"response": f"Atvainojiet, radās kļūda saziņā ar MI servisu: {str(e)}"}