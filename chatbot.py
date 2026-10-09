import re
import time

class InteractiveBot:
    def __init__(self):
        self.state = "GREETING"
        self.user_data = {"name": None, "topic": None}
        
    def extract_email(self, text):
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(email_pattern, text)
        return match.group(0) if match else None

    def get_response(self, user_input):
        cleaned_input = user_input.strip().lower()

        if cleaned_input in ["exit", "quit", "bye"]:
            self.state = "ENDED"
            return "Goodbye! Have a wonderful day ahead."

        if self.state == "GREETING":
            if not cleaned_input:
                return "Hello! I am your Python chatbot. What is your name?"
            
            if "name is" in cleaned_input:
                name = user_input.split("name is")[-1].strip()
            elif "i am" in cleaned_input:
                name = user_input.split("i am")[-1].strip()
            else:
                name = user_input.strip()
                
            self.user_data["name"] = name
            self.state = "MAIN_MENU"
            return f"Nice to meet you, {name}! I can help you with a few things today.\nType one of these keywords:\n💬 'support' (to open a ticket)\nℹ️ 'info' (to learn about me)\n🔄 'clear' (to reset)"

        if self.state == "MAIN_MENU":
            if "info" in cleaned_input:
                return f"I am a rules-based chatbot built completely in standard Python without external libraries! What else can I help you with, {self.user_data['name']}?"
            
            elif "support" in cleaned_input:
                self.state = "AWAITING_EMAIL"
                return "To log a support ticket, please type your email address:"
            
            elif "clear" in cleaned_input:
                self.user_data = {"name": None, "topic": None}
                self.state = "GREETING"
                return "Conversation reset! Let's start over. What is your name?"
            
            else:
                return f"Sorry {self.user_data['name']}, I didn't quite catch that. Please type 'info', 'support', or 'clear'."

        if self.state == "AWAITING_EMAIL":
            email = self.extract_email(user_input)
            if email:
                self.state = "MAIN_MENU"
                return f"Thank you! A support representative will reach out to **{email}**. Returning to main menu. Need anything else?"
            else:
                return "That doesn't look like a valid email address. Please try entering it again (e.g., test@example.com):"

def run_chat():
    bot = InteractiveBot()
    print("==================================================")
    print("🤖 PYTHON CHATBOT SYSTEM INITIALISED")
    print("💬 (Type 'exit' or 'quit' at any time to shut down)")
    print("==================================================")
    
    print(f"\nBot: {bot.get_response('')}")

    while bot.state != "ENDED":
        try:
            user_msg = input("\nYou: ")
            print("Bot is typing...", end="\r")
            time.sleep(0.4)
            
            bot_reply = bot.get_response(user_msg)
            print(f"Bot: {bot_reply}")
            
        except (KeyboardInterrupt, EOFError):
            print("\nBot: Session interrupted. Goodbye!")
            break

if __name__ == "__main__":
    run_chat()
