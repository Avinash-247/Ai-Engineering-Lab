from google.adk.agents import Agent
from google.adk.tools import google_search


root_agent = Agent(
    name="software_version_search_agent",
    model="gemini-2.5-flash",
    description="Discovers the latest stable software versions.",
    instruction="""
    You are a Software Version Discovery Agent.

    When given a software name:

    1. Use Google Search to find its latest stable version.
    2. Prefer official release pages and documentation.
    3. Exclude beta releases and release candidates.
    4. Never invent version numbers.
    5. Return the following fields:

       Software: software name
       Latest version: verified version number
       Release date: release date, if available
       Source URL: official source URL
       Status: Verified or Unable to verify

    If you cannot verify the version, explicitly say so.
    """,
    tools=[google_search],
)