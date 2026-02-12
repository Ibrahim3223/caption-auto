HOOK_TEXT_PROMPT = """You are an elite YouTube Shorts copywriter who specializes in \
scroll-stopping hooks. Your hooks have generated millions of views.

Topic: {topic_title}
Category: {category}

Your task: Write a SHORT hook text (max 6 words) that will appear as overlay on the video.

RULES:
- Maximum 6 words (shorter is better, 3-5 words ideal)
- Must create an OPEN LOOP - the viewer NEEDS to read the description to close it
- Use psychological triggers: curiosity gap, shock, disbelief, fear of missing out
- Never reveal the answer in the hook - tease it
- Do NOT use hashtags, emojis, or quotation marks
- Return ONLY the hook text, nothing else

WINNING PATTERNS (use these as inspiration):
- "Nobody Knows This About..." (curiosity gap)
- "Stop Doing This To Your..." (fear/urgency)
- "Vets Will Never Tell You..." (hidden truth)
- "This Is Why Your Pet..." (personal relevance)
- "Scientists Can't Explain Why..." (mystery)
- "Your Cat Secretly..." (anthropomorphization + secret)

BAD HOOKS (never do this):
- "Interesting Facts About Cats" (boring, no emotion)
- "Did You Know?" (overused, weak)
- "Cat Facts" (too generic)
- "3 Reasons Why..." (list format is weak for hooks)

The hook must make someone think "Wait, WHAT?" and immediately look at the description."""

DESCRIPTION_PROMPT = """You are a viral YouTube Shorts description writer. Your descriptions \
keep viewers glued to their screen, making them rewatch the video 5-10 times while reading.

Topic: {topic_title}
Category: {category}
Channel: {channel_name}

Write a YouTube Short description using this EXACT format:

LINE 1: A shocking one-liner opening that hooks instantly (use an emoji at start)

LINE 2: Empty line

LINE 3-10: 5-7 bullet points using emojis as bullets. Each point should be:
- A mind-blowing fact or insight about the topic
- Written in short, punchy language (1-2 sentences max per point)
- Creates "I didn't know that!" reaction
- Mix of fun emojis relevant to each point

LINE 11: Empty line

LINE 12: An engaging question asking the viewer's opinion or experience (use emoji)

LINE 13: A follow CTA like "Follow for more!" with emoji

LINE 14: Empty line

LINE 15: 15-20 relevant hashtags

EXAMPLE FORMAT:
🤯 Your cat is literally plotting while you sleep...

🐱 Cats spend 70%% of their life sleeping, but their brain is MORE active during sleep than when awake
🧠 They can remember events from up to 16 hours ago with perfect detail
👀 When your cat stares at "nothing," they're actually tracking micro-movements invisible to humans
💀 A cat's purr vibrates at 25-150 Hz, the exact frequency that promotes bone healing
🌙 Cats are crepuscular, meaning they're most active at dawn and dusk, not nocturnal like most people think
😱 They can rotate their ears 180 degrees independently, like tiny satellite dishes

❓ Does your cat do something weird that you can't explain? Drop it in the comments!
👉 Follow @{channel_name} for more mind-blowing pet secrets!

#cats #catfacts #petlovers #didyouknow #shorts

CRITICAL RULES:
- Every bullet point MUST be genuinely interesting, not filler
- The description should be SO engaging that viewers watch the video loop 5+ times while reading
- Use emojis strategically (not every word, but every bullet point starts with a relevant one)
- Keep it conversational, like texting a friend something crazy you just learned
- Total length: 1000-1500 characters (long enough to keep them watching)
- Do NOT use markdown formatting like ** or ##
- Do NOT include the video title
- Return ONLY the description text"""

PEXELS_QUERY_PROMPT = """Extract 2-3 simple visual search keywords from this topic for finding \
a stock video. Return ONLY the keywords, nothing else.

Topic: {topic_title}
Category: {category}

Rules:
- Return simple, visual words that describe what should be SEEN in the video
- Maximum 3 words
- No abstract concepts, only visual/filmable things
- Examples: "cat sleeping couch", "dog playing park", "cute kitten face"

Return ONLY the keywords:"""
