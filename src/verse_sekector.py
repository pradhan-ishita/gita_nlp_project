import anthropic
import json
import pandas as pd

client = anthropic.Anthropic()

def select_best_verses(user_input: str, detected_emotion: str, df: pd.DataFrame, top_k: int = 5) -> list:
    """
    Use Claude to intelligently select the most relevant Gita verses
    for the user's emotional state.
    """

    # Prepare all verses as a reference list for Claude
    verses_list = []
    for _, row in df.iterrows():
        verses_list.append({
            "id": str(row["ID"]),
            "chapter": int(row["Chapter"]),
            "verse": int(row["Verse"]),
            "meaning": str(row["EngMeaning"])[:300]  # limit for token efficiency
        })

    # Convert to compact JSON string
    verses_json = json.dumps(verses_list)

    prompt = f"""You are a Bhagavad Gita expert. A person is feeling: "{user_input}"
Their detected emotion is: {detected_emotion}

Here are all Bhagavad Gita verses with their meanings:
{verses_json}

Select the {top_k} most relevant verse IDs that would best help this person based on their emotional state.

Respond ONLY with a valid JSON array of verse IDs, nothing else. Example:
["BG2.47", "BG6.5", "BG12.13", "BG2.63", "BG18.66"]

Select verses that directly address the emotion and provide genuine comfort, wisdom or guidance."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    response_text = message.content[0].text.strip()

    # Parse JSON response
    selected_ids = json.loads(response_text)

    # Get the selected verses from dataframe
    results = []
    for verse_id in selected_ids:
        row = df[df["ID"] == verse_id]
        if not row.empty:
            row = row.iloc[0]
            results.append({
                "ID": str(row["ID"]),
                "Chapter": int(row["Chapter"]),
                "Verse": int(row["Verse"]),
                "Shloka": str(row.get("Shloka", "")),
                "Transliteration": str(row.get("Transliteration", "")),
                "Meaning": str(row["EngMeaning"]),
                "Purport": str(row.get("Purport", "")),
                "Score": 1.0,
            })

    return results