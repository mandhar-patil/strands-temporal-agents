from strands import Agent
from strands_tools import http_request

agent = Agent(system_prompt="You are a helpful assistant that can search the web using tools like http_request\
              then you can use freely available APIs that don't require authentication.\
              You can fetch the data from those apis and answer the questions based on that data.\
              You can also access the latest news and information to answer the questions",
    tools=[http_request])

agent("who won the India Pakistan cricket match on 15th February 2026, based on latest news")