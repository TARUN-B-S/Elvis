import requests

OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:1.5b"
MODEL_CONTEXT_FILE = ""

System_prompt = '''
    You are Elvis, a curious student and your teacher has teached you a concept.
    The questions should deepen the teacher's understanding of the topic and help them learn more about it.
    Only use facts that are provided by the teacher in their answers to your questions. Do not make up any facts or information that is not provided by the teacher. 
    Ask Curious Questions but not buggy or annoying ones. 
    Don't ask questions that resemble the previous questions. Always ask new questions that can help the teacher to explain the topic in a better way.
    Just ask the question with proper context rather than adding "Thank you" or "So, <question point again>" and things like that. 
    Be concise, and reply only with the exact reply for which the teacher can answer.
    Your only task is to ask questions with proper context. Not to answer them.
    Check the answer provided by the teacher, think about it, if any flaws are present, ask questions emphasizing the flaws.
    You will be given context, previous question and the answer that the teacher gave for you.
    Act upon it and only the information given in it.
    Never get out of your role and don't bring new information into the conversation if it is not already discussed by the teacher.
'''

Response_Types = '''
    1. If the teacher's explanation is abstracted you should ask them to explain it with more depth.
    2. What are the places in which the concept is being applied in real-life?
    3. What led to the invention of this/these concept(s)?
    4. What are the advantages and disadvantages of this/these concept(s)?
    5. Non Trivial results that can be derived from this/these concept(s) and how to derive them?
'''

def communicate_with_ollama(prompt):
    """
    Communicates with the Ollama API to generate a response based on the provided prompt.

    Args:
        prompt (str): The input prompt to send to the Ollama API.

    Returns:
        str: The generated response from the Ollama API.
    """

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        return response.json().get("response", "")
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Ollama API: {e}")
        return ""

def new_question(history, context, answer):
    """
    Generates a new question based on the teacher's answer.

    Args:
        answer (str): The teacher's answer to the last question.

    Returns:
        str: A new question generated based on the teacher's answer.
    """

    PROMPT = f'''
        System Prompt: {System_prompt}
        ----
        Things to remember while asking questions: {Response_Types}
        ----
        The History of the conversation so far is : {history if history else "No history available as of now"}
        ---
        The summary of the conversation so far is : {context if context else "No context avaiable as of now use history"}
        ----
        The teacher's answer to the last question is : {answer}
        ----
        Ask a question...
    '''

    new_question = communicate_with_ollama(PROMPT)
    return new_question

def update_context(history, context):
    """
    Updates the context of the conversation with the new question and answer.

    Args:
        question (str): The new question asked by the student.
        answer (str): The teacher's answer to the new question.
    """
    PROMPT = f'''
        The summary of the conversation so far is : {context}
        ----
        The new questions and answers in the conversation are: {history}
        ----
        Update the summary of the conversation so far with the new question and answer.
        Only include the facts don't include that the student was curious. Be Factual.
        Keep the summary concise and focused on the key points of the conversation.
        Strictly don't include any additional information that was not discussed in the conversation about the topic.
        Keep the word count of the summary less than 500 words.
    '''
    return communicate_with_ollama(PROMPT)