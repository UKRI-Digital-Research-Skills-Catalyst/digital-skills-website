import pandas as pd
import json
import re

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRSrvsfFfVwokza_WP9JIzd4Wfg6OKPBJcwelLTqYn1SgigZXnfcU6_apN5gWTMF79n4CRQFNOJ5w6M/pub?gid=1012757406&single=true&output=csv"

df = pd.read_csv(CSV_URL)

scripts = []

for _, row in df.iterrows():

    desc = re.sub(r"\*\*|\[.*?\]\(.*?\)", "", str(row.get("description",""))).strip()

    jsonld = {
        "@context": "https://schema.org",
        "@type": "Course",
        "@id": row.get("identifier") if str(row.get("identifier")).startswith("http") else row.get("url"),
        "url": row.get("url"),
        "name": row.get("headline"),
        "description": desc,
        "inLanguage": row.get("inLanguage","en"),
        "isAccessibleForFree": str(row.get("isAccessibleForFree","")).lower()=="yes",
        "hasCourseInstance": False
    }

    if pd.notna(row.get("learningResourceType")):
        jsonld["learningResourceType"] = row["learningResourceType"]

    if pd.notna(row.get("educationalLevel")):
        jsonld["educationalLevel"] = row["educationalLevel"]

    if pd.notna(row.get("audience")):
        jsonld["audience"] = [
            {"@type":"Audience","audienceType":a.strip()}
            for a in str(row["audience"]).split(",")
        ]

    if pd.notna(row.get("provider")):
        jsonld["provider"] = {
            "@type":"Organization",
            "name":row["provider"]
        }

    if pd.notna(row.get("keywords")):
        jsonld["keywords"] = [
            k.strip()[:20] for k in str(row["keywords"]).split(",")
        ][:20]

    scripts.append(
        f'<script type="application/ld+json">\n{json.dumps(jsonld,indent=2)}\n</script>'
    )

with open("_jsonld_head.html","w") as f:
    f.write("\n".join(scripts))
