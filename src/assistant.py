# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "ollama",
# ]
# ///
import ollama

class Assistant():
    def __init__(self, **kwargs):
        self.verbose: bool = kwargs.get('verbose', False)
        self.testing: bool = kwargs.get('testing', False)
        self.textResponseModel: str = kwargs.get('textResponseModel', "mistral")
        self.RAGEmbeddingModel: str = kwargs.get('RAGEmbeddingModel', "mistral")
        print(f"Assistant initialized.") if self.verbose else None

    def prompt(self, message: str) -> dict:
        print(f"Prompting assistant with message: {message}") if self.verbose else None

        if not self.testing:
            question = message
            context = ""
            formatted_prompt = f"Question: {question}\n\nContext: {context}"
            response = ollama.chat(model=self.textResponseModel, messages=[{"role": "user", "content": formatted_prompt }])
            output = response['message']['content']
        else:
            output = message
        
        return output
    
def new(**kwargs):
    """Create a new Assistant instance. Made for code readability."""
    return Assistant(**kwargs)