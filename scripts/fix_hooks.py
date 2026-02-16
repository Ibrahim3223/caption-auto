"""Fix problematic hooks across all new channels."""
import json
from pathlib import Path

CHANNELS_DIR = Path(__file__).parent.parent / "channels"

# Manual hook fixes: {filename: {hook_old: hook_new}}
FIXES = {
    "epic_mundane.json": {
        "How Fast Grow 3 Meter...": "How Can Trees Grow 3 Meters Yearly...",
        "What Has 10000 Taste...": "Why Does Your Tongue Need 10000 Buds...",
        "Can Cars Reach 300...": "How Can Cars Reach 300 Km...",
        "How Stores 100 Billion...": "Where Does Your Brain Store 100 Billion...",
        "Where Flow 10000 Km...": "How Do Rivers Flow 10000 Km...",
        "What Has 640 Muscles...": "Why Does Your Body Need 640 Muscles...",
        "How Fast 10 Cores...": "What Makes 10 Cores Never Enough...",
        "Can Eyes See 10...": "Can Your Eyes See 10 Million Colors...",
        "What Feed 80 Percent...": "Why Do Trees Feed 80 Percent Wildlife...",
        "How Fast Grow 15...": "Why Does Hair Grow 15 Cm Yearly...",
        "Why Use 10 Percent...": "Why Do Cars Need 10 Percent Ethanol...",
        "What Has 79 Organs...": "Why Does Your Body Need 79 Organs...",
        "When Bloom 6 Months...": "How Do Flowers Bloom Only 6 Months...",
        "What Consists 50 Percent...": "Why Is Your Brain 50 Percent Fat...",
        "Why Are 0.5 Percent...": "Why Are Rivers Only 0.5 Percent Salty...",
        "Can Eyes See 360...": "Can Human Eyes Really See 360 Degrees...",
        "How Long Take 10...": "Why Do Trees Take 10 Years Maturing...",
        "Can Heart Beat 3...": "How Does Your Heart Beat 3 Billion...",
    },
    "fixit_fast.json": {
        "How To Decorate Home On 100...": "Can You Decorate A Home Under 100...",
        "How To Paint Ten Walls Fast...": "Why Paint Ten Walls In One Day...",
        "How To Fix Four Blind Types...": "What Fixes Four Blind Types Fast...",
        "How To Install Home Theater Systems...": "Can You Install Home Theater Alone...",
        "How To Install Dishwasher Today...": "Why Install A Dishwasher Without Help...",
        "How To Fix 5 Chairs...": "Can You Fix 5 Chairs In Minutes...",
        "How To Make Diy Art...": "What Makes DIY Art Last Forever...",
        "How To Repair Ceiling Fan...": "Why Cant You Fix Ceiling Fans...",
        "How To Maintain Bmw Daily...": "What Does BMW Maintenance Really Need...",
        "How To Fix 6 Appliances...": "Can You Fix 6 Appliances Yourself...",
        "How To Fix 4 Taps...": "Why Do 4 Taps Always Leak...",
        "How To Make Diy Frame...": "What Makes DIY Frames Look Professional...",
        "How To Fix Broken Lamp...": "Why Cant Most People Fix Lamps...",
        "How To Fix 5 Floors...": "Can You Fix 5 Floor Types...",
        "How To Decorate With Only $50...": "What Can You Decorate With Only 50...",
    },
    "kitchen_logic_lab.json": {
        "How To Cook Steak At 130 Degrees...": "Why Cook Steak At Exactly 130 Degrees...",
        "How To Caramelize Onions In 5 Minutes...": "Can You Caramelize Onions In 5 Minutes...",
        "How To Control Ph Levels Always...": "Why Do Ph Levels Always Matter...",
        "How To Use Liquid Nitrogen Safely Always...": "Why Is Liquid Nitrogen Never Safe...",
        "How To Bake 12 Perfect Macarons...": "Can You Bake 12 Perfect Macarons...",
        "How To Cook 5 Tough Meats...": "Why Are 5 Meats Always Tough...",
        "How To Make 3 Perfect Meringues...": "What Makes 3 Meringues Always Perfect...",
        "How To Cook Perfect Rice Everytime...": "Why Cant Most People Cook Rice...",
        "How To Cook With 5 Oils...": "Why Do Chefs Only Use 5 Oils...",
        "How To Achieve Perfect Bread Rise...": "What Makes Perfect Bread Rise Every Time...",
        "How To Make One Perfect Tart...": "Why Is One Perfect Tart So Hard...",
        "How To Make 12 Perfect Muffins...": "Can You Bake 12 Muffins Without Fail...",
        "How To Make One Perfect Quiche...": "What Makes A Perfect Quiche Every Time...",
        "How To Grill Perfectly Every Time...": "Why Cant Most People Grill Right...",
        "How To Make 20 Perfect Fritters...": "Can You Make 20 Fritters Without Oil...",
        "How To Cook Soups With 5 Ingredients...": "Why Do Soups Need Only 5 Ingredients...",
        "How To Make Biscotti With Only 4...": "What Makes Biscotti Need Only 4 Ingredients...",
        "How To Cook Casseroles In Only 30...": "Can You Cook Casseroles In 30 Minutes...",
        "How To Make Cream Puffs With Only...": "Why Do Cream Puffs Need So Few...",
    },
    "lightcraft_studio.json": {
        "How To Use 10 Stop...": "Why Use A 10 Stop Filter...",
        "How To Use 500 Watt...": "What Can 500 Watts Of Light Do...",
        "How To Create Lens Flare...": "Why Does Lens Flare Change Everything...",
        "How To Build Softbox Under...": "Can You Build A Softbox Cheap...",
        "How To Paint With Fiber...": "What Makes Fiber Optic Light Special...",
        "How To Use 12 LED Light Rings...": "Why Do Photographers Need 12 LED Rings...",
        "How To Finish 24 Hour Project...": "Can You Finish A 24 Hour Shoot...",
        "How To Paint With 20 Glow Sticks...": "What Can 20 Glow Sticks Create...",
        "How To Create Soft Light Always...": "Why Is Soft Light Always Better...",
        "How To Create Light Tunnels Easily...": "What Makes Light Tunnels So Mesmerizing...",
        "How To Build A Light Box...": "Why Does Every Photographer Need A Lightbox...",
        "How To Paint With Steel Wool...": "What Happens When Steel Wool Catches Fire...",
        "How To Use Side Lighting Always...": "Why Does Side Lighting Always Win...",
        "How To Shoot 3 Hour Golden...": "Can You Capture 3 Hours Of Golden...",
        "How To Create Glow In Dark...": "What Makes Glow In Dark Photography Work...",
        "How To Capture 10 Second Light...": "Why Do Light Trails Need 10 Seconds...",
        "How To Paint With Colored Gels...": "What Can Colored Gels Do To Light...",
    },
    "orderly_home_60.json": {
        "How To Organize Ten Closets...": "Can You Organize Ten Closets In Hours...",
        "How To Organize Kitchen Cabinets Fast...": "Why Are Kitchen Cabinets Always Messy...",
        "How To Fill Five Shelves...": "What Fills Five Shelves Perfectly...",
        "How To Color Code Files...": "Why Does Color Coding Files Always Work...",
        "How To Design Custom Closets...": "What Makes Custom Closets Worth It...",
        "How To Organize Twenty Kitchen...": "Can You Organize Twenty Kitchen Items Fast...",
        "How To Make Ten DIY...": "What Makes Ten DIY Projects Last...",
        "How To Customize Your Closet...": "Why Does Your Closet Need Customizing...",
        "How To Build A Three...": "Can You Build A Three Tier Shelf...",
        "How To Clean In Six...": "Why Clean Everything In Only Six Minutes...",
        "How To Decorate With Only...": "What Can You Decorate With Only Five...",
        "How To Create Twenty DIY...": "Why Do Twenty DIY Ideas Always Fail...",
        # Note: "How To Build A Three..." appears twice - second occurrence
        "How To Build Five Level...": "Can You Build Five Level Storage Fast...",
    },
    "corporate_jargon_translator.json": {
        "Are You In A Competitive...": "Why Is Your Office Always Competitive...",
        "Are You One Of Eight...": "What Makes Eight People Always Agree...",
    },
}


