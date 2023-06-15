from langchain import LLMChain
from langchain.chat_models import ChatOpenAI
from pydantic import BaseSettings

from src.cli.utils import get_prompt_template


class OpenAISettings(BaseSettings):
    api_base: str
    api_organization: str
    api_key: str

    class Config:
        env_prefix: str = "openai_"


config = OpenAISettings()


def prepare_query(user_input: str) -> str:
    system_msg = "You are a virtual assistant preparing queries for search in PubMed from user input"
    user_msg = "Based on provided information prepare short statement in English to use in PubMed search API and check if it is a fact. Information: {content}"


    prompt = get_prompt_template(user_msg, system_msg, input_vars=['content'])
    chain = LLMChain(
        llm=ChatOpenAI(openai_api_key=config.api_key,openai_organization=config.api_organization,openai_api_base=config.api_base,temperature=0,
                       model_name="gpt-4"),
        prompt=prompt,
    )

    result = chain.run({"content": user_input})
    return result


def check_fact(
    query: str,
    context_data: str | None,
    user_prompt_template: str = None,
    system_prompt_template: str = None,
) -> str:
    prompt = get_prompt_template(user_prompt_template, system_prompt_template, input_vars = ["user_input", "context"])
    chain = LLMChain(
        llm=ChatOpenAI(openai_api_key=config.api_key,openai_organization=config.api_organization,openai_api_base=config.api_base,temperature=0,model_name="gpt-4"),
        prompt=prompt,
    )

    result = chain.run({"user_input": query, "context": context_data})
    return result
