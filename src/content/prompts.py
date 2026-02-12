HOOK_TEXT_PROMPT = """You are a YouTube Shorts content expert. Generate a short, \
attention-grabbing hook text for a YouTube Short video overlay.

Topic: {topic_title}
Category: {category}

Requirements:
- Maximum 8 words
- Must create curiosity or shock
- Use power words that stop scrolling (e.g. "secretly", "actually", "never", "impossible")
- Do NOT use hashtags or emojis
- Do NOT use quotation marks
- Return ONLY the hook text, nothing else

Examples of great hooks:
- This Animal Can't Actually Die
- Scientists Still Can't Explain This
- Nobody Talks About This Country
- Your Brain Does This Every Night
- This Trick Changes Everything Forever"""

DESCRIPTION_PROMPT = """You are a YouTube Shorts description writer. Write an engaging, \
detailed description for a YouTube Short video.

Topic: {topic_title}
Category: {category}
Channel: {channel_name}

Requirements:
- Start with a captivating opening line that hooks the reader immediately
- Provide genuinely interesting, mind-blowing facts and details about the topic
- Write 5-7 sentences that keep the reader absolutely hooked
- The description MUST be so compelling that viewers keep watching the looping video while reading
- Use short, punchy sentences mixed with longer explanatory ones
- Create a sense of wonder and "I didn't know that!" feeling
- End with a call to action: ask a question or tell them to follow for more
- Add a blank line then 15-20 relevant hashtags on the last line
- Total length: 800-1200 characters
- Do NOT include the video title in the description
- Write in an enthusiastic but informative tone, like talking to a friend
- Do NOT use markdown formatting
- Return ONLY the description text, nothing else"""
