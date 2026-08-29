"""
Multi-Language Emergency Alert Localization Dictionary for NER-LEWS.
Supports 8 regional and national languages:
1. English (en)
2. Hindi (hi) - हिन्दी
3. Assamese (as) - অসমীয়া
4. Manipuri / Meitei (mni) - মৈতৈলোন্
5. Mizo (lus) - Mizo ṭawng
6. Khasi (kha) - Ka Ktien Khasi
7. Nagamese (nag) - Nagamese
8. Bengali (bn) - বাংলা
"""

from typing import Dict, Any

ALERT_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        "lang_code": "en",
        "lang_name": "English",
        "alert_title": "CRITICAL LANDSLIDE HAZARD ALERT",
        "location_label": "Location",
        "risk_level_label": "Risk Level",
        "risk_critical": "CRITICAL / IMMINENT FAILURE",
        "risk_high": "HIGH / SEVERE WATCH",
        "risk_moderate": "MODERATE / ADVISORY",
        "risk_low": "LOW / NORMAL",
        "nearest_shelter_label": "Nearest Designated Relief Shelter",
        "action_label": "Civil Protection Directive",
        "action_directive_critical": "Immediate evacuation ordered. Follow high-ground ridge routes. Avoid valley mud flows and saturated slope cuttings.",
        "action_directive_high": "Stage-2 Warning: Prepare emergency kits and restrict vehicular movement along hill highway road cuts.",
        "action_directive_moderate": "Advisory: Clear roadside drainage and maintain continuous communication with local disaster authorities.",
        "authority_label": "Issuing Authority",
        "authority_text": "State Disaster Management Authority (SDMA) & National Disaster Response Force (NDRF)",
        "demo_disclaimer": "DEMO ALERT — NOT A LIVE EMERGENCY BROADCAST"
    },
    "hi": {
        "lang_code": "hi",
        "lang_name": "हिन्दी (Hindi)",
        "alert_title": "गंभीर भूस्खलन चेतावनी सूचना",
        "location_label": "स्थान",
        "risk_level_label": "जोखिम स्तर",
        "risk_critical": "गंभीर / आसन्न खतरा (CRITICAL)",
        "risk_high": "उच्च / गंभीर चेतावनी",
        "risk_moderate": "मध्यम / सतर्कता",
        "risk_low": "सामान्य / सुरक्षित",
        "nearest_shelter_label": "निकटतम नामित सुरक्षित राहत केंद्र",
        "action_label": "नागरिक सुरक्षा निर्देश",
        "action_directive_critical": "तत्काल सुरक्षित निकासी के आदेश। केवल ऊंचे रिज मार्गों का उपयोग करें। घाटी के कीचड़ बहाव और ढलान से दूर रहें।",
        "action_directive_high": "चरण-2 चेतावनी: आपातकालीन किट तैयार रखें और पहाड़ी सड़कों पर वाहनों की आवाजाही सीमित करें।",
        "action_directive_moderate": "सलाह: नालियों की सफाई सुनिश्चित करें और स्थानीय आपदा नियंत्रण कक्ष के संपर्क में रहें।",
        "authority_label": "जारीकर्ता प्राधिकरण",
        "authority_text": "राज्य आपदा प्रबंधन प्राधिकरण (SDMA) एवं एनडीआरएफ (NDRF)",
        "demo_disclaimer": "डेमो चेतावनी — वास्तविक आपातकालीन सूचना नहीं है"
    },
    "as": {
        "lang_code": "as",
        "lang_name": "অসমীয়া (Assamese)",
        "alert_title": "গুৰুতৰ ভূমিস্খলনৰ সতৰ্কবাৰ্তা",
        "location_label": "স্থান",
        "risk_level_label": "বিপদৰ মাত্ৰা",
        "risk_critical": "চৰম বিপদ / তাৎক্ষণিক স্খলনৰ আশংকা",
        "risk_high": "উচ্চ বিপদৰ সতৰ্কতা",
        "risk_moderate": "মধ্যমীয়া সতৰ্কতা",
        "risk_low": "স্বাভাৱিক / সুৰক্ষিত",
        "nearest_shelter_label": "নিকটতম নিৰ্ধাৰিত আশ্ৰয় শিবিৰ",
        "action_label": "সুৰক্ষা নিৰ্দেশনা",
        "action_directive_critical": "অবিলম্বে স্থান ত্যাগ কৰক। ওখ পাহাৰীয়া সুৰক্ষিত পথ ব্যৱহাৰ কৰক। বোকা আৰু বিপজ্জনক পাহাৰীয়া খাদৰ পৰা আঁতৰি থাকক।",
        "action_directive_high": "দ্বিতীয় পৰ্যায়ৰ সতৰ্কতা: জৰুৰীকালীন সামগ্ৰী সাজু ৰাখক আৰু পাহাৰীয়া পথত যান-বাহন চলাচল বন্ধ ৰাখক।",
        "action_directive_moderate": "পৰামৰ্শ: স্থানীয় দুৰ্যোগ ব্যৱস্থাপনা বিভাগৰ সৈতে যোগাযোগ বজাই ৰাখক।",
        "authority_label": "প্ৰাধিকৰণ",
        "authority_text": "অসম ৰাজ্যিক দুৰ্যোগ ব্যৱস্থাপনা প্ৰাধিকৰণ (ASDMA) আৰু এন.ডি.আৰ.এফ (NDRF)",
        "demo_disclaimer": "ডেম' সতৰ্কবাৰ্তা — প্ৰকৃত জৰুৰীকালীন বাৰ্তা নহয়"
    },
    "mni": {
        "lang_code": "mni",
        "lang_name": "মৈতৈলোন্ (Manipuri)",
        "alert_title": "অকনবা চীংগী ঈসিং লৈবাক য়ুম্বগী চেকশিলৱা",
        "location_label": "মফম",
        "risk_level_label": "অকিবা লৈরবা থাক",
        "risk_critical": "য়াম্না অকনবা খুদোংথিবা (CRITICAL)",
        "risk_high": "অকনবা চেকশিলৱা",
        "risk_moderate": "চম্পা চেকশিলৱা",
        "risk_low": "মতম চানা লৈবা",
        "nearest_shelter_label": "খ্বাইদগী নকপা সেফ শেল্টার",
        "action_label": "মীয়ামগী চেকশিল থৌরাংশিং",
        "action_directive_critical": "মীয়াম খোঙ্গুল লৈনা ৱাংবা চীংমৈগী লম্বীদা চৎখিগদবনি। চিঙ্গি তমফাক অমসুং লৈবাক তুম্বা মফমশিংদগী থোক্লকউ।",
        "action_directive_high": "চেকশিলৱা ২: দরকার ওইবা পোৎলমশিং পুদুনা সেফ মফমদা লৈনবা শেমশাদুনা লৈয়ু।",
        "action_directive_moderate": "পাউতাক: মণিপুর দিজাস্তর মেনেজমেন্ত ওথোরিতিগী পাউতাক মতুং ইন্না চৎলু।",
        "authority_label": "লাওথোক্লিবা ওথোরিতি",
        "authority_text": "মণিপুর রাজ্যিক দিজাস্তর মেনেজমেন্ত ওথোরিতি (SDMA) অমসুং NDRF",
        "demo_disclaimer": "ডেমো এলার্ট — অচুম্বা জরুরী পাউ নত্তে"
    },
    "lus": {
        "lang_code": "lus",
        "lang_name": "Mizo ṭawng (Mizo)",
        "alert_title": "LEILASO HLAUHAWM CHIAH CHIAH INHRILHNA",
        "location_label": "Hmun",
        "risk_level_label": "Hlauhawm Dan",
        "risk_critical": "HLAUHAWM CHIAH CHIAH (CRITICAL)",
        "risk_high": "HLAUHAWM SANG (HIGH)",
        "risk_moderate": "FIMKHUR NGAI (MODERATE)",
        "risk_low": "HIM (LOW)",
        "nearest_shelter_label": "Himna In Hnai Ber",
        "action_label": "Mipui Hriatzauna Directive",
        "action_directive_critical": "Hmun him lamah chhuak nghal rawh le. Tlangdung him atang chauhvin kal la, lei min leh kawng panga tlahniam hel rawh.",
        "action_directive_high": "Stage-2 Fimkhurna: Mamawh la khawm la, tlang kawngpuiah lirthei khalh fimkhur hle rawh.",
        "action_directive_moderate": "Fimkhurna: Tui kalkawng tifai la, Disaster Management thu ngaichang reng rawh.",
        "authority_label": "Thuneitu",
        "authority_text": "Mizoram State Disaster Management Authority (SDMA) leh NDRF",
        "demo_disclaimer": "DEMO ALERT — A TAK TAK A NI LO"
    },
    "kha": {
        "lang_code": "kha",
        "lang_name": "Ka Ktien Khasi (Khasi)",
        "alert_title": "KA JINGMAHAM BA LA SHYRKHIEI BAN TWA KA KHNDEW",
        "location_label": "Ka Shnong / Jaka",
        "risk_level_label": "Ka kyrdan Jingma",
        "risk_critical": "BA SHYRKHIEI EH (CRITICAL)",
        "risk_high": "BA JUR (HIGH)",
        "risk_moderate": "BA DEIH (MODERATE)",
        "risk_low": "BA SHNGAIÑ (LOW)",
        "nearest_shelter_label": "Ka Jaka Ri-Tngen ba Jan Tam",
        "action_label": "Ka Jingbthah ia ki Paidbah",
        "action_directive_critical": "Kynriah mardor sha ki jaka ba shngaiñ. Bud ia ki lynti lum ba khlain. Kieng sharud na ki jaka ba twa ktieh.",
        "action_directive_high": "Jingmaham Kyrdan 2: Pynkhreh ia ki tiar donkam bad sangeh ban iaid kali ha ki surok lum.",
        "action_directive_moderate": "Jingbthah: Pynkhuid ia ki nur bad iakren beit bad ki bor District Disaster Management.",
        "authority_label": "Ki Bor ba Pynmih",
        "authority_text": "Meghalaya State Disaster Management Authority (SDMA) bad NDRF",
        "demo_disclaimer": "DEMO JINGMAHAM — KAM DEI KA JINGPYNMIH BA SHISHA"
    },
    "nag": {
        "lang_code": "nag",
        "lang_name": "Nagamese (Nagamese)",
        "alert_title": "MATI GIRA DANGER KHOBOR / ALERT",
        "location_label": "Jaiga",
        "risk_level_label": "Risk Level",
        "risk_critical": "EKDUM DANGER / GIRA BAKI ASE",
        "risk_high": "DAANGOR DANGER WATCH",
        "risk_moderate": "FIMKHUR KORIBI",
        "risk_low": "SAFE / NORMAL",
        "nearest_shelter_label": "Usar laga Safe Relief Shelter",
        "action_label": "Public Saftey Niyom",
        "action_directive_critical": "Joldi jaiga chari kene ucha pahar rasta dhurikena jabi. Mati bishi gira rasta aru nodi kinar te najabi.",
        "action_directive_high": "Stage-2 Warning: Emergency saman thik rakhikena gari pahar rasta te bishi nachalabi.",
        "action_directive_moderate": "Advisory: Nala safa rakhikena DC / Disaster team laga kotha manibi.",
        "authority_label": "Authority",
        "authority_text": "Nagaland State Disaster Management Authority (NSDMA) & NDRF",
        "demo_disclaimer": "DEMO WARNING — REAL EMERGENCY NAHOI"
    },
    "bn": {
        "lang_code": "bn",
        "lang_name": "বাংলা (Bengali)",
        "alert_title": "মারাত্মক ভূমিধস সংক্রান্ত জরুরি সতর্কবার্তা",
        "location_label": "স্থান",
        "risk_level_label": "ঝুঁকির মাত্রা",
        "risk_critical": "চরম বিপদজনক / অবিলম্বে ধসের সম্ভাবনা (CRITICAL)",
        "risk_high": "উচ্চ বিপদ সতর্কতা",
        "risk_moderate": "মাঝারি সতর্কতা",
        "risk_low": "স্বাভাবিক / নিরাপদ",
        "nearest_shelter_label": "নিকটবর্তী মনোনীত নিরাপদ আশ্রয় কেন্দ্র",
        "action_label": "নাগরিক সুরক্ষা নির্দেশিকা",
        "action_directive_critical": "অবিলম্বে নিরাপদ স্থানে সরে যান। শুধুমাত্র উচ্চ শৈলশিরা পথ ব্যবহার করুন। উপত্যকার কাদা প্রবাহ ও খাড়া ঢাল থেকে দূরে থাকুন।",
        "action_directive_high": "পর্যায়-২ সতর্কতা: জরুরি সামগ্রী প্রস্তুত রাখুন এবং পাহাড়ি রাস্তায় অপ্রয়োজনীয় যাতায়াত বন্ধ রাখুন।",
        "action_directive_moderate": "পরামর্শ: স্থানীয় বিপর্যয় মোকাবিলা দপ্তরের নির্দেশাবলী সতর্কভাবে মেনে চলুন।",
        "authority_label": "প্রদানকারী কর্তৃপক্ষ",
        "authority_text": "রাজ্য বিপর্যয় মোকাবিলা কর্তৃপক্ষ (SDMA) এবং এনডিআরএফ (NDRF)",
        "demo_disclaimer": "ডেমো সতর্কবার্তা — প্রকৃত জরুরি বার্তা নয়"
    }
}

