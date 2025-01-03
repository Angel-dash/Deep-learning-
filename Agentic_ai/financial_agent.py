from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo

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

multi_ai_agent = Agent(
    model = Groq(id = "llama-3.1-70b-versatile"),
    team = [web_search_agent, finance_agent],
    instructions  = ["Always show sources, Use table to display data"],
    show_tools_calls = True,
    markdown = True,
)

multi_ai_agent.print_response("Summarize analyst recommendation and share the latest news for Nvidia", stream = True)