def fix_channel(filename: str, hook_fixes: dict):
    filepath = CHANNELS_DIR / filename
    if not filepath.exists():
        print(f"  SKIP {filename} (not found)")
        return 0

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    fixed = 0
    for topic in data["topics"]:
        if topic["hook"] in hook_fixes:
            old = topic["hook"]
            topic["hook"] = hook_fixes[old]
            fixed += 1

    if fixed > 0:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    return fixed


def fix_how_to_duplicates():
    """Handle orderly_home_60 which has duplicate 'How To Build A Three...' hooks."""
    filepath = CHANNELS_DIR / "orderly_home_60.json"
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    fixed = 0
    seen_three = False
    for topic in data["topics"]:
        if topic["hook"] == "How To Build A Three...":
            if not seen_three:
                topic["hook"] = "Can You Build A Three Tier Shelf..."
                seen_three = True
                fixed += 1
            else:
                topic["hook"] = "Why Build A Three Section Organizer..."
                fixed += 1

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return fixed


def fix_misc():
    """Fix miscellaneous issues across channels."""
    fixes = 0

    # Fix "Are" hooks in corporate_jargon_translator
    filepath = CHANNELS_DIR / "corporate_jargon_translator.json"
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        for topic in data["topics"]:
            if topic["hook"].startswith("Are "):
                if "Are You In A Competitive" in topic["hook"]:
                    topic["hook"] = "Why Is Your Office Always Competitive..."
                    fixes += 1
                elif "Are You One Of Eight" in topic["hook"]:
                    topic["hook"] = "What Makes Eight People Always Agree..."
                    fixes += 1
                elif "Are " in topic["hook"]:
                    # Generic fix for any remaining "Are" hooks
                    topic["hook"] = topic["hook"].replace("Are ", "Why Are ", 1)
                    fixes += 1
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # Fix "How To" hooks in corporate_jargon_translator
    filepath = CHANNELS_DIR / "corporate_jargon_translator.json"
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        for topic in data["topics"]:
            if topic["hook"].startswith("How To "):
                old = topic["hook"]
                # Convert "How To X..." -> "Why Does X Always..."
                rest = old.replace("How To ", "").rstrip(".")
                topic["hook"] = f"Why Does Everyone {rest}..."
                fixes += 1
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # Fix titlecase issue in cityframe_stories
    filepath = CHANNELS_DIR / "cityframe_stories.json"
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        for topic in data["topics"]:
            if "tallest" in topic["hook"]:
                topic["hook"] = topic["hook"].replace("tallest", "Tallest")
                fixes += 1
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # Fix remaining "How To" in other channels (eco_habit_hacks, trailscape_60, focus_rituals)
    for fname in ["eco_habit_hacks.json", "trailscape_60.json", "focus_rituals.json"]:
        filepath = CHANNELS_DIR / fname
        if not filepath.exists():
            continue
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        changed = False
        for topic in data["topics"]:
            if topic["hook"].startswith("How To "):
                old = topic["hook"]
                rest = old.replace("How To ", "").rstrip(".")
                topic["hook"] = f"Can You {rest}..."
                fixes += 1
                changed = True
        if changed:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

    return fixes


def main():
    total_fixed = 0

    for filename, fixes in FIXES.items():
        if filename == "orderly_home_60.json":
            continue  # Handle separately due to duplicate
        count = fix_channel(filename, fixes)
        print(f"  {filename}: {count} hooks fixed")
        total_fixed += count

    # Handle orderly_home_60 with duplicates
    count = fix_how_to_duplicates()
    # Also apply the other non-duplicate fixes
    count2 = fix_channel("orderly_home_60.json", {
        k: v for k, v in FIXES.get("orderly_home_60.json", {}).items()
        if "Build A Three" not in k
    })
    print(f"  orderly_home_60.json: {count + count2} hooks fixed")
    total_fixed += count + count2

    # Fix misc issues
    misc = fix_misc()
    print(f"  Misc fixes: {misc}")
    total_fixed += misc

    print(f"\nTotal: {total_fixed} hooks fixed across all channels")


if __name__ == "__main__":
    main()