def get_translated_alert(alert_data: Dict[str, Any], lang: str = "en") -> Dict[str, Any]:
    """Generates a localized emergency bulletin dictionary in the selected language."""
    lang_code = lang.lower() if lang.lower() in ALERT_TRANSLATIONS else "en"
    t = ALERT_TRANSLATIONS[lang_code]

    severity = alert_data.get("severity", "CRITICAL").upper()
    if "CRIT" in severity or "EXTREME" in severity:
        risk_text = t["risk_critical"]
        directive = t["action_directive_critical"]
    elif "HIGH" in severity or "SEVERE" in severity:
        risk_text = t["risk_high"]
        directive = t["action_directive_high"]
    elif "MOD" in severity or "WARN" in severity:
        risk_text = t["risk_moderate"]
        directive = t["action_directive_moderate"]
    else:
        risk_text = t["risk_low"]
        directive = t["action_directive_moderate"]

    return {
        "lang_code": lang_code,
        "language_code": lang_code,
        "language_name": t["lang_name"],
        "alert_id": alert_data.get("alert_id", "ALT-DEMO-001"),
        "title": t["alert_title"],
        "location": alert_data.get("region_name", alert_data.get("location", "Tupul, Noney District, Manipur")),
        "state": alert_data.get("state", "Manipur"),
        "risk_level_label": t["risk_level_label"],
        "risk_level": risk_text,
        "nearest_shelter_label": t["nearest_shelter_label"],
        "nearest_shelter": alert_data.get("nearest_shelter", "Noney District Headquarter Safe Relief Shelter"),
        "action_label": t["action_label"],
        "action_directive": directive,
        "issuing_authority": t["authority_text"],
        "disclaimer": t["demo_disclaimer"],
        "timestamp": alert_data.get("timestamp", alert_data.get("created_at", "20:48 UTC+05:30"))
    }
