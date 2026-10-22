# from google.adk.agents import Agent
# from google.adk.tools import google_search
# from .auther1 import get_author
# INSTRUCTION = """\
# You find the latest STABLE release of a software product using web search only.

# You will receive one software entry with: name, optional currently-installed
# version, and an optional reference URL.

# Rules:
# - Search the web. Prefer official sources (vendor site, official download or
#   release page, official GitHub releases, official docs). If a reference URL
#   is given, search for that site/domain first (e.g. "site:example.com release").
# - Ignore beta, RC, nightly, preview and LTS-vs-current confusion: report the
#   latest stable release, and mention an LTS version in "notes" if one exists
#   separately (e.g. Node.js).
# - Do not guess or use memory. If you cannot confirm a version from search
#   results, set latest_version to "NOT_FOUND".
# - If a current version was provided, set status to "up-to-date" or
#   "outdated" by comparing it with latest_version; otherwise use "unknown".

# Respond with ONLY a single JSON object, no markdown fences, no extra text:
# {
#   "name": "...",
#   "latest_version": "...",
#   "release_date": "YYYY-MM-DD or empty",
#   "status": "up-to-date | outdated | unknown",
#   "source_url": "page where you confirmed the version",
#   "notes": "short note or empty"
# }
# """


# root_agent = Agent(
#     name="software_version_checker",
#     model="gemini-2.5-flash",
#     description="Finds the latest stable version of a software product via web search.",
#     instruction=INSTRUCTION,
#     tools=[get_author],
# )

from pathlib import Path
from pypdf import PdfReader
from google.adk.tools import function_tool
import asyncio


def get_author(path: str) -> str:
    """Extract the author name from a PDF file's metadata."""

    pdf_path = Path(path)

    if not pdf_path.is_absolute():
        pdf_path = Path(__file__).parent / pdf_path

    if not pdf_path.exists():
        return f"PDF file not found: {pdf_path}"

    reader = PdfReader("sample_ai_author.pdf")
    metadata = reader.metadata

    if metadata and metadata.author:
        return metadata.author

    return "Author name not found in PDF metadata"

custom_tool=function_tool(func=get_author)




from google.adk.agents.llm_agent import Agent

async def main():
    custom_tool=function_tool(func=get_author)
    root_agent = Agent(
        name="software_version_agent",
        model="gemini-2.5-flash",
        instruction="""
            You are a PDF author information assistant.

            You have access to a tool named get_author.

        The PDF file sample_ai_author.pdf is located in the same
        directory as the get_author function.

        When the user asks for the author of this PDF:
        1. Call get_author with path="sample_ai_author.pdf".
        2. Do not ask the user to provide the path.
        3. Return the result from the tool.
""",
        tools=[custom_tool],
    )



if __name__ =="__main__":
    asyncio.run(main())