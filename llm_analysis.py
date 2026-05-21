import dotenv
from langchain_openai import AzureChatOpenAI
from dotenv import dotenv_values
from promps import PRIVACY_PROMPT

dotenv.load_dotenv()

apk_analysis_file = "./tik_tok_report.json"  # Path to your APK analysis file

llm = AzureChatOpenAI(
    azure_deployment="gpt-4o",
    api_version="2024-08-01-preview",  # or your api version
)

with open(apk_analysis_file, "r") as file:
    llm_analysis = file.read()

messages = [
    {
        "role": "system",
        "content": PRIVACY_PROMPT,
    },
    {
        "role": "user",
        "content": llm_analysis,
    },
]

llm_response = llm.invoke(
    messages
)

print(llm_response.content)

with open("llm_analysis.md", "w") as file:
    file.write(llm_response.content)
