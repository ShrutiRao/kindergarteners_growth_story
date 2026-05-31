from tabs.comparison import render_comparison_tab
from tabs.history import render_history_tab
from tabs.intake import render_intake_tab


def create_app_shell():
    return {
        "title": "Kindergarten Growth Journey",
        "tabs": ["Input", "Historical Snapshot", "Comparison"],
    }


def inject_styles():
    import streamlit as st

    st.markdown(
        """
        <style>
            .stApp {
                background: linear-gradient(180deg, #f7fbff 0%, #ffffff 40%, #f8f4ef 100%);
            }
            h1, h2, h3 {
                letter-spacing: -0.02em;
            }
            .block-container {
                padding-top: 1.5rem;
                padding-bottom: 2rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    import streamlit as st

    from src.benchmarks import load_age_grade_standards

    st.set_page_config(page_title="Kindergarten Growth Journey", layout="wide")
    inject_styles()
    shell = create_app_shell()
    st.title(shell["title"])

    input_tab, history_tab, comparison_tab = st.tabs(shell["tabs"])

    with input_tab:
        render_intake_tab()

    with history_tab:
        render_history_tab()

    with comparison_tab:
        standards = load_age_grade_standards()
        render_comparison_tab(standards=standards)


if __name__ == "__main__":
    main()
