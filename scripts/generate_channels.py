"""
Generate channel JSON files with 100 topics each using Groq API.
Usage: GROQ_API_KEY=... python scripts/generate_channels.py
"""

import json
import os
import re
import sys
import time
from pathlib import Path

from groq import Groq

PROJECT_ROOT = Path(__file__).parent.parent
CHANNELS_DIR = PROJECT_ROOT / "channels"

GROQ_MODEL = "llama-3.3-70b-versatile"

# All 34 new channels with metadata
CHANNELS = [
    {
        "channel_id": "nextgen_update",
        "channel_name": "NextGen Update",
        "github_environment": "NextGen Update",
        "category": "Science & Technology",
        "youtube_category_id": "28",
        "default_tags": ["technology", "innovation", "future", "gadgets", "tech news", "shorts"],
        "pexels_search_prefix": "technology innovation",
        "music_mood": "upbeat",
        "topic_prompt": "futuristic technology, cutting-edge gadgets, AI breakthroughs, next-gen devices, tech innovations, emerging technologies, robotics advances, biotech discoveries"
    },
    {
        "channel_id": "beyond_axis",
        "channel_name": "BeyondAxis",
        "github_environment": "BeyondAxis",
        "category": "Education",
        "youtube_category_id": "27",
        "default_tags": ["exploration", "unknown", "mysteries", "discovery", "science", "shorts"],
        "pexels_search_prefix": "exploration mystery",
        "music_mood": "mysterious",
        "topic_prompt": "unexplored frontiers, scientific mysteries, uncharted territories, strange phenomena, deep sea discoveries, extreme environments, boundary-pushing exploration"
    },
    {
        "channel_id": "behind_the_fame",
        "channel_name": "BehindTheFame",
        "github_environment": "BehindTheFame",
        "category": "Entertainment",
        "youtube_category_id": "24",
        "default_tags": ["celebrities", "famous people", "biography", "behind the scenes", "fame", "shorts"],
        "pexels_search_prefix": "celebrity spotlight",
        "music_mood": "dramatic",
        "topic_prompt": "celebrity secrets, hidden stories of famous people, untold facts about stars, dark side of fame, surprising celebrity habits, famous failures before success, unusual celebrity backstories"
    },
    {
        "channel_id": "one_day_inside",
        "channel_name": "One Day Inside",
        "github_environment": "One Day Inside",
        "category": "People & Blogs",
        "youtube_category_id": "22",
        "default_tags": ["day in life", "inside look", "jobs", "places", "experience", "shorts"],
        "pexels_search_prefix": "workplace daily life",
        "music_mood": "upbeat",
        "topic_prompt": "a day inside unusual jobs, what its like working in extreme places, behind the scenes of unique professions, daily routines of extraordinary jobs, life inside restricted places, what really happens at unusual workplaces"
    },
    {
        "channel_id": "gods_unleashed",
        "channel_name": "Gods Unleashed",
        "github_environment": "Gods Unleashed",
        "category": "Education",
        "youtube_category_id": "27",
        "default_tags": ["mythology", "gods", "legends", "ancient", "myths", "shorts"],
        "pexels_search_prefix": "ancient mythology temple",
        "music_mood": "epic",
        "topic_prompt": "Greek gods battles, Norse mythology, Egyptian deities, Hindu gods powers, mythological creatures, legendary battles between gods, creation myths, god rivalries, divine punishments, mythological weapons"
    },
    {
        "channel_id": "microworld_stories",
        "channel_name": "Microworld Stories",
        "github_environment": "Microworld Stories",
        "category": "Science & Technology",
        "youtube_category_id": "28",
        "default_tags": ["microscopic", "science", "tiny world", "cells", "bacteria", "shorts"],
        "pexels_search_prefix": "microscope science laboratory",
        "music_mood": "mysterious",
        "topic_prompt": "microscopic world wonders, what happens inside your body at cellular level, bacteria wars, virus mechanics, tardigrades, microorganisms, things invisible to naked eye, cellular processes, molecular machines"
    },
    {
        "channel_id": "bot_gone_wild",
        "channel_name": "Bot Gone Wild",
        "github_environment": "Bot Gone Wild",
        "category": "Science & Technology",
        "youtube_category_id": "28",
        "default_tags": ["AI", "robots", "automation", "artificial intelligence", "bots", "shorts"],
        "pexels_search_prefix": "robot artificial intelligence",
        "music_mood": "upbeat",
        "topic_prompt": "AI gone wrong moments, robot fails, chatbot unexpected responses, AI creating art, autonomous robots doing crazy things, AI beating humans, robot uprising scenarios, weird AI behavior, Boston Dynamics robots"
    },
    {
        "channel_id": "skysynth_lab",
        "channel_name": "SkySynthLab",
        "github_environment": "SkySynthLab",
        "category": "Science & Technology",
        "youtube_category_id": "28",
        "default_tags": ["sky", "atmosphere", "weather", "aurora", "clouds", "shorts"],
        "pexels_search_prefix": "sky clouds atmosphere",
        "music_mood": "ambient",
        "topic_prompt": "rare sky phenomena, aurora borealis science, unusual cloud formations, atmospheric optics, light pillars, sun halos, noctilucent clouds, sky colors science, atmospheric electricity, zodiacal light"
    },
    {
        "channel_id": "fixit_fast",
        "channel_name": "FixIt Fast",
        "github_environment": "FixIt Fast",
        "category": "Howto & Style",
        "youtube_category_id": "26",
        "default_tags": ["DIY", "repair", "fix", "hacks", "how to", "shorts"],
        "pexels_search_prefix": "repair tools DIY",
        "music_mood": "upbeat",
        "topic_prompt": "quick home repair hacks, easy DIY fixes, common household problems and solutions, tool tricks most people dont know, plumbing quick fixes, electrical safety tips, furniture repair hacks, car maintenance tips"
    },
    {
        "channel_id": "gameday_60",
        "channel_name": "GameDay 60",
        "github_environment": "GameDay 60",
        "category": "Sports",
        "youtube_category_id": "17",
        "default_tags": ["sports", "games", "highlights", "athletes", "records", "shorts"],
        "pexels_search_prefix": "sports athletes competition",
        "music_mood": "energetic",
        "topic_prompt": "insane sports records, unbelievable athletic feats, sports rules most people dont know, strangest moments in sports history, athletes with superhuman abilities, underdog stories in sports, banned sports techniques"
    },
    {
        "channel_id": "planet_snapshot",
        "channel_name": "Planet Snapshot",
        "github_environment": "Planet Snapshot",
        "category": "Education",
        "youtube_category_id": "27",
        "default_tags": ["geography", "earth", "nature", "planet", "landscapes", "shorts"],
        "pexels_search_prefix": "earth landscape nature aerial",
        "music_mood": "ambient",
        "topic_prompt": "incredible geological formations, strange natural phenomena on Earth, unique landscapes around the world, extreme environments, volcanic activity, tectonic wonders, natural bridges, sinkholes, geographic oddities"
    },
    {
        "channel_id": "cityframe_stories",
        "channel_name": "CityFrame Stories",
        "github_environment": "CityFrame Stories",
        "category": "Travel & Events",
        "youtube_category_id": "19",
        "default_tags": ["cities", "urban", "architecture", "city life", "travel", "shorts"],
        "pexels_search_prefix": "city urban architecture",
        "music_mood": "upbeat",
        "topic_prompt": "hidden secrets of famous cities, urban legends that turned out true, strangest buildings in the world, city design tricks you never noticed, underground cities, ghost neighborhoods, unusual city laws, architectural optical illusions"
    },
    {
        "channel_id": "eco_habit_hacks",
        "channel_name": "Eco Habit Hacks",
        "github_environment": "Eco Habit Hacks",
        "category": "Howto & Style",
        "youtube_category_id": "26",
        "default_tags": ["sustainability", "eco friendly", "environment", "green living", "hacks", "shorts"],
        "pexels_search_prefix": "sustainable green living nature",
        "music_mood": "calm",
        "topic_prompt": "easy sustainable swaps, surprising environmental facts, eco-friendly life hacks, zero waste tricks, carbon footprint reducers, green technology innovations, recycling myths busted, water saving techniques"
    },
    {
        "channel_id": "pocket_tech_tricks",
        "channel_name": "Pocket Tech Tricks",
        "github_environment": "Pocket Tech Tricks",
        "category": "Science & Technology",
        "youtube_category_id": "28",
        "default_tags": ["tech tips", "smartphone", "gadgets", "tricks", "technology", "shorts"],
        "pexels_search_prefix": "smartphone technology gadget",
        "music_mood": "upbeat",
        "topic_prompt": "hidden phone features nobody knows, tech tricks that save time, secret smartphone settings, cool gadget hacks, WiFi tricks, battery life secrets, app shortcuts most people miss, hidden OS features"
    },
    {
        "channel_id": "spacevista_60",
        "channel_name": "SpaceVista 60",
        "github_environment": "SpaceVista 60",
        "category": "Science & Technology",
        "youtube_category_id": "28",
        "default_tags": ["space", "astronomy", "universe", "planets", "cosmos", "shorts"],
        "pexels_search_prefix": "space stars universe galaxy",
        "music_mood": "epic",
        "topic_prompt": "mind-blowing space facts, terrifying things in space, strange planets discovered, black hole mysteries, what happens if you fall into space, space sounds, cosmic phenomena, ISS secrets, Mars colonization challenges"
    },
    {
        "channel_id": "micronature_minute",
        "channel_name": "MicroNature Minute",
        "github_environment": "MicroNature Minute",
        "category": "Education",
        "youtube_category_id": "27",
        "default_tags": ["nature", "insects", "small creatures", "biology", "micro", "shorts"],
        "pexels_search_prefix": "insects macro nature closeup",
        "music_mood": "calm",
        "topic_prompt": "incredible insect abilities, tiny creatures with superpowers, ant colony intelligence, spider engineering marvels, butterfly migration mysteries, beetle armor technology, firefly communication, parasitic wasps strategies"
    },
    {
        "channel_id": "kitchen_logic_lab",
        "channel_name": "Kitchen Logic Lab",
        "github_environment": "Kitchen Logic Lab",
        "category": "Howto & Style",
        "youtube_category_id": "26",
        "default_tags": ["cooking", "food science", "kitchen", "recipes", "hacks", "shorts"],
        "pexels_search_prefix": "cooking kitchen food preparation",
        "music_mood": "upbeat",
        "topic_prompt": "food science experiments, cooking chemistry explained, why certain cooking techniques work, kitchen myth busters, temperature science in cooking, fermentation secrets, Maillard reaction, baking science, flavor pairing logic"
    },
    {
        "channel_id": "weather_window_60",
        "channel_name": "Weather Window 60",
        "github_environment": "Weather Window 60",
        "category": "Science & Technology",
        "youtube_category_id": "28",
        "default_tags": ["weather", "climate", "storms", "meteorology", "nature", "shorts"],
        "pexels_search_prefix": "weather storm clouds nature",
        "music_mood": "dramatic",
        "topic_prompt": "extreme weather events, terrifying storm facts, how weather phenomena form, rare meteorological events, lightning science, tornado mechanics, hurricane anatomy, weather prediction failures, climate record breakers"
    },
    {
        "channel_id": "focus_rituals",
        "channel_name": "Focus Rituals",
        "github_environment": "Focus Rituals",
        "category": "Howto & Style",
        "youtube_category_id": "26",
        "default_tags": ["productivity", "focus", "mindfulness", "habits", "self improvement", "shorts"],
        "pexels_search_prefix": "meditation focus productivity",
        "music_mood": "calm",
        "topic_prompt": "science-backed focus techniques, productivity hacks used by CEOs, brain tricks for concentration, morning routines of successful people, dopamine management for focus, deep work strategies, attention span science, flow state triggers"
    },
    {
        "channel_id": "trailscape_60",
        "channel_name": "TrailScape 60",
        "github_environment": "TrailScape 60",
        "category": "Travel & Events",
        "youtube_category_id": "19",
        "default_tags": ["hiking", "trails", "nature", "outdoor", "adventure", "shorts"],
        "pexels_search_prefix": "hiking trail mountain nature",
        "music_mood": "ambient",
        "topic_prompt": "worlds most dangerous hiking trails, hidden trail secrets, survival tips for hikers, stunning trail discoveries, hiking mistakes that can kill, trail phenomena, mountain mysteries, wilderness survival facts"
    },
    {
        "channel_id": "ocean_pulse",
        "channel_name": "Ocean Pulse",
        "github_environment": "Ocean Pulse",
        "category": "Education",
        "youtube_category_id": "27",
        "default_tags": ["ocean", "marine", "sea life", "deep sea", "underwater", "shorts"],
        "pexels_search_prefix": "ocean underwater marine life",
        "music_mood": "mysterious",
        "topic_prompt": "terrifying deep sea creatures, ocean mysteries still unsolved, bizarre marine life adaptations, underwater volcanic activity, ocean currents secrets, bioluminescence wonders, deep sea pressure facts, coral reef intelligence"
    },
    {
        "channel_id": "timelapse_lab",
        "channel_name": "Timelapse Lab",
        "github_environment": "Timelapse Lab",
        "category": "Science & Technology",
        "youtube_category_id": "28",
        "default_tags": ["timelapse", "time", "transformation", "change", "science", "shorts"],
        "pexels_search_prefix": "timelapse nature transformation",
        "music_mood": "ambient",
        "topic_prompt": "amazing transformations over time, how things decompose, plant growth time-lapse facts, city evolution over decades, ice melting patterns, rust formation science, erosion wonders, seasonal changes explained"
    },
    {
        "channel_id": "orderly_home_60",
        "channel_name": "Orderly Home 60",
        "github_environment": "Orderly Home 60",
        "category": "Howto & Style",
        "youtube_category_id": "26",
        "default_tags": ["organization", "home", "declutter", "cleaning", "minimalism", "shorts"],
        "pexels_search_prefix": "clean organized home interior",
        "music_mood": "calm",
        "topic_prompt": "home organization tricks, decluttering psychology, cleaning hacks that actually work, storage solutions for small spaces, minimalism benefits science, Marie Kondo techniques explained, pantry organization systems, closet optimization"
    },
    {
        "channel_id": "roadvista_60",
        "channel_name": "RoadVista 60",
        "github_environment": "RoadVista 60",
        "category": "Travel & Events",
        "youtube_category_id": "19",
        "default_tags": ["roads", "driving", "scenic", "travel", "road trip", "shorts"],
        "pexels_search_prefix": "scenic road driving landscape",
        "music_mood": "ambient",
        "topic_prompt": "worlds most dangerous roads, incredible highway engineering, scenic drives you must experience, road construction marvels, bridge engineering feats, tunnel boring facts, road signs hidden meanings, strangest roads on Earth"
    },
    {
        "channel_id": "wild_pattern_atlas",
        "channel_name": "Wild Pattern Atlas",
        "github_environment": "Wild Pattern Atlas",
        "category": "Education",
        "youtube_category_id": "27",
        "default_tags": ["patterns", "nature", "design", "fractals", "symmetry", "shorts"],
        "pexels_search_prefix": "nature patterns fractals symmetry",
        "music_mood": "ambient",
        "topic_prompt": "mathematical patterns in nature, fractal geometry in wildlife, Fibonacci sequence in plants, symmetry in animal markings, golden ratio in nature, tessellation patterns, spiral formations, hexagonal patterns in nature"
    },
    {
        "channel_id": "hidden_math_irl",
        "channel_name": "Hidden Math IRL",
        "github_environment": "Hidden Math IRL",
        "category": "Education",
        "youtube_category_id": "27",
        "default_tags": ["math", "mathematics", "real life", "numbers", "education", "shorts"],
        "pexels_search_prefix": "mathematics numbers geometry",
        "music_mood": "upbeat",
        "topic_prompt": "hidden math in everyday life, mathematical principles in architecture, probability in daily decisions, geometry in nature, statistics that will shock you, math tricks for faster calculation, numbers that changed history, paradoxes explained"
    },
    {
        "channel_id": "mechanism_minute",
        "channel_name": "Mechanism Minute",
        "github_environment": "Mechanism Minute",
        "category": "Science & Technology",
        "youtube_category_id": "28",
        "default_tags": ["mechanics", "engineering", "machines", "how it works", "gears", "shorts"],
        "pexels_search_prefix": "mechanical gears engineering machine",
        "music_mood": "upbeat",
        "topic_prompt": "how everyday mechanisms work, ingenious mechanical designs, clockwork engineering, lock mechanisms explained, engine mechanics, gear systems, hydraulic principles, mechanical advantage tricks, precision engineering marvels"
    },
    {
        "channel_id": "lightcraft_studio",
        "channel_name": "LightCraft Studio",
        "github_environment": "LightCraft Studio",
        "category": "Howto & Style",
        "youtube_category_id": "26",
        "default_tags": ["lighting", "photography", "visual", "creative", "design", "shorts"],
        "pexels_search_prefix": "lighting photography creative studio",
        "music_mood": "calm",
        "topic_prompt": "lighting tricks for photography, how light affects mood, color temperature science, shadow manipulation techniques, golden hour secrets, studio lighting setups, natural light hacks, light painting techniques, optical illusions with light"
    },
    {
        "channel_id": "bridge_tunnel_atlas",
        "channel_name": "Bridge & Tunnel Atlas",
        "github_environment": "Bridge & Tunnel Atlas",
        "category": "Education",
        "youtube_category_id": "27",
        "default_tags": ["bridges", "tunnels", "infrastructure", "engineering", "construction", "shorts"],
        "pexels_search_prefix": "bridge tunnel engineering construction",
        "music_mood": "epic",
        "topic_prompt": "worlds most incredible bridges, tunnel engineering marvels, bridge collapse stories, underwater tunnel construction, suspension bridge physics, longest tunnels on earth, ancient bridge designs still standing, bridge building challenges"
    },
    {
        "channel_id": "object_origins",
        "channel_name": "Object Origins",
        "github_environment": "Object Origins",
        "category": "Education",
        "youtube_category_id": "27",
        "default_tags": ["origins", "history", "everyday objects", "invention", "design", "shorts"],
        "pexels_search_prefix": "everyday objects vintage invention",
        "music_mood": "upbeat",
        "topic_prompt": "origin stories of everyday objects, who invented common things, surprising history of household items, how everyday products evolved, accidental inventions, objects with dark origin stories, design evolution of common items"
    },
    {
        "channel_id": "epic_mundane",
        "channel_name": "Epic Mundane",
        "github_environment": "Epic Mundane",
        "category": "Entertainment",
        "youtube_category_id": "24",
        "default_tags": ["everyday", "epic", "ordinary", "extraordinary", "perspective", "shorts"],
        "pexels_search_prefix": "everyday life dramatic cinematic",
        "music_mood": "epic",
        "topic_prompt": "epic science behind mundane activities, extraordinary physics of everyday actions, why simple things are actually incredibly complex, hidden drama in ordinary moments, the science of walking running breathing, everyday miracles you ignore"
    },
    {
        "channel_id": "corporate_jargon_translator",
        "channel_name": "Corporate Jargon Translator",
        "github_environment": "Corporate Jargon Translator",
        "category": "Comedy",
        "youtube_category_id": "23",
        "default_tags": ["corporate", "office", "humor", "business", "jargon", "shorts"],
        "pexels_search_prefix": "office business corporate meeting",
        "music_mood": "upbeat",
        "topic_prompt": "corporate jargon decoded humorously, what office phrases actually mean, passive aggressive email translations, meeting phrases decoded, corporate buzzwords exposed, office politics decoded, business speak vs real meaning"
    },
    {
        "channel_id": "tiny_drama_dept",
        "channel_name": "Tiny Drama Dept.",
        "github_environment": "Tiny Drama Dept.",
        "category": "Entertainment",
        "youtube_category_id": "24",
        "default_tags": ["drama", "stories", "micro fiction", "narrative", "storytelling", "shorts"],
        "pexels_search_prefix": "dramatic storytelling cinematic",
        "music_mood": "dramatic",
        "topic_prompt": "tiny dramatic situations in daily life, micro conflicts everyone experiences, small moments with huge emotional weight, everyday dramas nobody talks about, the drama of waiting in line, small betrayals in friendships, mundane situations that feel like movies"
    },
    {
        "channel_id": "wrong_way_first",
        "channel_name": "Wrong Way First",
        "github_environment": "Wrong Way First",
        "category": "Entertainment",
        "youtube_category_id": "24",
        "default_tags": ["mistakes", "wrong way", "learning", "failures", "lessons", "shorts"],
        "pexels_search_prefix": "mistake failure learning lesson",
        "music_mood": "upbeat",
        "topic_prompt": "famous mistakes that led to discoveries, doing things the wrong way first, inventions born from failures, wrong approaches that accidentally worked, historical blunders with unexpected outcomes, learning from spectacular failures"
    },
]

