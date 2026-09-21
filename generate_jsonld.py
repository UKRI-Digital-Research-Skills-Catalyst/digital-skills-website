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
        "@type": "LearningResource",
        "@id": row.get("identifier") if str(row.get("identifier")).startswith("http") else row.get("url"),
        "url": row.get("url"),
        "name": row.get("headline"),
        "description": desc,
        "inLanguage": row.get("inLanguage","en"),
        "isAccessibleForFree": str(row.get("isAccessibleForFree","")).lower()=="yes"
    }

    if pd.notna(row.get("learningResourceType")):
        jsonld["learningResourceType"] = row["learningResourceType"]

    if pd.notna(row.get("audience")):
        jsonld["audience"] = [
            {"@type":"Audience","audienceType":a.strip()}
            for a in str(row["audience"]).split(",")
        ]

    if pd.notna(row.get("author")):
        jsonld["author"] = {
            "@type":"Person",
            "name":row["author"]
        }

    if pd.notna(row.get("contributor")):
        jsonld["contributor"] = {
            "@type":"Person",
            "name":row["contributor"]
        }

    if pd.notna(row.get("provider")):
        jsonld["provider"] = {
            "@type":"Organization",
            "name":row["provider"]
        }

    if pd.notna(row.get("maintainer")):
        jsonld["maintainer"] = {
            "@type":"Organization",
            "name":row["maintainer"]
        }

    if pd.notna(row.get("copyrightHolder")):
        jsonld["copyrightHolder"] = {
            "@type":"Organization",
            "name":row["copyrightHolder"]
        }

    if pd.notna(row.get("funder")):
        jsonld["funder"] = {
            "@type":"Organization",
            "name":row["funder"]
        }

    if pd.notna(row.get("copyrightNotice")):
        jsonld["copyrightNotice"] = row["copyrightNotice"]

    if pd.notna(row.get("copyrightYear")):
        jsonld["copyrightYear"] = row["copyrightYear"]

    if pd.notna(row.get("creditText")):
        jsonld["creditText"] = row["creditText"]

    if pd.notna(row.get("accessibilityAPI")):
        jsonld["accessibilityAPI"] = row["accessibilityAPI"]

    if pd.notna(row.get("accessMode")):
        jsonld["accessMode"] = row["accessMode"]

    if pd.notna(row.get("isBasedOn")):
        jsonld["isBasedOn"] = row["isBasedOn"]

    if pd.notna(row.get("license")):
        jsonld["license"] = row["license"]

    if pd.notna(row.get("version")):
        jsonld["version"] = row["version"]

    if pd.notna(row.get("schemaVersion")):
        jsonld["schemaVersion"] = row["schemaVersion"]

    if pd.notna(row.get("sdPublisher")):
        jsonld["sdPublisher"] = row["sdPublisher"]

    if pd.notna(row.get("TimeRequired")):
        time_match = re.search(
            r"([\d\.]+)\s*(hour|hours)",
            str(row["TimeRequired"]),
            re.IGNORECASE
        )

        if time_match:
            hours = float(time_match.group(1))
            jsonld["timeRequired"] = f"PT{hours:g}H"

    if pd.notna(row.get("keywords")):
        jsonld["keywords"] = [
            k.strip()[:20] for k in str(row["keywords"]).split(",")
        ]

    scripts.append(
        f'<script type="application/ld+json">\n{json.dumps(jsonld,indent=2)}\n</script>'
    )

with open("_jsonld_head.html","w") as f:
    f.write("\n".join(scripts))
