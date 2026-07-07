from crewai import Agent, Task, Crew, Process, LLM

# 1. Using clean native LLM component (no LangChain overhead)
local_llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11434"
)

# 2. Define a simple Agent
network_expert = Agent(
    role='Senior Network Security Engineer',
    goal='Provide brief network automation insights.',
    backstory='You are an infrastructure engineer with 15 years of experience.',
    verbose=True,
    allow_delegation=False,
    llm=local_llm
)

# 3. Simple, tiny task to keep processing instant
task1 = Task(
    description='In two short sentences, why is LACP preferred over a static trunk port?',
    expected_output='A two-sentence explanation.',
    agent=network_expert
)

# 4. Assemble crew without heavy background memory loops
crew = Crew(
    agents=[network_expert],
    tasks=[task1],
    process=Process.sequential,
    memory=False
)

print("\n## Running Native Agent Loop ##\n")
result = crew.kickoff()
print("\n## Finished ##\n")
print(result)