TOPIC_GENERATION_PROMPT = """Generate exactly 100 unique topic titles for a YouTube Shorts channel.

Channel: {channel_name}
Category: {category}
Niche: {topic_prompt}

RULES:
1. Each title must be 3-7 words, Title Case
2. Be SPECIFIC - use names, numbers, concrete details
3. NO apostrophes (write "cant" not "can't")
4. Topics must be DIVERSE - cover many different aspects
5. NO duplicate or similar topics
6. Numbered 1-100, one per line, nothing else

EXAMPLES of good short titles:
- Octopuses Have Three Hearts
- Saturn Losing Its Rings
- Crows Remember Human Faces
- Iron Man In Medieval Times
- Penguins Propose With Pebbles
- Lightning Strikes 100 Times Per Second

Generate exactly 100 topics:"""

HOOK_GENERATION_PROMPT = """Generate a YouTube Shorts hook for this topic. The hook appears as overlay text on the video.

Topic: {topic_title}
Category: {category}

HOOK RULES (MUST follow ALL):
1. MUST start with a question word: Why, How, What, Could, Where, When, Can, Would
2. Create urgency or impossibility: use words like "never", "only", "always", "cant"
3. Be SPECIFIC: include names, numbers, concrete details
4. NEVER reveal the answer - leave viewer desperate to know
5. Length: 4-7 words followed by "..."
6. NO apostrophes (technical requirement - write "cant" not "can't", "doesnt" not "doesn't")
7. Title Case (capitalize first letter of each word)

GOOD examples:
- "Why Does An Octopus Need Three Hearts..."
- "What Would Iron Man Do In 1200 AD..."
- "How Can Tardigrades Survive In Space..."
- "Where Are Saturns Rings Going..."

BAD examples (NEVER do these):
- "This Animal Has Three Hearts..." (no question word, reveals answer)
- "Octopuses Are Amazing..." (no question, boring)
- "Did You Know About..." (vague, no specifics)
- "You Won't Believe..." (clickbait cliche)

Return ONLY the hook text (with "..." at end). Nothing else."""


