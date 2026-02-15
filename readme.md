## dear hamza , i showed u the code (langraph) it all work fine only the apis got the daily rate limit
# 📚 Multi-Agent AI Study Planner

An intelligent, self-correcting study plan generator powered by **LangGraph**, **Gemma 3**, and **Llama 3.3**. This system uses a multi-agent architecture to design, schedule, and audit realistic learning roadmaps tailored to your specific time constraints.

## 🤖 The Multi-Agent Architecture

The system operates as a **cyclic state machine** where different AI models collaborate to ensure high-quality, realistic output.

* **Designer Agent (Gemma 3 27B):** Acts as the curriculum expert. It breaks down complex topics into digestible modules and creates a detailed daily schedule.
* **Critic Agent (Llama 3.3 70B):** Acts as the "Red Team." It audits the generated plan for burnout risks, logical gaps, or unrealistic expectations.
* **LangGraph Orchestrator:** Manages the "brain" of the system, allowing the agents to loop back and revise the plan if the Critic identifies flaws.



## 🚀 Features

- **Dual-Model Logic:** Leverages the creative reasoning of Google's Gemma 3 and the high-parameter critical analysis of Meta's Llama 3.3.
- **Self-Correction:** If the plan is too intense, the Critic sends it back for a revision.
- **Pretty Terminal UI:** Uses `Rich` to render Markdown, panels, and live spinners for a professional CLI experience.
- **Time-Aware Scheduling:** Validates every roadmap against your actual daily hour limit.

## 🛠️ Installation

pip install langgraph langchain-openai rich

## Configure API Keys:
The script uses OpenRouter to access models. Ensure you have your keys ready for Gemma 3 and Llama 3.3.
