from gpt_liquid.pca import ProstateCancer, PCA_EXAMPLES
from gpt_liquid.gpt import generate_template
from utils import make_key_value_table, make_quote
import streamlit as st

value = st.sidebar.selectbox(
    "Example cases",
    [("Prostate cancer", (ProstateCancer, PCA_EXAMPLES))],
    format_func=lambda case: case[0],
)
api_key = st.sidebar.text_input("OpenAI API key", type="password")

assert isinstance(value, tuple), "Value should be a tuple"
name, (Model, examples) = value

if "examples" not in st.session_state:
    st.session_state.examples = examples

st.title("Generate Liquid templates using GPT")

current_examples: list[tuple[Model, str]] = st.session_state.examples
assert current_examples is not None and isinstance(
    current_examples, list
), "Examples should be a list"

st.header("Examples")
for i, (data, text) in enumerate(current_examples):
    st.markdown(f"**Example {i+1}**")
    st.markdown(make_key_value_table(data.model_dump()))
    st.markdown(make_quote(text))
    st.button(
        "Remove example",
        key=f"remove_example_{i}",
        on_click=lambda: st.session_state.examples.remove((data, text)),
    )

with st.form("example"):
    st.markdown("**New example**")
    for field in Model.model_fields.keys():
        st.text_input(field, key=field)
    st.text_area("Text", key="text")
    st.form_submit_button(
        "Add example",
        on_click=lambda: st.session_state.examples.append(
            (
                ProstateCancer.model_validate_json(st.session_state.json),
                st.session_state.text,
            )
        ),
    )

should_generate_template = st.button(
    "Generate template",
)

if should_generate_template:
    if not st.session_state.examples:
        st.error("Please add at least one example")
        st.stop()
    template = generate_template(
        Model, examples=st.session_state.examples, api_key=api_key
    )
    st.header("Generated template")
    st.markdown(template)
