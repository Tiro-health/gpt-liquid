from typing import TypeVar, Type
from openai import OpenAI
from pydantic import BaseModel

TModel = TypeVar("TModel", bound=BaseModel)


def construct_system_message(model: Type[BaseModel]):
    keys = ", ".join(model.model_fields.keys())
    return (
        "You are a Liquid generation robot. You are very good at generating Liquid-templates and will output"
        + "only valid Liquid code that can be used directly by a Liquid template engine. The Liquid template engine will "
        + f"receive a object `data` with the following keys: {keys}."
    )


def generate_template(
    model: Type[TModel], examples: list[tuple[TModel, str]], *, api_key: str | None
) -> str:
    client = OpenAI(api_key=api_key)
    serialized_examples = [(data.model_dump_json(), text) for (data, text) in examples]
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": construct_system_message(model),
            },
            {
                "role": "user",
                "content": "\n\n".join(
                    [
                        f"""
                Give the following data 

                ```json
                {data} 
                ```
                
                I want to generate the following text:

                ```
                {text}
                ```
            """
                        for (data, text) in serialized_examples
                    ]
                ),
            },
            {
                "role": "system",
                "content": "Generate the liquide template that will output the text above without any extra text. The template should be valid liquid code.",
            },
        ],
        model="gpt-4",
    )
    template = chat_completion.choices[0].message.content

    assert template, "Template is empty"
    return template
