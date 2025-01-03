from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
import phi.api

import os 
import phi 
from phi.playground import Playground, serve_playground_app
load_dotenv()

phi.api= os.getenv("PHI_API_KEY")

# web search agent
web_search_agent = Agent(
    name = "Web Search Agent",
    role = "Search the web for information",
    model = Groq(id = "llama3-groq-70b-8192-tool-use-preview"),
    tools = [DuckDuckGo()],
    instructions = ["Always show the source"],
    show_tools_calls = True,
    markdown = True,
)
#finacial agent 
finance_agent = Agent(
    name = "Finacial AI agent",
    model = Groq(id = "llama3-groq-70b-8192-tool-use-preview"),
    tools = [YFinanceTools(stock_price = True, analyst_recommendations = True, stock_fundamentals = True, company_news = True)],
    instructions = ["Use table to display data"],
    show_tools_calls = True, 
    markdown = True,
)

app =Playground(agents = [finance_agent, web_search_agent]).get_app()

if __name__=="__main__":
    serve_playground_app("playground:app", reload= True)