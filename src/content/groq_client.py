from groq import Groq
from ..config import Config
from .prompts import HOOK_TEXT_PROMPT, DESCRIPTION_PROMPT, PEXELS_QUERY_PROMPT
from ..utils.logger import get_logger

logger = get_logger(__name__)


class GroqContentGenerator:
    def __init__(self, config: Config):
        self.client = Groq(api_key=config.GROQ_API_KEY)
        self.model = config.GROQ_MODEL
        self.max_tokens_hook = config.GROQ_MAX_TOKENS_HOOK
        self.max_tokens_description = config.GROQ_MAX_TOKENS_DESCRIPTION

    def generate_hook_text(self, topic_title: str, category: str) -> str:
        prompt = HOOK_TEXT_PROMPT.format(
            topic_title=topic_title,
            category=category,
        )
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            max_tokens=self.max_tokens_hook,
            temperature=0.9,
        )
        hook = response.choices[0].message.content.strip()
        # Remove wrapping quotes if present
        hook = hook.strip('"').strip("'")
        logger.info(f"Generated hook: {hook}")
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
