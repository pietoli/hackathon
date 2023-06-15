from pathlib import Path

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)


def get_prompt_template(
    user_prompt_template: str, system_prompt_template: str, input_vars: list[str]
) -> ChatPromptTemplate:
    if system_prompt_template is None:
        with open(Path(__file__).parent / "prompts" / "system.prompt") as f:
            system_template = f.read().strip()
    else:
        system_template = system_prompt_template

    if user_prompt_template is None:
        with open(Path(__file__).parent / "prompts" / "user.prompt") as f:
            human_template = f.read().strip()
    else:
        human_template = user_prompt_template

    return ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template(human_template),
        ],
        input_variables=input_vars,
    )


def get_human_template() -> str:
    with open(Path(__file__).parent / "prompts" / "user.prompt") as f:
        return f.read().strip()


def get_system_template() -> str:
    with open(Path(__file__).parent / "prompts" / "system.prompt") as f:
        return f.read().strip()