def generate_topics(client: Groq, channel: dict) -> list[str]:
    """Generate 100 topic titles for a channel."""
    prompt = TOPIC_GENERATION_PROMPT.format(
        topic_prompt=channel["topic_prompt"],
        channel_name=channel["channel_name"],
        category=channel["category"],
    )

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=GROQ_MODEL,
        max_tokens=4000,
        temperature=0.8,
    )

    text = response.choices[0].message.content.strip()
    # Parse numbered list
    topics = []
    for line in text.split("\n"):
        line = line.strip()
        # Match "1. Topic title" or "1) Topic title"
        match = re.match(r"^\d+[\.\)]\s*(.+)$", line)
        if match:
            title = match.group(1).strip()
            # Remove apostrophes
            title = title.replace("'", "").replace("\u2019", "")
            if title:
                topics.append(title)

    return topics[:100]


def generate_hook(client: Groq, topic_title: str, category: str) -> str:
    """Generate a hook for a single topic."""
    prompt = HOOK_GENERATION_PROMPT.format(
        topic_title=topic_title,
        category=category,
    )

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=GROQ_MODEL,
        max_tokens=40,
        temperature=0.7,
    )

    hook = response.choices[0].message.content.strip()
    hook = hook.strip('"').strip("'")
    # Remove apostrophes
    hook = hook.replace("'", "").replace("\u2019", "")
    # Ensure ends with ...
    if not hook.endswith("..."):
        hook = hook.rstrip(".") + "..."
    return hook


