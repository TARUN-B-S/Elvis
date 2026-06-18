import ollama_request as oll_req
context = ""
history = ""
total_history = ""
# _ = oll_req.communicate_with_ollama(oll_req.System_prompt)

print(20*"=")
print("Welcome to Elvis")
print(20*"=")

print("\nTeach me!\n")

user_input = input("User > ")
if user_input.lower() == "/exit":
    exit(0)

while True:
    question = oll_req.new_question(history, context, user_input)
    print("Elvis >", question)
    user_answer = input("User > ")
    if user_answer.lower() == "/exit":
        break
    history+= f"Elvis: {question}\nTeacher: {user_answer}\n"
    if(len(history.split("\n")) > 10):
        context = oll_req.update_context(history, context)
        total_history+= history
        history = ""
    with open("conversation_history.txt", "w") as f:
        f.write(total_history + history)
    print("\n\n",context,"\n\n")
