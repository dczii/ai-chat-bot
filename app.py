from llm_api import openai_chatbot_chain
import chainlit as cl

SYSTEM_PROMPT = (
    "You are an expert lawyer specializing in AI bills in the Philippines. "
    "Always interpret ambiguous or follow-up questions as referring to AI-related bills and continue the same topic "
    "unless the user explicitly switches subjects. "
    "Answer strictly using the provided context from AI-related bills. "
    "If the question is not related to AI Bills, reply:\n"
    "'I don't know. I can only answer questions related to AI bills based on the provided documents.' "
)

#|--------------------------------------------------------------------------|
#|                            On Boarding                                   |
#|--------------------------------------------------------------------------|
@cl.on_chat_start
async def on_chat_start():
    elements = [
        cl.Image(
            name="logo",
            display="inline",
            path="./static/Logo.png",
        )
    ]
    await cl.Message(content="Hello! Welcome to Danilo's Chatbot about AI Bills!", elements=elements).send()
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": SYSTEM_PROMPT}],
    )
    app_user = cl.user_session.get("user")

#|--------------------------------------------------------------------------|
#|                               Chat                                       |
#|--------------------------------------------------------------------------|
@cl.on_message
async def main(user_input: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": user_input.content})

    llm_output = cl.Message(content="")
    await llm_output.send()

    stream = await openai_chatbot_chain(message_history)

    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await llm_output.stream_token(token)

    message_history.append({"role": "assistant", "content": llm_output.content})
    await llm_output.update()