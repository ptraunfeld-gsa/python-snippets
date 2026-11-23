
# OOP: 
class BaseAiAgent():
    def __init__(self):
        pass

class GSAiAgent(BaseAiAgent):
    ...

class USAiAgent(BaseAiAgent):
    ...


ai_agent : BaseAiAgent = get_ai_agent(...)


# Functional: 
def gsai_analyze(input_data: str, prompt: str) -> str:
    return "result"

def usai_analyze(input_data: str, prompt: str) -> str:
    return "result"


# Forwarder / Delegator
def ai_analyze(input_data: str, prompt: str) -> str:
    ai_agents = { 
        "gsai" : gsai_analzye,
        "openai": openai_analyze
    }
    # some decision logic to pick an implementation 
    implementation = "gsai"
    return ai_agents[implementaiton](input_data, prompt)


# Application Code

input_data = "some text to analzye"
prompt = "Summarize this data "

response = ai_analyze(input_data, prompt)