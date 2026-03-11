from email import message
import os
import json
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


# ------------------------- Page settings -------------------------

st.set_page_config(
    page_title="AI Pair Engineer",
    page_icon="💻",
    layout="wide",
)

# st.title("💻 AI Pair Engineer")
# st.write("Paste a code snippet and receive AI suggestions before human code review.")

# ------------------------- Custom Styling -------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}
.main-title {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom:0.7rem;
}
.subtitle {
    font-size: 1.05rem;
    color: #A0A0A0;
    margin-bottom: 1.6rem;
}
.section-card {
    background: #111827;
    border: 1px solid #2A2F3A;
    border-radius: 16px;
    padding: 1.2rem 1.2rem 1rem 1.2rem;
    margin-bottom: 1rem;

}
.card-title {
    font-size: 1.05rem;
    font-weight: 600;
    margin-bottom: 0.8rem;
}
.small-note {
    font-size: 0.92rem;
    color: #9CA3AF;
}
.result-label {
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 0.7rem;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 3rem;
    font-weight: 600;
}

.stTextArea textarea {
    font-family: Consolas, Monaco, monospace;
    font-size: 14px;
}

.badge {
    display: inline-block;
    padding: 0.25rem 0.6rem;
    border-radius: 999px;
    background: #1F2937;
    border: 1px solid #374151;
    font-size: 0.82rem;
    margin-right: 0.4rem;
    color: #D1D5DB;
}
</style>
""", unsafe_allow_html=True)

# ------------------------- Header -------------------------

st.markdown('<div class="main-title">💻 AI Pair Engineer</div>',
            unsafe_allow_html=True)
st.markdown('<div class="subtitle">A lightweight AI assistant that reviews short code snippets for code quality, maintainability, testing, and developer experience before human review.</div>',
            unsafe_allow_html=True)
st.markdown(
    """
    <span class="badge">Readability</span>
    <span class="badge">Maintainability</span>
    <span class="badge">Testing</span>
    <span class="badge">Refactoring</span>
    <span class="badge">UX Suggestions</span>
    """,
    unsafe_allow_html=True)

# ------------------------- Sidebar -------------------------
with st.sidebar:
    st.header("About")
    st.write("This prototype acts like an AI pair engineer. "
             "It reviews code and returns practical, technical suggestions before team review."
             )
    st.subheader("What it returns:")
    st.write("- Code quality issues")
    st.write("- Exactly 3 improvements")
    st.write("- UX improvements if relevant")
    st.write("- Suggested test cases")
    st.write("- A technical positive note")
    st.write("- A refactored version")

    st.header("Best for:")
    st.write("Short Python or JavaScript functions, components, or snippets.")

# ------------------------- Input Section -------------------------
left, right = st.columns([2.2, 1])

with left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Code Input</div>',
                unsafe_allow_html=True)

    language = st.selectbox(
        "Programming Language",
        ["Python", "JavaScript"],
        index=0,
    )

    sample_snippets = {
        "Python": """def calc(nums):
    total = 0
    for i in nums:
        total = total + i
    print(total)
""",
        "JavaScript": """function calc(nums) {
  let total = 0;
  for (let i = 0; i < nums.length; i++) {
    total += nums[i];
  }
  console.log(total);
}
"""
    }
    use_sample = st.checkbox("Load a sample snippet", value=True)

    code_input = st.text_area(
        "Paste your code snippet",
        value=sample_snippets[language] if use_sample else "",
        height=320,
        placeholder="Paste your code here..."
    )
    st.markdown('<div class="small-note">Tip: paste one focused function or component for the best review quality.</div>',
                unsafe_allow_html=True)
    review_clicked = st.button("Review Code")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Review Criteria</div>',
                unsafe_allow_html=True)
    st.write("The assistant checks whether the snippet:")
    st.write("- uses clear names")
    st.write("- separates responsibilities well")
    st.write("- handles edge cases")
    st.write("- can be tested easily")
    st.write("- supports good user experience where relevant")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Examples of UX-related feedback</div>',
                unsafe_allow_html=True)
    st.write("- user-facing errors are unclear")
    st.write("- loading states are missing")
    st.write("- empty states are not handled")
    st.write("- validation feedback is weak")
    st.write("- action names are not intuitive")
    st.markdown('</div>', unsafe_allow_html=True)


# # ------------------------- Language Selector -------------------------

# language = st.selectbox(
#     "Programming Language",
#     ["Python, JavaScript"]
# )

# # ------------------------- Code Input -------------------------

# code_input = st.text_area(
#     "Paste your code snippet here",
#     height=300,
#     placeholder="Paste your code here..."
# )

# ------------------------- AI Prompt -------------------------

def build_prompt(language: str, code: str) -> str:
    return f"""
