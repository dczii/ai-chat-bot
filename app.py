from llm_api import openai_chatbot_chain
import chainlit as cl

SYSTEM_PROMPT = (
    "You are an expert lawyer specializing in AI bills in the Philippines. "
    "Always interpret ambiguous or follow-up questions as referring to AI-related bills and continue the same topic "
    "unless the user explicitly switches subjects. "
    "Answer strictly about AI-related bills from the Philippines. "
    "If the question is not related to AI Bills, reply:\n"
    "'I don't know. I can only answer questions related to AI bills based from the Philippines.' "
)

@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="DICT & AI Curriculum",
            message="What does the Department of Information and Communications Technology do in the age-appropriate curriculum modules and why is it important for the Philippines to act now?",
            icon="https://www.svgrepo.com/show/417125/idea.svg",
        ),
        cl.Starter(
            label="AI in PH Schools",
            message="How does the Philippines plan to incorporate AI education into its elementary and secondary curriculum?",
            icon="https://www.svgrepo.com/show/417125/idea.svg",
        ),
        cl.Starter(
            label="AI Roadmap & Registration",
            message="How does the development of the philippine ai roadmap relate to futures thinking and the registration of ai systems in the philippines?",
            icon="https://www.svgrepo.com/show/417125/idea.svg",
        ),
    ]

#|--------------------------------------------------------------------------|
#|                            On Boarding                                   |
#|--------------------------------------------------------------------------|
@cl.on_chat_start
async def on_chat_start():
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