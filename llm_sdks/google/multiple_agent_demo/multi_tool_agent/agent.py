from google.adk.agents.llm_agent import Agent



def get_weather(city:str="khammam")->dict:
    location={
        "khammam":"very cloudy",
        "chennai":"very hot",
        "Hyderbad":"moderate",
    }
    return {city:location.get(city,"data not available")}

def get_time(city:str="khammam")->dict:
    location_time={
        "khammam":"19:00",
        "chennai":"17:00",
        "Hyderbad":"8:00",
    }
    return {city:location_time.get(city,"no data found")}


root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    # description='A helpful assistant for user questions.',
    description="Agent to answer question about the time and wether.",
    # instruction='''
    # you are a friendly programming and Ai tutor.
    # first identify the learner's requested teachinf mode.
    # modes:
    # 1:Detailed Explination:
    # Example step-by step with examplease and code.
    # 2: quick revision:
    # Given concise notes , key ponts and interview answers,
    # 3.explain like i'm lo:
    # use simple words and drealtable analogies.
    # ''',
    instruction="you are a helpful agent who can answer user question about the time and wether in a city",
    tools=[get_weather,get_time],
)

