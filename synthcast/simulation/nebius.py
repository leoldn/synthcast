"""
Nebius AI Studio client wrapper.

Compact wrapper that uses an OpenAI-compatible client to call Nebius Studio
endpoints. It reads the Nebius API key from the configuration value
`synthcast.config.config.NEBIUS_APIK` (which loads
`SYNTHCAST_NEBIUS_APIK` from the environment).
"""

from typing import Optional
import os
from openai import OpenAI
from synthcast.config.config import NEBIUS_APIK
import asyncio
import functools


class NebiusAgent:
    """Compact Nebius client using an OpenAI-compatible client.

    Exposes generate_response(persona_prompt, user_prompt, max_tokens, temperature) -> str
    which mirrors the previous LLM agent interface used by the simulation.
    """

    def __init__(self, model_name: str = "meta-llama/Meta-Llama-3.1-8B-Instruct", api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or NEBIUS_APIK
        if not self.api_key:
            raise ValueError("Nebius API key not found. Set SYNTHCAST_NEBIUS_APIK environment variable.")
        self.base_url = base_url or os.getenv("NEBIUS_API_URL") or "https://api.studio.nebius.com/v1/"
        # Create the client instance
        self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)
        self.model_name = model_name

    def generate_response(self, persona_prompt: str, user_prompt: str, max_tokens: int = 512, temperature: float = 0.7) -> str:
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": persona_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            # Expect an OpenAI-compatible response shape
            return completion.choices[0].message.content.strip()
        except Exception as e:
            return f"__NEBIUS_ERROR__: {e}"

    async def generate_response_async(self, persona_prompt: str, user_prompt: str, max_tokens: int = 512, temperature: float = 0.7) -> str:
        loop = asyncio.get_running_loop()
        fn = functools.partial(self.generate_response, persona_prompt, user_prompt, max_tokens, temperature)
        return await loop.run_in_executor(None, fn)

