# AI Pair Engineer

**AI Pair Engineer** is a lightweight AI-assisted code review tool that helps developers improve short code snippets before human review.

The application analyzes a piece of Python or JavaScript code and returns structured feedback including code quality issues, maintainability improvements, suggested test cases, and a refactored version of the code.

This project demonstrates how AI can act as a **pair programming assistant**, helping developers identify potential problems early and improve code quality before submitting changes for review.

---

## Features

- **Code Quality Review**  
  Detects readability, structure, and maintainability issues in a snippet.

- **Three Targeted Improvements**  
  Returns exactly three meaningful suggestions to improve the code.

- **UX Awareness**  
  Highlights potential user-experience improvements when the code affects user interaction.

- **Suggested Test Cases**  
  Recommends practical tests developers should implement.

- **Technical Positive Note**  
  Includes one professional observation written like a senior engineer reviewing the code.

- **Refactored Version**  
  Generates a cleaner version of the submitted code.

- **Language Awareness**  
  The review adapts to the selected programming language (Python or JavaScript).

- **Fallback Review Mode**  
  If the OpenAI API is unavailable, the tool still provides a basic local review.

---

## Demo

Paste a short function or component into the interface and click **Review Code** to receive structured feedback.

Example snippet:

```python
def calc(nums):
    total = 0
    for i in nums:
        total = total + i
    print(total)
```

Example feedback:

```
Issues Found
• Computation logic is coupled with output, reducing testability.
• Edge cases such as empty input are not handled.
• Variable naming could be more descriptive.

Three Improvements
• Return values instead of printing output.
• Handle empty inputs safely.
• Use Python built-in functions for clarity.

Suggested Tests
• Normal list input
• Empty list input
• Invalid input types
```

---

## Tech Stack

- **Python**
- **Streamlit** – interactive UI for the tool
- **OpenAI API** – AI code review generation
- **JSON structured responses** – reliable parsing of AI output

---

## Project Structure

```
ai-pair-engineer
│
├── app.py            # Main Streamlit application
├── requirements.txt  # Project dependencies
├── README.md
└── .gitignore
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/ai-pair-engineer.git
cd ai-pair-engineer
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment:

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## OpenAI API Setup

Create an API key from:

https://platform.openai.com/api-keys

Set the environment variable.

### PowerShell

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

Then run the app:

```bash
streamlit run app.py
```

---

## Why This Project

Code review is one of the most valuable but time-consuming parts of software development.

This prototype explores how an AI assistant can act as a **pre-review step**, helping developers:

- catch issues earlier
- improve readability and maintainability
- think about test coverage
- produce cleaner code before human review

The goal is not to replace human review, but to **augment developer workflows**.

---

## Future Improvements

Potential enhancements for this prototype include:

- Code quality scoring system
- Severity levels for detected issues
- Before vs after code comparison
- Support for additional programming languages
- GitHub pull request integration
- Automated test generation

---

## Author

**Sara Mahran**  
Software Engineer | Coding Instructor

GitHub:  
https://github.com/SaraMahran
