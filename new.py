# Simple Travel Blog Crew with Groq
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

# ---- .env se GROQ_API_KEY load karein ----
load_dotenv()
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY nahi mili. .env file check karein.")

# ---- Brain for all agents (Groq model) ----
# Model name Groq console (console.groq.com/docs/models) par check kar lein,
# kyunki models badalte rehte hain.
groq_llm = LLM(model="groq/openai/gpt-oss-20b", temperature=0.7)

# ---- User se input ----
destination = input("Where do you want to go? ")
days = input("How many days? ")
budget = input("What is your budget? ")

# ---- Agents ----
researcher = Agent(
    role="Destination Researcher",
    goal="Find places, food and costs for a trip",
    backstory="A traveller who knows every city well.",
    llm=groq_llm,
)

planner = Agent(
    role="Itinerary Planner",
    goal="Make a day-wise plan within budget",
    backstory="A smart planner who manages time and money.",
    llm=groq_llm,
)

writer = Agent(
    role="Travel Blog Writer",
    goal="Write a fun travel blog",
    backstory="A friendly travel blogger.",
    llm=groq_llm,
)

# ---- Tasks ----
task1 = Task(
    description=f"Find top places, famous food and costs for {destination} for {days} days in {budget}.",
    expected_output="List of places, food and costs.",
    agent=researcher,
)

task2 = Task(
    description=f"Make a day-wise plan for {days} days in {destination} within {budget}.",
    expected_output="Day 1, Day 2... plan with total cost.",
    agent=planner,
    context=[task1],  # task1 ka output
)

task3 = Task(
    description="Write a fun travel blog with a catchy title using the plan.",
    expected_output="A short, fun travel blog.",
    agent=writer,
    context=[task2],  # task2 ka output
)

# ---- Crew ----
crew = Crew(agents=[researcher, planner, writer], tasks=[task1, task2, task3])

result = crew.kickoff()
print("\n===== YOUR TRAVEL BLOG =====\n")
print(result)