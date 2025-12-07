document.addEventListener('DOMContentLoaded', () => {
    const chatbotToggler = document.querySelector(".chatbot-toggler");
    const closeBtn = document.querySelector(".close-btn");
    const chatbox = document.querySelector(".chatbox");
    const chatInput = document.querySelector(".chat-input textarea");
    const sendChatBtn = document.querySelector(".chat-input span");

    // 1. SOLIS: Izveidot mainīgo sarunas vēstures glabāšanai.
    // TODO: Izveidojiet mainīgo sarunas vēstures glabāšanai.
    let chatHistory = []; 

    const createChatLi = (message, className) => {
        const chatLi = document.createElement("li");
        chatLi.classList.add("chat", className);
        let chatContent = className === "outgoing" ? `<p></p>` : `<span class="material-symbols-outlined">smart_toy</span><p></p>`;
        chatLi.innerHTML = chatContent;
        chatLi.querySelector("p").textContent = message;
        return chatLi;
    }

    // 2. SOLIS: Implementēt funkciju, kas sazinās ar serveri.
    const generateResponse = (incomingChatLi) => {
        const API_URL = "/chatbot";
        const messageElement = incomingChatLi.querySelector("p");

        // TODO: Sagatavot pieprasījuma opcijas (request options)
        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            // Izveidojiet JSON virknes objektu, kas satur gan pēdējo lietotāja ziņu, gan visu iepriekšējo sarunas vēsturi.
            // Pēdējā ziņa jau ir iekļauta `chatHistory` masīva beigās funkcijā `handleChat`.
            body: JSON.stringify({
                // Jūsu servera pusei ir nepieciešama tikai pēdējā ziņa atsevišķi, bet mēs varam iegūt to no vēstures
                // Taču, lai būtu skaidrs un atbilstošs jūsu servera implementācijai, mēs izsūtām visu vēsturi un pēdējo ziņu.
                // Mēs izņemam pēdējo ziņu, jo tā ir lietotāja ziņa, un nosūtām atlikušo vēsturi.
                history: chatHistory.slice(0, -1), // visa vēsture, izņemot pēdējo (lietotāja) ziņu
                message: chatHistory[chatHistory.length - 1].content // Pēdējā (lietotāja) ziņa
            })
        };

        // TODO: Izsaukt `fetch()` ar izveidotajām opcijām.
        fetch(API_URL, requestOptions)
            .then(res => res.json())
            .then(data => {
                const botResponse = data.response;
                
                // 1. Atjaunojiet `messageElement` saturu ar saņemto atbildi.
                messageElement.textContent = botResponse;
                
                // 2. Pievienojiet bota atbildi mainīgajā sarunas vēstures glabāšanai.
                // Pievienojam sarunas vēsturei ar lomu "assistant"
                chatHistory.push({ role: "assistant", content: botResponse });
            })
            .catch(() => {
                messageElement.textContent = "Oops! Something went wrong. Please try again.";
            })
            .finally(() => {
                chatbox.scrollTo(0, chatbox.scrollHeight);
                // Pēc atbildes saņemšanas vajadzētu atkārtoti iespējot ievades lauku (ja tas tika atspējots)
                chatInput.disabled = false;
                sendChatBtn.disabled = false;
            });
    }

    const handleChat = () => {
        const userMessage = chatInput.value.trim();
        if(!userMessage) return;

        // Pagaidu atspējošana, kamēr AI atbild
        chatInput.disabled = true; 
        sendChatBtn.disabled = true;

        chatInput.value = "";
        chatInput.style.height = `auto`;

        chatbox.appendChild(createChatLi(userMessage, "outgoing"));
        chatbox.scrollTo(0, chatbox.scrollHeight);
        
        // 3. SOLIS: Pievienot lietotāja ziņu mainīgajā sarunas vēstures glabāšanai
        // TODO: Pievienojiet ziņu masīvam pareizajā formātā (kā objektu ar "role" un "content").
        chatHistory.push({ role: "user", content: userMessage });
        
        setTimeout(() => {
            const incomingChatLi = createChatLi("Thinking...", "incoming");
            chatbox.appendChild(incomingChatLi);
            chatbox.scrollTo(0, chatbox.scrollHeight);
            // Izsaucam atbildes ģenerēšanas funkciju
            generateResponse(incomingChatLi);
        }, 600);
    }

    chatInput.addEventListener("input", () => {
        chatInput.style.height = `auto`;
        chatInput.style.height = `${chatInput.scrollHeight}px`;
    });

    chatInput.addEventListener("keydown", (e) => {
        if(e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
            e.preventDefault();
            handleChat();
        }
    });

    sendChatBtn.addEventListener("click", handleChat);
    closeBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
    chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));
});