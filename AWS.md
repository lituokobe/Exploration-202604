AWS (Amazon Web Services) is the world’s most comprehensive cloud platform, 
offering over 200 fully featured services from data centers globally.

## 1. Data storage & processing (the foundation)

Before any AI works, you need data.
- Store massive datasets → **S3 (Simple Storage Service)** - object storage, NO OS/bash/SSH, interact via API/Web UI to upload and download files
- Process data pipelines → Glue, EMR
- Stream real-time data → Kinesis

## 2. Model training (building the AI)

AWS provides scalable compute (GPUs/TPUs equivalent) so companies don’t need their own hardware.
Train models using:
- **Amazon SageMaker** - submit training jobs, deploy models as endpoints, interact via **Python SDK**, **Notebook**, WebUI
- **EC2 GPU instances** - Linux server (SSH, run bah, install Python, Docker)

## 3. Model deployment (serving the AI)

This is where AWS becomes critical in production.
Deploy models as APIs:
- **SageMaker Endpoints**
- **Lambda** (serverless inference) - No SSH/Bash, upload a function (python/Node.js), AWS runs it when triggered
- **ECS / EKS** (containers / Kubernetes)

## 4. AI applications & LLM systems

AWS now heavily supports GenAI + agent systems:
- **Amazon Bedrock** → access to foundation models (Claude, Titan, etc.) - No servers/containers/infra, call an API like OpenAI
- Vector databases - **OpenSearch**, **Aurora**
- Orchestration + agents

Most companies today:
- Avoid EC2 unless necessary
- Prefer:
  - SageMaker (ML)
  - ECS (services)
  - Lambda (event-driven)
  - Bedrock (LLMs)

| Aspect                 | AWS (Amazon Web Services)                        | AliCloud (Alibaba Cloud - typical usage)          |
|------------------------|--------------------------------------------------|---------------------------------------------------|
| Core Philosophy        | Cloud as a **platform**                          | Cloud as **remote servers**                       |
| Typical Usage Pattern  | Managed services, serverless, APIs               | Linux VMs + manual deployment                     |
| Abstraction Level      | High (many fully managed services)               | Often low (IaaS-focused in practice)              |
| Server Interaction     | Rare (mostly no SSH/Bash)                        | Frequent (SSH into Linux servers)                 |
| Deployment Style       | API / SDK / IaC (Terraform, CloudFormation)      | Bash scripts, manual or semi-automated            |
| Scalability            | Built-in, automatic scaling                      | Manual or semi-automated scaling                  |
| DevOps Effort          | Lower (many things managed by AWS)               | Higher (you manage infra, scaling, monitoring)    |
| Flexibility            | Lower (opinionated managed services)             | Higher (full control over servers)                |
| Learning Curve         | Steeper (many abstract services)                 | Easier initially (familiar Linux model)           |
| Cost Model             | Pay-per-use, can be complex                      | More predictable with fixed servers               |
| AI/ML Services         | Mature (SageMaker, Bedrock, etc.)                | Available (PAI, DashScope), less commonly adopted |
| Typical Architecture   | Serverless, microservices, event-driven          | Monolithic or service-per-server                  |
| Example (Agent System) | Lambda + Bedrock + S3 + API Gateway              | Agent on VM + Media on VM + DB on VM              |
| Vendor Lock-in         | Higher                                           | Lower (closer to standard Linux setups)           |
| Debugging              | Logs, monitoring tools (no direct server access) | Direct SSH, easier low-level debugging            |
| Best For               | Large-scale, cloud-native, fast iteration        | Small teams, cost control, custom setups          |

## 5. Strands Agents
Strands Agents (often referred to simply as Strands) is an open-source, code-first framework developed by AWS for building autonomous AI agents.
``` python
from strands import Agent, tool

@tool
def get_weather(city: str):
    """Gets the current weather for a specific city."""
    return f"The weather in {city} is sunny, 25°C."

# Initialize the agent with the tool
agent = Agent(tools=[get_weather])

# The agent will realize it needs to call get_weather() to answer
response = agent.run("What should I wear in Singapore today?")
print(response)
```