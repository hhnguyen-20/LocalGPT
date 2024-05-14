from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
import chainlit as cl
import logging


# Logging setup
def setup_logging():
    """
    Sets up the logging configuration for the chatbot.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def log_event(event: str) -> None:
    """
    Logs an event message.
    """
    logging.info(event)


def log_error(error: str) -> None:
    """
    Logs an error message.
    """
    logging.error(error)


setup_logging()  # Set up logging


async def handle_error(context: str, exception: Exception) -> None:
    """
    Handles an error by logging the error message and sending an error message to the user.
    """
    error_message = f"An error occurred in {context}: {str(exception)}"
    log_error(error_message)
    await cl.Message(content=error_message).send()


def get_runnable_session() -> Runnable:
    """
    Retrieves the runnable session from the user session.
    """
    return cl.user_session.get("runnable")


def set_runnable_session(runnable: Runnable) -> None:
    """
    Stores the runnable session in the user session.
    """
    cl.user_session.set("runnable", runnable)


def validate_input(input_text: str) -> bool:
    """
    Validates the input text by checking if it is not empty or only contains whitespace.
    """
    return bool(input_text and input_text.strip())


@cl.on_chat_start
async def on_chat_start() -> None:
    """
    Initializes the chatbot by sending an image and setting the runnable session.
    """
    try:
        # Sending an image with the local file path
        elements = [
            cl.Image(name="image1", display="inline", path="images/hung_jr.jpg")
        ]
        await cl.Message(content="Hello there, I am Hung Junior. How can I help you?", elements=elements).send()

        # Initialize the language model and prompt template
        model = Ollama(model="hung_jr")
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system",
                 "You're a very knowledgeable chatbot who provides accurate and eloquent answers to questions."),
                ("human", "{question}"),
            ]
        )
        runnable = prompt | model | StrOutputParser()
        set_runnable_session(runnable)
        log_event("Chat started and runnable session set.")

    except Exception as e:
        await handle_error("chat initialization", e)


@cl.on_message
async def on_message(message: cl.Message) -> None:
    """
    Processes the user message by sending it to the language model and sending the response to the user.
    """
    try:
        if not validate_input(message.content):
            await cl.Message(content="Please enter a valid question.").send()
            return

        runnable: Runnable = get_runnable_session()
        msg = cl.Message(content="")

        async for chunk in runnable.astream(
                {"question": message.content},
                config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
        ):
            await msg.stream_token(chunk)

        await msg.send()
        log_event(f"Processed message: {message.content}")

    except Exception as e:
        await handle_error("message processing", e)
