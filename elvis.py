import ollama_request as oll_req
context = ""

# _ = oll_req.communicate_with_ollama(oll_req.System_prompt)

print(20*"=")
print("Welcome to Elvis")
print(20*"=")

print("\nTeach me!")

user_input = input("User > ")
if user_input.lower() == "/exit":
    exit(0)

while True:
    question = oll_req.new_question(context, user_input)
    print("Elvis >", question)
    user_answer = input("User > ")
    if user_answer.lower() == "/exit":
        break
    context = oll_req.update_context(question, user_answer, context)
    print("\n\n",context,"\n\n")
