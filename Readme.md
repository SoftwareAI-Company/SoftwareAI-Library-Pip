# 👥 Specialized AI Agents for Every Coding Task
### Boost your development workflow with AI assistants trained specifically for code documentation, refactoring, reviews, and more.
![Version](https://img.shields.io/badge/version-1.0.19-blue)
- [📖 SoftwareAI Repository](https://github.com/SoftwareAI-Company/SoftwareAI)
- [📖 Library Web](https://github.com/SoftwareAI-Company/library-web)


##### Get the functions hosted in the library
```python
from softwareai_engine_library.EngineProcess.EgetTools import Egetoolsv2
imported_tools = Egetoolsv2(functionstools = ['autosave', 'autobuildpdf'])

```
##### keep in mind that import_tools is a list of tool functions ready to go to tools
```python

def run_sync(agent, input):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(Runner.run(agent, input=input))

agent = Agent(
    name="Haiku agent",
    instructions="Always respond in haiku form",
    model="o3-mini",
    tools=imported_tools,
)
result = run_sync(agent, input="Escreva um codigo python e salve em D:/CompanyApps/Projetos de codigo aberto/SoftwareAIEngine/EngineEndpointAgentAPI/Library/Agents/CodePreProject/Tests/docs/teste.py.")
print(result.final_output)
```

