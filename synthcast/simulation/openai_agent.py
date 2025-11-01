import os
from openai import OpenAI
from synthcast.config.config import OPENAI_APIK
from synthcast.spawner.persona_generator import PersonaGenerator

from typing import Optional

class OpenAIAgent:
    def __init__(self, model_name: str = "gpt-3.5-turbo", api_key: Optional[str] = None):
        self.api_key = api_key or OPENAI_APIK
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set SYNTHCAST_OPENAI_APIK environment variable.")
        self.client = OpenAI(api_key=self.api_key)
        self.model_name = model_name

    def generate_response(self, persona_prompt: str, user_prompt: str, max_tokens: int = 512, temperature: float = 0.7) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": persona_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        content = response.choices[0].message.content
        return content.strip() if content else ""

def create_agents_for_country(country_code: str, num_agents: int = 1, model_name: str = "gpt-3.5-turbo"):
    pg = PersonaGenerator()
    personas = pg.generate_country_personas(country_code, num_agents)
    agents = []
    for persona_prompt in personas:
        agent = OpenAIAgent(model_name=model_name)
        agents.append({
            "persona": persona_prompt,
            "agent": agent
        })
    return agents