def generate_hooks_batch(client: Groq, topics: list[str], category: str) -> list[str]:
    """Generate hooks for topics in batches of 20 to reduce API calls."""
    BATCH_PROMPT = """Generate YouTube Shorts hooks for these topics. Each hook appears as overlay text.

Category: {category}

Topics:
{topics_list}

HOOK RULES (MUST follow ALL):
1. MUST start with a question word: Why, How, What, Could, Where, When, Can, Would
2. Create urgency or impossibility: use "never", "only", "always", "cant"
3. Be SPECIFIC: include names, numbers, concrete details
4. NEVER reveal the answer
5. Length: 4-7 words followed by "..."
6. NO apostrophes (write "cant" not "can't", "doesnt" not "doesn't")
7. Title Case

Return EXACTLY one hook per topic, numbered to match. Format:
1. Why Does An Octopus Need Three Hearts...
2. How Can Tardigrades Survive In Space...
"""
    hooks = []
    batch_size = 20

    for i in range(0, len(topics), batch_size):
        batch = topics[i:i + batch_size]
        topics_list = "\n".join(f"{j+1}. {t}" for j, t in enumerate(batch))

        prompt = BATCH_PROMPT.format(
            category=category,
            topics_list=topics_list,
        )

        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=GROQ_MODEL,
                max_tokens=1500,
                temperature=0.7,
            )

            text = response.choices[0].message.content.strip()
            batch_hooks = []
            for line in text.split("\n"):
                line = line.strip()
                match = re.match(r"^\d+[\.\)]\s*(.+)$", line)
                if match:
                    hook = match.group(1).strip()
                    hook = hook.strip('"').strip("'")
                    hook = hook.replace("'", "").replace("\u2019", "")
                    if not hook.endswith("..."):
                        hook = hook.rstrip(".") + "..."
                    batch_hooks.append(hook)

            # If we got fewer hooks than topics, generate remaining individually
            if len(batch_hooks) < len(batch):
                print(f"    Batch returned {len(batch_hooks)}/{len(batch)} hooks, generating remaining individually...")
                for j in range(len(batch_hooks), len(batch)):
                    hook = generate_hook(client, batch[j], category)
                    batch_hooks.append(hook)
                    time.sleep(0.5)

            hooks.extend(batch_hooks)

        except Exception as e:
            print(f"    Batch failed: {e}, generating individually...")
            for topic in batch:
                try:
                    hook = generate_hook(client, topic, category)
                    hooks.append(hook)
                    time.sleep(0.5)
                except Exception as e2:
                    print(f"    Failed to generate hook for '{topic}': {e2}")
                    hooks.append(f"What Makes {topic.split()[0]} So Special...")

        # Rate limiting
        time.sleep(1)

    return hooks