You are a senior software engineer performing a professional code review.

The code provided is written in: {language}

Important rules:
- Review the code ONLY in the context of {language}.
- Do NOT suggest syntax or patterns from other languages.
- Assume the snippet belongs to a {language} codebase.

Your tasks:

1. Identify issues related to readability, structure, maintainability, or design.
2. Recommend exactly 3 meaningful improvements.
3. Suggest useful test cases relevant to {language}.
4. Suggest UX improvements if the code interacts with users.
5. Provide one technical positive note like a senior engineer.
6. Provide a cleaner refactored version of the code in {language}.

Return ONLY valid JSON using this format:

{{
  "issues_found": [],
  "three_improvements": [],
  "ux_improvements": [],
  "suggested_tests": [],
  "positive_note": "",
  "refactored_code": ""
}}

Code:
```{language.lower()}
{code}
```"""
# ------------------------- Fallback Review -------------------------


# def fallback_review(language: str, code: str) -> dict:
#     ux_improvements = []
#     code_lower = code.lower()

#     if any(
#         keyword in code_lower
#         for keyword in ["input", "form", "button", "onclick", "submit", "alert", "render", "display"]

#     ):
#         ux_improvements.append("Add clearer validation or feedback for invalid user input.",
#                                "Ensure the user sees a meaningful state when an action succeeds or fails."
#                                )

#         suggested_tests = []
#         if language == "Python":
#             suggested_tests = [
#                 "Test the function with expected valid input and verify the returned result.",
#                 "Test empty or missing input to confirm the function handles it safely.",
#                 "Test invalid input types and verify the function fails predictably or validates input."
#             ]
#         else:
#             suggested_tests = [
#                 "Test the function with expected valid input and verify the output or side effect.",
#                 "Test empty or undefined input to confirm safe handling.",
#                 "Test invalid data types and verify the code handles them defensively."
#             ]

#         return {
#             "issues_found": [
#                 "The snippet could separate computation logic from output or side effects more clearly.",
#                 "Naming and structure could be improved to make the code easier to scan quickly.",
#                 "Edge cases and invalid inputs are not clearly handled."
#             ],
#             "three_improvements": [
#                 "Use more descriptive function and variable names to improve readability.",
#                 "Move core logic into smaller reusable units where appropriate.",
#                 "Add explicit handling for edge cases and invalid inputs."
#             ],
#             "ux_improvements": ux_improvements,
#             "suggested_tests": suggested_tests,
#             "positive_note": "The snippet keeps the logic focused on a single task, which is a good starting point for maintainable code.",
#             "refactored_code": code
#         }

def fallback_review(language: str, code: str) -> dict:
    ux_improvements = []
    code_lower = code.lower()

    if any(
        keyword in code_lower
        for keyword in ["input", "form", "button", "onclick", "submit", "alert", "prompt", "render", "display"]
    ):
        ux_improvements = [
            "Add clearer validation or feedback for invalid user input.",
            "Ensure the user sees a meaningful state when an action succeeds or fails."
        ]

    if language == "Python":
        suggested_tests = [
            "Test the function with expected valid input and verify the returned result.",
            "Test empty or missing input to confirm the function handles it safely.",
            "Test invalid input types and verify the function fails predictably or validates input."
        ]
    else:
        suggested_tests = [
            "Test the function with expected valid input and verify the output or side effect.",
            "Test empty or undefined input to confirm safe handling.",
            "Test invalid data types and verify the code handles them defensively."
        ]

    return {
        "issues_found": [
            "The snippet could separate computation logic from output or side effects more clearly.",
            "Naming and structure could be improved to make the code easier to scan quickly.",
            "Edge cases and invalid inputs are not clearly handled."
        ],
        "three_improvements": [
            "Use more descriptive function and variable names to improve readability.",
            "Move core logic into smaller reusable units where appropriate.",
            "Add explicit handling for edge cases and invalid inputs."
        ],
        "ux_improvements": ux_improvements,
        "suggested_tests": suggested_tests,
        "positive_note": "The snippet keeps the logic focused on a single task, which is a good starting point for maintainable code.",
        "refactored_code": code
    }


# ------------------------- AI Review -------------------------

# def review_code(language: str, code: str) -> dict:
#     try:
#         client = OpenAI()

#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             response_format={"type": "json_object"},
#             messages=[
#                 {
#                     "role": "system",
#                     "content": "You are a precise senior software engineer who returns strict JSON only."
#                 },
#                 {
#                     "role": "user",
#                     "content": build_prompt(language, code)
#                 }
#             ],
#             temperature=0.2
#         )

#         text = response.choices[0].message.content.strip()
#         parsed = json.loads(text)

#         parsed.setdefault("issues_found", [])
#         parsed.setdefault("three_improvements", [])
#         parsed.setdefault("ux_improvements", [])
#         parsed.setdefault("suggested_tests", [])
#         parsed.setdefault("positive_note", "")
#         parsed.setdefault("refactored_code", code)

#         return parsed

#     except Exception:
#         st.warning(
#             "OpenAI response unavailable, so a local fallback review was used.")
#         return fallback_review(language, code)

def review_code(language: str, code: str) -> dict:
    try:
        client = OpenAI()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": "You are a precise senior software engineer who returns strict JSON only."
                },
                {
                    "role": "user",
                    "content": build_prompt(language, code)
                }
            ],
            temperature=0.2
        )

        text = response.choices[0].message.content.strip()
        parsed = json.loads(text)

        parsed.setdefault("issues_found", [])
        parsed.setdefault("three_improvements", [])
        parsed.setdefault("ux_improvements", [])
        parsed.setdefault("suggested_tests", [])
        parsed.setdefault("positive_note", "")
        parsed.setdefault("refactored_code", code)

        return parsed

    except Exception as e:
        st.warning(
            f"OpenAI response unavailable, so a local fallback review was used. Error: {e}")
        return fallback_review(language, code)


# ------------------------- Output Section -------------------------

if review_clicked:
    if not code_input.strip():
        st.warning("Please paste a code snippet first.")
    else:
        with st.spinner("Reviewing code..."):
            result = review_code(language, code_input)

        st.write("")
        st.subheader("Review Results")

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="result-label">Issues Found</div>',
                        unsafe_allow_html=True)
            for issue in result.get("issues_found", []):
                st.write(f"• {issue}")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown(
                '<div class="result-label">Three Improvements</div>', unsafe_allow_html=True)
            for item in result.get("three_improvements", []):
                st.write(f"• {item}")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown(
                '<div class="result-label">Suggested Tests</div>', unsafe_allow_html=True)
            for test in result.get("suggested_tests", []):
                st.write(f"• {test}")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_b:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown(
                '<div class="result-label">UX Improvements</div>', unsafe_allow_html=True)
            ux_items = result.get("ux_improvements", [])
            if ux_items:
                for ux in ux_items:
                    st.write(f"• {ux}")
            else:
                st.write(
                    "• No direct UX improvements were identified for this snippet.")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown(
                '<div class="result-label">Technical Positive Note</div>', unsafe_allow_html=True)
            st.info(result.get("positive_note", "No positive note returned."))
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-label">Refactored Code</div>',
                    unsafe_allow_html=True)
        st.code(result.get("refactored_code", ""), language=language.lower())
        st.markdown('</div>', unsafe_allow_html=True)

# def review_code(language: str, code: str) -> dict:
#     try:
#         client = OpenAI()

#         prompt = build_ai_prompt(language, code)

#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": "You are a professional code reviewer."},
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.3
#         )

#         text = response.choices[0].message.content

#         start = text.find("{")
#         end = text.rfind("}") + 1

#         json_text = text[start:end]

#         return json.loads(json_text)

#     except Exception as e:
#         st.error(f"AI request failed. Showing basic fallback response.")

#         return {
#             "issues_found": [
#                 "Code could benefit from clearer function separation",
#                 "Consider improving variable naming",
#                 "Edge cases may not be handled"
#             ],
#             "three_improvements": [
#                  "Use descriptive variable names",
#                 "Break logic into smaller functions",
#                 "Add comments explaining key logic"
#             ],
#             "suggested_tests": [
#                 "Test user creation with different data types",
#                 "Test user update with invalid input",
#                 "Test user deletion with non-existent user"
#             ],
#             "positive_note": "Code is generally well-structured and easy to follow.",
#             "refactored_code": code
#         }

# # ------------------------- Review button -------------------------
# if st.button("Review Code"):

#     if code_input.strip() == "":
#         st.warning("Please paste your code snippet first.")

#     else:
#         with st.spinner("Reviewing code..."):

#             result = review_code(language, code_input)

#         st.success("Code review complete!")

#         col1, col2 = st.columns(2)

#         with col1:
#             st.subheader("Issues Found")

#             for issue in result["issues_found"]:
#                 st.write("•", issue)

#             st.subheader("Three Improvements")

#             for improvement in result["three_improvements"]:
#                 st.write("•", improvement)

#             st.subheader("Suggested Tests")

#             for test in result["suggested_tests"]:
#                 st.write("•", test)

#             with col2:

#                 st.subheader("Positive Note")

#                 st.info(result["positive_note"])

#                 st.subheader("Refactored Code")

#                 st.code(result["refactored_code"], language=language.lower())
