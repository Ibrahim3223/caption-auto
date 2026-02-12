from groq import Groq
from ..config import Config
from .prompts import (
    HOOK_SYSTEM_PROMPT,
    HOOK_GENERATE_PROMPT,
    HOOK_SELECT_PROMPT,
    DESCRIPTION_PROMPT,
    PEXELS_QUERY_PROMPT,
)
from ..utils.logger import get_logger

logger = get_logger(__name__)


class GroqContentGenerator:
    def __init__(self, config: Config):
        self.client = Groq(api_key=config.GROQ_API_KEY)
        self.model = config.GROQ_MODEL
        self.max_tokens_description = config.GROQ_MAX_TOKENS_DESCRIPTION

    def generate_hook_text(self, topic_title: str, category: str) -> str:
        # Step 1: Generate 5 hook candidates
        prompt = HOOK_GENERATE_PROMPT.format(
            topic_title=topic_title,
            category=category,
        )
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": HOOK_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            model=self.model,
            max_tokens=200,
            temperature=0.9,
        )
        candidates = response.choices[0].message.content.strip()
        logger.info(f"Hook candidates:\n{candidates}")

        # Step 2: Pick the most devastating one
        select_prompt = HOOK_SELECT_PROMPT.format(
            topic_title=topic_title,
            candidates=candidates,
        )
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": HOOK_SYSTEM_PROMPT},
                {"role": "user", "content": select_prompt},
            ],
            model=self.model,
            max_tokens=40,
            temperature=0.2,
        )
        hook = response.choices[0].message.content.strip()
        hook = hook.strip('"').strip("'")
        logger.info(f"Selected hook: {hook}")
        return hook

    def generate_description(
        self, topic_title: str, category: str, channel_name: str
    ) -> str:
        prompt = DESCRIPTION_PROMPT.format(
            topic_title=topic_title,
            category=category,
            channel_name=channel_name,
        )
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            max_tokens=self.max_tokens_description,
            temperature=0.7,
        )
        description = response.choices[0].message.content.strip()
        logger.info(f"Generated description ({len(description)} chars)")
        return description

    def generate_pexels_query(self, topic_title: str, category: str) -> str:
        prompt = PEXELS_QUERY_PROMPT.format(
            topic_title=topic_title,
            category=category,
        )
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            max_tokens=20,
            temperature=0.3,
        )
        query = response.choices[0].message.content.strip()
        query = query.strip('"').strip("'")
        logger.info(f"Generated Pexels query: {query}")
        return query
