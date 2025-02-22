import subprocess
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

class MessageGenerator:
    def __init__(self):
        self.base_temperature = 0.7
        self.temperature_increment = 0.1
        self.max_temperature = 1.0
        self.current_temperature = self.base_temperature
        
    def create_llm(self):
        return OllamaLLM(
            model="llama3.2", 
            base_url="http://localhost:11434",
            temperature=self.current_temperature
        )

    def increase_temperature(self):
        self.current_temperature = min(
            self.current_temperature + self.temperature_increment,
            self.max_temperature
        )
        
    def reset_temperature(self):
        self.current_temperature = self.base_temperature

    def generate_message(self, diff):
        llm = self.create_llm()
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Your task is to write a concise commit message according to a given code diff. Your output should only be the commit message with no other information."),
            ("user", "Code Diff: {query_diff} Commit Message:")
        ])
        chain = prompt | llm
        return chain.invoke({"query_diff": diff})

generator = MessageGenerator()

def get_diff():
    """Get the Git diff of staged changes."""
    result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    if result.stdout.strip() == "":
        print("No staged changes found. Please use 'git add' to stage your changes first.")
        return None
    return result.stdout

def generate_message(qdiff):
    """Generate a commit message using the Ollama LLM."""
    return generator.generate_message(qdiff)

def increase_creativity():
    """Increase the temperature for next generation."""
    generator.increase_temperature()

def reset_creativity():
    """Reset the temperature to base value."""
    generator.reset_temperature()

def main():
    """Main function to generate commit message."""
    diff = get_diff()
    if diff is None:
        return 1
    
    try:
        message = generate_message(diff)
        print(message.strip())
        return 0
    except Exception as e:
        print(f"Error generating commit message: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())