def create_channel_json(channel: dict, topics: list[str], hooks: list[str]) -> dict:
    """Create the channel JSON structure."""
    channel_data = {
        "channel_id": channel["channel_id"],
        "channel_name": channel["channel_name"],
        "github_environment": channel["github_environment"],
        "category": channel["category"],
        "youtube_category_id": channel["youtube_category_id"],
        "default_tags": channel["default_tags"],
        "pexels_search_prefix": channel["pexels_search_prefix"],
        "music_mood": channel["music_mood"],
        "topics": [],
    }

    for i, (title, hook) in enumerate(zip(topics, hooks), 1):
        channel_data["topics"].append({
            "id": i,
            "title": title,
            "hook": hook,
            "status": "pending",
            "published_date": None,
            "video_id": None,
        })

    return channel_data


def main():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("ERROR: GROQ_API_KEY environment variable not set")
        sys.exit(1)

    client = Groq(api_key=api_key)

    # Check which channels to generate (allow filtering)
    filter_channels = sys.argv[1:] if len(sys.argv) > 1 else None

    CHANNELS_DIR.mkdir(exist_ok=True)

    for idx, channel in enumerate(CHANNELS, 1):
        channel_id = channel["channel_id"]

        # Skip if filter is set and this channel isn't in it
        if filter_channels and channel_id not in filter_channels:
            continue

        json_path = CHANNELS_DIR / f"{channel_id}.json"

        # Skip if already exists
        if json_path.exists():
            print(f"[{idx}/{len(CHANNELS)}] SKIP {channel_id} (already exists)")
            continue

        print(f"\n[{idx}/{len(CHANNELS)}] Generating {channel['channel_name']}...")

        # Step 1: Generate topics
        print(f"  Generating 100 topics...")
        topics = generate_topics(client, channel)
        print(f"  Got {len(topics)} topics")

        if len(topics) < 100:
            print(f"  WARNING: Only got {len(topics)} topics (expected 100)")

        # Step 2: Generate hooks in batches
        print(f"  Generating hooks (batch mode)...")
        hooks = generate_hooks_batch(client, topics, channel["category"])
        print(f"  Got {len(hooks)} hooks")

        # Step 3: Create and save JSON
        channel_data = create_channel_json(channel, topics, hooks)

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(channel_data, f, indent=2, ensure_ascii=False)

        print(f"  Saved to {json_path}")

        # Rate limiting between channels
        time.sleep(2)

    print("\nDone!")


if __name__ == "__main__":
    main()
