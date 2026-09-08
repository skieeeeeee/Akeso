"""Punjabi translations, keyed by the English source string.

MACHINE-AUTHORED — pending review by a Punjabi speaker. Clinical phrasing in
particular should be checked: a question that reads oddly to a patient gets a
worse answer, and a worse answer reaches a doctor.

Written in Gurmukhi, as used in Indian Punjab.

Add or correct an entry by editing this file; nothing else needs to change.
An inline `pa=` argument at a `t()` call site always overrides an entry here.

Terminology held consistent throughout: ਮਰੀਜ਼ (patient), ਬਿਮਾਰੀ (illness),
ਦਵਾਈ (medicine), ਜਾਂਚ (test/examination), ਮੁਲਾਕਾਤ (visit), ਸ਼ਿਕਾਇਤ (complaint),
ਨਿਦਾਨ (diagnosis), ਸਹਿਮਤੀ (consent).
"""

from __future__ import annotations

PUNJABI: dict[str, str] = {
    # --- Onboarding steps, greetings and status messages ------------------
    "Health ID": "ਹੈਲਥ ਆਈਡੀ",
    "Your details": "ਤੁਹਾਡੀ ਜਾਣਕਾਰੀ",
    "Comfort check": "ਸਹੂਲਤ ਜਾਂਚ",
    "Your experience": "ਤੁਹਾਡਾ ਅਨੁਭਵ",
    "Consent": "ਸਹਿਮਤੀ",
    "Health history": "ਸਿਹਤ ਇਤਿਹਾਸ",
    "Done": "ਪੂਰਾ",
    "Welcome": "ਜੀ ਆਇਆਂ ਨੂੰ",
    "Welcome back": "ਤੁਹਾਡਾ ਫਿਰ ਸੁਆਗਤ ਹੈ",
    "Sorry, I did not catch that. Please try again, or tap an option.":
        "ਮਾਫ਼ ਕਰਨਾ, ਮੈਨੂੰ ਸਮਝ ਨਹੀਂ ਆਇਆ। ਕਿਰਪਾ ਕਰਕੇ ਦੁਬਾਰਾ ਦੱਸੋ, ਜਾਂ ਕੋਈ ਵਿਕਲਪ ਚੁਣੋ।",
    "Saved. Ready to be read.": "ਸੰਭਾਲ ਲਿਆ। ਪੜ੍ਹਨ ਲਈ ਤਿਆਰ।",
    "Reading your document. This usually takes a few seconds.":
        "ਤੁਹਾਡਾ ਕਾਗਜ਼ ਪੜ੍ਹਿਆ ਜਾ ਰਿਹਾ ਹੈ। ਇਸ ਵਿੱਚ ਆਮ ਤੌਰ ਤੇ ਕੁਝ ਸਕਿੰਟ ਲੱਗਦੇ ਹਨ।",
    "We found some information in this document. Please check it.":
        "ਇਸ ਕਾਗਜ਼ ਵਿੱਚ ਸਾਨੂੰ ਕੁਝ ਜਾਣਕਾਰੀ ਮਿਲੀ। ਕਿਰਪਾ ਕਰਕੇ ਇਸ ਨੂੰ ਦੇਖੋ।",
    "We read the text but could not pick out medical details. "
    "Your doctor can still read it.":
        "ਅਸੀਂ ਲਿਖਤ ਪੜ੍ਹੀ ਪਰ ਡਾਕਟਰੀ ਵੇਰਵਾ ਨਹੀਂ ਕੱਢ ਸਕੇ। "
        "ਤੁਹਾਡੇ ਡਾਕਟਰ ਇਸ ਨੂੰ ਪੜ੍ਹ ਸਕਦੇ ਹਨ।",
    "We could not read this document. It is saved and you can try again.":
        "ਅਸੀਂ ਇਹ ਕਾਗਜ਼ ਨਹੀਂ ਪੜ੍ਹ ਸਕੇ। ਇਹ ਸੰਭਾਲਿਆ ਗਿਆ ਹੈ ਅਤੇ ਤੁਸੀਂ ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰ ਸਕਦੇ ਹੋ।",
    "This summarises what you told us and what your documents say. "
    "It is not a diagnosis, and your doctor will go through it with you.":
        "ਤੁਸੀਂ ਜੋ ਦੱਸਿਆ ਅਤੇ ਤੁਹਾਡੇ ਕਾਗਜ਼ਾਂ ਵਿੱਚ ਜੋ ਲਿਖਿਆ ਹੈ, ਇਹ ਉਸ ਦਾ ਸਾਰ ਹੈ। "
        "ਇਹ ਨਿਦਾਨ ਨਹੀਂ ਹੈ, ਅਤੇ ਤੁਹਾਡੇ ਡਾਕਟਰ ਇਸ ਨੂੰ ਤੁਹਾਡੇ ਨਾਲ ਦੇਖਣਗੇ।",
    "Your visit details have been sent to the care team. Please wait to be called.":
        "ਤੁਹਾਡੀ ਮੁਲਾਕਾਤ ਦੀ ਜਾਣਕਾਰੀ ਦੇਖਭਾਲ ਟੀਮ ਨੂੰ ਭੇਜ ਦਿੱਤੀ ਗਈ ਹੈ। ਕਿਰਪਾ ਕਰਕੇ ਬੁਲਾਏ ਜਾਣ ਤੱਕ ਇੰਤਜ਼ਾਰ ਕਰੋ।",
    "Your visit has been sent and marked urgent. Please stay near the staff desk.":
        "ਤੁਹਾਡੀ ਜਾਣਕਾਰੀ ਭੇਜ ਦਿੱਤੀ ਗਈ ਹੈ ਅਤੇ ਤੁਰੰਤ ਵਜੋਂ ਨਿਸ਼ਾਨਬੱਧ ਕੀਤੀ ਗਈ ਹੈ। "
        "ਕਿਰਪਾ ਕਰਕੇ ਸਟਾਫ਼ ਡੈਸਕ ਦੇ ਨੇੜੇ ਰਹੋ।",

    # --- Accessibility assessment -------------------------------------
    "How comfortable are you using smartphones or digital devices?":
        "ਸਮਾਰਟਫ਼ੋਨ ਜਾਂ ਡਿਜੀਟਲ ਯੰਤਰ ਵਰਤਣ ਵਿੱਚ ਤੁਹਾਨੂੰ ਕਿੰਨਾ ਸੌਖਾ ਲੱਗਦਾ ਹੈ?",
    "This helps us choose how much detail to show on each screen.":
        "ਇਸ ਤੋਂ ਅਸੀਂ ਤੈਅ ਕਰਦੇ ਹਾਂ ਕਿ ਹਰ ਸਕਰੀਨ ਉੱਤੇ ਕਿੰਨਾ ਵੇਰਵਾ ਦਿਖਾਉਣਾ ਹੈ।",
    "Very comfortable": "ਬਹੁਤ ਸੌਖਾ",
    "Somewhat comfortable": "ਕੁਝ ਹੱਦ ਤੱਕ ਸੌਖਾ",
    "I sometimes need help": "ਮੈਨੂੰ ਕਦੇ-ਕਦੇ ਮਦਦ ਦੀ ਲੋੜ ਪੈਂਦੀ ਹੈ",
    "I prefer a simpler experience": "ਮੈਨੂੰ ਸੌਖਾ ਤਰੀਕਾ ਪਸੰਦ ਹੈ",
    "How would you prefer to answer questions?": "ਤੁਸੀਂ ਸਵਾਲਾਂ ਦੇ ਜਵਾਬ ਕਿਵੇਂ ਦੇਣਾ ਚਾਹੋਗੇ?",
    "You can always switch between speaking and tapping later.":
        "ਬੋਲਣ ਅਤੇ ਛੂਹਣ ਵਿਚਕਾਰ ਤੁਸੀਂ ਬਾਅਦ ਵਿੱਚ ਕਦੇ ਵੀ ਬਦਲ ਸਕਦੇ ਹੋ।",
    "By speaking": "ਬੋਲ ਕੇ",
    "By touching options": "ਵਿਕਲਪਾਂ ਨੂੰ ਛੂਹ ਕੇ",
    "Both": "ਦੋਵੇਂ",
    "Do you have difficulty reading text on screens?":
        "ਸਕਰੀਨ ਉੱਤੇ ਲਿਖਿਆ ਪੜ੍ਹਨ ਵਿੱਚ ਤੁਹਾਨੂੰ ਮੁਸ਼ਕਲ ਆਉਂਦੀ ਹੈ?",
    "If reading is hard, we can make text larger and read questions aloud.":
        "ਪੜ੍ਹਨਾ ਔਖਾ ਹੋਵੇ, ਤਾਂ ਅਸੀਂ ਲਿਖਤ ਵੱਡੀ ਕਰ ਸਕਦੇ ਹਾਂ ਅਤੇ ਸਵਾਲ ਉੱਚੀ ਆਵਾਜ਼ ਵਿੱਚ ਪੜ੍ਹ ਸਕਦੇ ਹਾਂ।",
    "Do you have difficulty seeing content on screens?":
        "ਸਕਰੀਨ ਉੱਤੇ ਦੇਖਣ ਵਿੱਚ ਤੁਹਾਨੂੰ ਮੁਸ਼ਕਲ ਆਉਂਦੀ ਹੈ?",
    "We can increase the text size and use stronger colour contrast.":
        "ਅਸੀਂ ਲਿਖਤ ਦਾ ਆਕਾਰ ਵਧਾ ਸਕਦੇ ਹਾਂ ਅਤੇ ਰੰਗਾਂ ਦਾ ਫ਼ਰਕ ਹੋਰ ਸਾਫ਼ ਕਰ ਸਕਦੇ ਹਾਂ।",
    "Do you have difficulty hearing audio instructions?":
        "ਸੁਣਾਈਆਂ ਹਦਾਇਤਾਂ ਸੁਣਨ ਵਿੱਚ ਤੁਹਾਨੂੰ ਮੁਸ਼ਕਲ ਆਉਂਦੀ ਹੈ?",
    "If hearing is hard, nothing in this app will depend on sound.":
        "ਸੁਣਨਾ ਔਖਾ ਹੋਵੇ, ਤਾਂ ਇਸ ਐਪ ਵਿੱਚ ਕੁਝ ਵੀ ਆਵਾਜ਼ ਉੱਤੇ ਨਿਰਭਰ ਨਹੀਂ ਰਹੇਗਾ।",
    "No difficulty": "ਕੋਈ ਮੁਸ਼ਕਲ ਨਹੀਂ",
    "Sometimes": "ਕਦੇ-ਕਦੇ",
    "Yes": "ਹਾਂ",
    "No": "ਨਹੀਂ",
    "Is there anything else that would make this easier for you?":
        "ਤੁਹਾਡੇ ਲਈ ਇਹ ਹੋਰ ਸੌਖਾ ਬਣਾਉਣ ਵਾਲੀ ਕੋਈ ਹੋਰ ਗੱਲ ਹੈ?",
    "This is completely optional. Share only what you want to.":
        "ਇਹ ਪੂਰੀ ਤਰ੍ਹਾਂ ਮਰਜ਼ੀ ਦਾ ਹੈ। ਜੋ ਤੁਸੀਂ ਦੱਸਣਾ ਚਾਹੁੰਦੇ ਹੋ, ਸਿਰਫ਼ ਉਹੀ ਦੱਸੋ।",
    "I find reading and writing difficult": "ਮੈਨੂੰ ਪੜ੍ਹਨ-ਲਿਖਣ ਵਿੱਚ ਮੁਸ਼ਕਲ ਆਉਂਦੀ ਹੈ",
    "I have low vision": "ਮੈਨੂੰ ਘੱਟ ਦਿਖਦਾ ਹੈ",
    "I am hard of hearing": "ਮੈਨੂੰ ਘੱਟ ਸੁਣਦਾ ਹੈ",
    "Tapping the screen is tiring": "ਸਕਰੀਨ ਨੂੰ ਛੂਹਣਾ ਥਕਾਊ ਲੱਗਦਾ ਹੈ",
    "Someone is helping me today": "ਅੱਜ ਕੋਈ ਮੇਰੀ ਮਦਦ ਕਰ ਰਿਹਾ ਹੈ",
    "I use sign language": "ਮੈਂ ਸੰਕੇਤ ਭਾਸ਼ਾ ਵਰਤਦਾ/ਵਰਤਦੀ ਹਾਂ",
    "Before we begin": "ਸ਼ੁਰੂ ਕਰਨ ਤੋਂ ਪਹਿਲਾਂ",
    "Speak your answers": "ਆਪਣੇ ਜਵਾਬ ਬੋਲੋ",
    "Speak or tap, whichever suits": "ਬੋਲੋ ਜਾਂ ਛੂਹੋ — ਜੋ ਸੌਖਾ ਹੋਵੇ",
    "Tap to choose answers": "ਜਵਾਬ ਚੁਣਨ ਲਈ ਛੂਹੋ",
    "One question at a time, large buttons": "ਇੱਕ ਵਾਰੀ ਇੱਕ ਸਵਾਲ, ਵੱਡੇ ਬਟਨ",
    "All options on one screen": "ਸਾਰੇ ਵਿਕਲਪ ਇੱਕੋ ਸਕਰੀਨ ਉੱਤੇ",
    "Standard": "ਮਿਆਰੀ",
    "Easy": "ਸੌਖਾ",
    "Normal": "ਆਮ",
    "Large": "ਵੱਡਾ",
    "Extra large": "ਬਹੁਤ ਵੱਡਾ",
    "Normal colours": "ਆਮ ਰੰਗ",
    "High contrast": "ਵਧੇਰੇ ਸਾਫ਼ ਰੰਗ-ਫ਼ਰਕ",
    "Voice": "ਆਵਾਜ਼",
    "Touch": "ਛੋਹ",
    "Optional": "ਮਰਜ਼ੀ ਦਾ",
    "Usually filled in from your date of birth.": "ਆਮ ਤੌਰ ਤੇ ਤੁਹਾਡੀ ਜਨਮ ਤਾਰੀਖ਼ ਤੋਂ ਭਰਿਆ ਜਾਂਦਾ ਹੈ।",
    "Your doctor needs this to understand your case before you walk in.":
        "ਤੁਹਾਡੇ ਅੰਦਰ ਆਉਣ ਤੋਂ ਪਹਿਲਾਂ ਤੁਹਾਡਾ ਕੇਸ ਸਮਝਣ ਲਈ ਡਾਕਟਰ ਨੂੰ ਇਹ ਲੋੜੀਂਦਾ ਹੈ।",

    # --- Consent -------------------------------------------------------
    "Collecting your health information": "ਤੁਹਾਡੀ ਸਿਹਤ ਸੰਬੰਧੀ ਜਾਣਕਾਰੀ ਇਕੱਠੀ ਕਰਨੀ",
    "Your symptoms, past illnesses, surgeries, medicines, allergies and family history.":
        "ਤੁਹਾਡੇ ਲੱਛਣ, ਪਿਛਲੀਆਂ ਬਿਮਾਰੀਆਂ, ਆਪਰੇਸ਼ਨ, ਦਵਾਈਆਂ, ਐਲਰਜੀ ਅਤੇ ਪਰਿਵਾਰਕ ਇਤਿਹਾਸ।",
    "So your doctor already knows your history and can spend the visit on your actual problem.":
        "ਤਾਂ ਜੋ ਤੁਹਾਡੇ ਡਾਕਟਰ ਨੂੰ ਤੁਹਾਡਾ ਇਤਿਹਾਸ ਪਹਿਲਾਂ ਹੀ ਪਤਾ ਹੋਵੇ ਅਤੇ ਮੁਲਾਕਾਤ ਦਾ ਸਮਾਂ ਤੁਹਾਡੀ ਅਸਲ ਸਮੱਸਿਆ ਉੱਤੇ ਲੱਗੇ।",
    "It is stored against your patient record and shown to the clinician treating you.":
        "ਇਹ ਤੁਹਾਡੇ ਮਰੀਜ਼ ਰਿਕਾਰਡ ਨਾਲ ਸੰਭਾਲਿਆ ਜਾਂਦਾ ਹੈ ਅਤੇ ਤੁਹਾਡਾ ਇਲਾਜ ਕਰਨ ਵਾਲੇ ਡਾਕਟਰ ਨੂੰ ਦਿਖਾਇਆ ਜਾਂਦਾ ਹੈ।",
    "Sharing with your doctor": "ਤੁਹਾਡੇ ਡਾਕਟਰ ਨਾਲ ਸਾਂਝਾ ਕਰਨਾ",
    "A summary of what you tell us today, and any records you upload.":
        "ਅੱਜ ਤੁਸੀਂ ਜੋ ਦੱਸੋਗੇ ਉਸ ਦਾ ਸਾਰ, ਅਤੇ ਤੁਹਾਡੇ ਵੱਲੋਂ ਅਪਲੋਡ ਕੀਤੇ ਰਿਕਾਰਡ।",
    "Only clinicians involved in your care can see it.":
        "ਸਿਰਫ਼ ਤੁਹਾਡੇ ਇਲਾਜ ਨਾਲ ਜੁੜੇ ਡਾਕਟਰ ਹੀ ਇਹ ਦੇਖ ਸਕਦੇ ਹਨ।",
    "Linking your health ID": "ਤੁਹਾਡਾ ਹੈਲਥ ਆਈਡੀ ਜੋੜਨਾ",
    "The health ID number you entered, linked to this patient record.":
        "ਤੁਹਾਡੇ ਵੱਲੋਂ ਦਿੱਤਾ ਹੈਲਥ ਆਈਡੀ ਨੰਬਰ, ਇਸ ਮਰੀਜ਼ ਰਿਕਾਰਡ ਨਾਲ ਜੁੜਿਆ।",
    "So your records can follow you between visits instead of starting over.":
        "ਤਾਂ ਜੋ ਹਰ ਮੁਲਾਕਾਤ ਉੱਤੇ ਨਵੇਂ ਸਿਰੇ ਤੋਂ ਸ਼ੁਰੂ ਕਰਨ ਦੀ ਥਾਂ ਤੁਹਾਡੇ ਰਿਕਾਰਡ ਤੁਹਾਡੇ ਨਾਲ ਰਹਿਣ।",
    "This is a prototype and is not connected to the national ABDM network.":
        "ਇਹ ਇੱਕ ਨਮੂਨਾ ਹੈ ਅਤੇ ਰਾਸ਼ਟਰੀ ABDM ਨੈੱਟਵਰਕ ਨਾਲ ਜੁੜਿਆ ਨਹੀਂ ਹੈ।",
    "We will ask about your health so your doctor is prepared before you meet. "
    "You choose what to share, and you can withdraw your consent at any time.":
        "ਤੁਹਾਡੀ ਮੁਲਾਕਾਤ ਤੋਂ ਪਹਿਲਾਂ ਡਾਕਟਰ ਤਿਆਰ ਹੋਵੇ, ਇਸ ਲਈ ਅਸੀਂ ਤੁਹਾਡੀ ਸਿਹਤ ਬਾਰੇ ਪੁੱਛਾਂਗੇ। "
        "ਕੀ ਸਾਂਝਾ ਕਰਨਾ ਹੈ, ਇਹ ਤੁਸੀਂ ਤੈਅ ਕਰਦੇ ਹੋ, ਅਤੇ ਆਪਣੀ ਸਹਿਮਤੀ ਤੁਸੀਂ ਕਦੇ ਵੀ ਵਾਪਸ ਲੈ ਸਕਦੇ ਹੋ।",
    "You can withdraw consent later from your profile. Nothing is shared without your agreement.":
        "ਤੁਸੀਂ ਬਾਅਦ ਵਿੱਚ ਆਪਣੀ ਪ੍ਰੋਫ਼ਾਈਲ ਤੋਂ ਸਹਿਮਤੀ ਵਾਪਸ ਲੈ ਸਕਦੇ ਹੋ। ਤੁਹਾਡੀ ਰਜ਼ਾਮੰਦੀ ਤੋਂ ਬਿਨਾਂ ਕੁਝ ਵੀ ਸਾਂਝਾ ਨਹੀਂ ਕੀਤਾ ਜਾਂਦਾ।",

    # --- Red flags / safety --------------------------------------------
    "Please speak to healthcare staff now": "ਕਿਰਪਾ ਕਰਕੇ ਹੁਣ ਸਿਹਤ ਕਰਮਚਾਰੀਆਂ ਨਾਲ ਗੱਲ ਕਰੋ",
    "Some of the symptoms you described may require urgent medical attention.":
        "ਤੁਹਾਡੇ ਦੱਸੇ ਕੁਝ ਲੱਛਣਾਂ ਨੂੰ ਤੁਰੰਤ ਡਾਕਟਰੀ ਧਿਆਨ ਦੀ ਲੋੜ ਹੋ ਸਕਦੀ ਹੈ।",
    "Please inform nearby healthcare staff immediately. Show them this screen.":
        "ਕਿਰਪਾ ਕਰਕੇ ਨੇੜਲੇ ਸਿਹਤ ਕਰਮਚਾਰੀਆਂ ਨੂੰ ਤੁਰੰਤ ਦੱਸੋ। ਉਨ੍ਹਾਂ ਨੂੰ ਇਹ ਸਕਰੀਨ ਦਿਖਾਓ।",
    "This does not confirm a medical condition. It only means a health worker should "
    "look at you sooner rather than later.":
        "ਇਸ ਨਾਲ ਕੋਈ ਬਿਮਾਰੀ ਪੱਕੀ ਨਹੀਂ ਹੁੰਦੀ। ਇਸ ਦਾ ਮਤਲਬ ਸਿਰਫ਼ ਇਹ ਹੈ ਕਿ ਸਿਹਤ ਕਰਮਚਾਰੀ "
        "ਤੁਹਾਨੂੰ ਦੇਰ ਨਾਲ ਨਹੀਂ, ਸਗੋਂ ਛੇਤੀ ਦੇਖੇ।",
    "Marked urgent — please stay near the staff desk.":
        "ਤੁਰੰਤ ਵਜੋਂ ਨਿਸ਼ਾਨਬੱਧ — ਕਿਰਪਾ ਕਰਕੇ ਸਟਾਫ਼ ਡੈਸਕ ਦੇ ਨੇੜੇ ਰਹੋ।",
    "Continue answering while waiting": "ਇੰਤਜ਼ਾਰ ਦੌਰਾਨ ਜਵਾਬ ਦਿੰਦੇ ਰਹੋ",
    "I need immediate assistance": "ਮੈਨੂੰ ਤੁਰੰਤ ਮਦਦ ਦੀ ਲੋੜ ਹੈ",

    # --- Medical profile sections --------------------------------------
    "Why you are here": "ਤੁਸੀਂ ਇੱਥੇ ਕਿਉਂ ਆਏ ਹੋ",
    "First, tell us what brings you in today.": "ਪਹਿਲਾਂ, ਅੱਜ ਤੁਸੀਂ ਕਿਸ ਲਈ ਆਏ ਹੋ ਇਹ ਦੱਸੋ।",
    "What problem brings you in today?": "ਅੱਜ ਕਿਸ ਸਮੱਸਿਆ ਲਈ ਤੁਸੀਂ ਆਏ ਹੋ?",
    "Describe it in your own words. You can speak instead of typing.":
        "ਆਪਣੇ ਸ਼ਬਦਾਂ ਵਿੱਚ ਦੱਸੋ। ਟਾਈਪ ਕਰਨ ਦੀ ਥਾਂ ਤੁਸੀਂ ਬੋਲ ਸਕਦੇ ਹੋ।",
    "e.g. chest pain for three days": "ਜਿਵੇਂ ਤਿੰਨ ਦਿਨਾਂ ਤੋਂ ਛਾਤੀ ਵਿੱਚ ਦਰਦ",
    "About this problem": "ਇਸ ਸਮੱਸਿਆ ਬਾਰੇ",
    "How long has it been there, and what makes it better or worse?":
        "ਇਹ ਕਿੰਨੇ ਸਮੇਂ ਤੋਂ ਹੈ, ਅਤੇ ਕਿਸ ਨਾਲ ਠੀਕ ਜਾਂ ਵੱਧ ਲੱਗਦਾ ਹੈ?",
    "How long have you had this?": "ਇਹ ਤੁਹਾਨੂੰ ਕਿੰਨੇ ਸਮੇਂ ਤੋਂ ਹੈ?",
    "A rough idea is fine.": "ਅੰਦਾਜ਼ਾ ਦੱਸ ਦਿਓ ਤਾਂ ਵੀ ਚੱਲੇਗਾ।",
    "Started today": "ਅੱਜ ਸ਼ੁਰੂ ਹੋਇਆ",
    "2–3 days": "੨–੩ ਦਿਨ",
    "About a week": "ਲਗਭਗ ਇੱਕ ਹਫ਼ਤਾ",
    "A few weeks": "ਕੁਝ ਹਫ਼ਤੇ",
    "More than a month": "ਇੱਕ ਮਹੀਨੇ ਤੋਂ ਵੱਧ",
    "How much does it trouble you, from 1 to 10?": "ਇਹ ਤੁਹਾਨੂੰ ੧ ਤੋਂ ੧੦ ਵਿੱਚ ਕਿੰਨੀ ਤਕਲੀਫ਼ ਦਿੰਦਾ ਹੈ?",
    "1 is very mild, 10 is the worst.": "੧ ਦਾ ਮਤਲਬ ਬਹੁਤ ਹਲਕਾ, ੧੦ ਦਾ ਮਤਲਬ ਸਭ ਤੋਂ ਵੱਧ।",
    "Is there anything that makes it better or worse?":
        "ਕਿਸ ਨਾਲ ਇਹ ਠੀਕ ਜਾਂ ਵੱਧ ਹੁੰਦਾ ਹੈ, ਇਹੋ ਜਿਹਾ ਕੁਝ ਹੈ?",
    "For example rest, food, walking, or a medicine you took.":
        "ਜਿਵੇਂ ਅਰਾਮ, ਖਾਣਾ, ਤੁਰਨਾ, ਜਾਂ ਤੁਹਾਡੀ ਲਈ ਹੋਈ ਦਵਾਈ।",
    "Anything else you feel": "ਤੁਹਾਨੂੰ ਮਹਿਸੂਸ ਹੁੰਦਾ ਕੁਝ ਹੋਰ",
    "A quick check for other symptoms.": "ਹੋਰ ਲੱਛਣਾਂ ਦੀ ਛੇਤੀ ਜਾਂਚ।",
    "Are you also feeling any of these?": "ਤੁਹਾਨੂੰ ਇਨ੍ਹਾਂ ਵਿੱਚੋਂ ਕੁਝ ਮਹਿਸੂਸ ਹੋ ਰਿਹਾ ਹੈ?",
    "Choose as many as you like.": "ਜਿੰਨੇ ਚਾਹੋ ਵਿਕਲਪ ਚੁਣੋ।",
    "Fever": "ਬੁਖ਼ਾਰ",
    "Cough": "ਖੰਘ",
    "Breathlessness": "ਸਾਹ ਚੜ੍ਹਨਾ",
    "Short of breath": "ਦਮ ਚੜ੍ਹਨਾ",
    "Headache": "ਸਿਰ ਦਰਦ",
    "Dizziness": "ਚੱਕਰ",
    "Vomiting": "ਉਲਟੀ",
    "Loose motions": "ਦਸਤ",
    "Swelling": "ਸੋਜ",
    "Pain": "ਦਰਦ",
    "Very tired": "ਬਹੁਤ ਥਕਾਵਟ",
    "Losing weight": "ਭਾਰ ਘਟਣਾ",
    "Not sleeping well": "ਨੀਂਦ ਨਾ ਆਉਣਾ",
    "Stomach pain": "ਪੇਟ ਦਰਦ",
    "Stomach problem": "ਪੇਟ ਦੀ ਤਕਲੀਫ਼",
    "Chest pain": "ਛਾਤੀ ਵਿੱਚ ਦਰਦ",

    # --- Past illnesses -------------------------------------------------
    "Past illnesses": "ਪਿਛਲੀਆਂ ਬਿਮਾਰੀਆਂ",
    "Now a few questions about long-term health conditions.":
        "ਹੁਣ ਲੰਬੇ ਸਮੇਂ ਦੀਆਂ ਬਿਮਾਰੀਆਂ ਬਾਰੇ ਕੁਝ ਸਵਾਲ।",
    "Has a doctor told you that you have a long-term illness?":
        "ਤੁਹਾਨੂੰ ਲੰਬੇ ਸਮੇਂ ਦੀ ਬਿਮਾਰੀ ਹੈ, ਇਹ ਡਾਕਟਰ ਨੇ ਦੱਸਿਆ ਹੈ?",
    "Such as diabetes, blood pressure or asthma.": "ਜਿਵੇਂ ਸ਼ੂਗਰ, ਬਲੱਡ ਪ੍ਰੈਸ਼ਰ ਜਾਂ ਦਮਾ।",
    "Any long-term illness you have been told you have?":
        "ਤੁਹਾਨੂੰ ਹੈ ਇਹ ਦੱਸੀ ਗਈ ਕੋਈ ਲੰਬੇ ਸਮੇਂ ਦੀ ਬਿਮਾਰੀ?",
    "Which illness?": "ਕਿਹੜੀ ਬਿਮਾਰੀ?",
    "Any old illness?": "ਪੁਰਾਣੀ ਕੋਈ ਬਿਮਾਰੀ?",
    "Ongoing conditions": "ਚੱਲ ਰਹੀਆਂ ਬਿਮਾਰੀਆਂ",
    "Diabetes": "ਸ਼ੂਗਰ",
    "High blood pressure": "ਵੱਧ ਬਲੱਡ ਪ੍ਰੈਸ਼ਰ",
    "Asthma": "ਦਮਾ",
    "Heart disease": "ਦਿਲ ਦੀ ਬਿਮਾਰੀ",
    "Thyroid problem": "ਥਾਇਰਾਇਡ ਦੀ ਤਕਲੀਫ਼",
    "Tuberculosis": "ਤਪਦਿਕ",
    "Cancer": "ਕੈਂਸਰ",
    "Something else": "ਕੁਝ ਹੋਰ",
    "Are you currently taking medicine for {item}?":
        "{item} ਲਈ ਤੁਸੀਂ ਹੁਣ ਦਵਾਈ ਲੈ ਰਹੇ ਹੋ?",
    "Do you remember the name of the medicine for {item}?":
        "{item} ਲਈ ਦਵਾਈ ਦਾ ਨਾਂ ਤੁਹਾਨੂੰ ਯਾਦ ਹੈ?",
    "If you are not sure, you can skip this or upload the prescription later.":
        "ਪੱਕਾ ਪਤਾ ਨਾ ਹੋਵੇ, ਤਾਂ ਇਹ ਛੱਡ ਦਿਓ ਜਾਂ ਬਾਅਦ ਵਿੱਚ ਦਵਾਈ ਦੀ ਪਰਚੀ ਅਪਲੋਡ ਕਰੋ।",

    # --- Operations -----------------------------------------------------
    "Operations": "ਆਪਰੇਸ਼ਨ",
    "Have you ever had an operation?": "ਤੁਹਾਡਾ ਕਦੇ ਆਪਰੇਸ਼ਨ ਹੋਇਆ ਹੈ?",
    "Have you had any operation?": "ਤੁਹਾਡਾ ਕੋਈ ਆਪਰੇਸ਼ਨ ਹੋਇਆ ਹੈ?",
    "Any operation, however long ago.": "ਕੋਈ ਵੀ ਆਪਰੇਸ਼ਨ, ਭਾਵੇਂ ਕਿੰਨਾ ਪੁਰਾਣਾ ਹੋਵੇ।",
    "What operation, and roughly when?": "ਕਿਹੜਾ ਆਪਰੇਸ਼ਨ, ਅਤੇ ਲਗਭਗ ਕਦੋਂ?",
    "For example: gallbladder removed, 2019.": "ਜਿਵੇਂ: ਪਿੱਤੇ ਦੀ ਥੈਲੀ ਕਢਵਾਈ, ੨੦੧੯।",
    "e.g. gallbladder removed, 2019": "ਜਿਵੇਂ ਪਿੱਤੇ ਦੀ ਥੈਲੀ ਕਢਵਾਈ, ੨੦੧੯",

    # --- Medicines ------------------------------------------------------
    "Medicines": "ਦਵਾਈਆਂ",
    "Medicines you take": "ਤੁਹਾਡੀਆਂ ਲਈਆਂ ਜਾਂਦੀਆਂ ਦਵਾਈਆਂ",
    "Let us record the medicines you take.": "ਤੁਹਾਡੀਆਂ ਲਈਆਂ ਜਾਂਦੀਆਂ ਦਵਾਈਆਂ ਦਰਜ ਕਰੀਏ।",
    "Which medicines do you take regularly?": "ਤੁਸੀਂ ਨਿਯਮਿਤ ਕਿਹੜੀਆਂ ਦਵਾਈਆਂ ਲੈਂਦੇ ਹੋ?",
    "Which medicines are you taking now?": "ਤੁਸੀਂ ਹੁਣ ਕਿਹੜੀਆਂ ਦਵਾਈਆਂ ਲੈ ਰਹੇ ਹੋ?",
    "Any daily medicine?": "ਰੋਜ਼ ਦੀ ਕੋਈ ਦਵਾਈ?",
    "Include tablets, insulin, inhalers and drops.":
        "ਗੋਲੀਆਂ, ਇਨਸੁਲਿਨ, ਇਨਹੇਲਰ ਅਤੇ ਤੁਪਕੇ ਵੀ ਦੱਸੋ।",
    "Add them one at a time. Tap a common answer or say it aloud.":
        "ਇੱਕ ਵਾਰੀ ਇੱਕ ਜੋੜੋ। ਆਮ ਜਵਾਬ ਨੂੰ ਛੂਹੋ ਜਾਂ ਉੱਚੀ ਆਵਾਜ਼ ਵਿੱਚ ਬੋਲੋ।",
    "Add them one at a time.": "ਇੱਕ ਵਾਰੀ ਇੱਕ ਜੋੜੋ।",
    "e.g. Metformin 500 mg twice a day": "ਜਿਵੇਂ ਮੈਟਫਾਰਮਿਨ ੫੦੦ ਮਿ.ਗ੍ਰਾ. ਦਿਨ ਵਿੱਚ ਦੋ ਵਾਰ",

    # --- Allergies ------------------------------------------------------
    "Allergies": "ਐਲਰਜੀ",
    "Medicine problems": "ਦਵਾਈ ਦੀ ਤਕਲੀਫ਼",
    "This one matters a lot for your safety.": "ਤੁਹਾਡੀ ਸੁਰੱਖਿਆ ਲਈ ਇਹ ਬਹੁਤ ਜ਼ਰੂਰੀ ਹੈ।",
    "Are you allergic to any medicine or food?":
        "ਤੁਹਾਨੂੰ ਕਿਸੇ ਦਵਾਈ ਜਾਂ ਖਾਣੇ ਦੀ ਐਲਰਜੀ ਹੈ?",
    "Any allergy?": "ਕੋਈ ਐਲਰਜੀ?",
    "Has any medicine ever caused you a problem?":
        "ਕਿਸੇ ਦਵਾਈ ਨਾਲ ਤੁਹਾਨੂੰ ਕਦੇ ਤਕਲੀਫ਼ ਹੋਈ ਹੈ?",
    "Tell us even if you are unsure — it keeps you safe.":
        "ਪੱਕਾ ਪਤਾ ਨਾ ਹੋਵੇ ਤਾਂ ਵੀ ਦੱਸੋ — ਇਸ ਨਾਲ ਤੁਸੀਂ ਸੁਰੱਖਿਅਤ ਰਹਿੰਦੇ ਹੋ।",
    "For example it upset your stomach, or you had to stop it.":
        "ਜਿਵੇਂ ਪੇਟ ਖ਼ਰਾਬ ਹੋਇਆ, ਜਾਂ ਉਹ ਬੰਦ ਕਰਨੀ ਪਈ।",
    "Which ones?": "ਕਿਹੜੀਆਂ?",
    "Penicillin": "ਪੈਨਿਸਿਲਿਨ",
    "Aspirin": "ਐਸਪਰੀਨ",
    "Sulfa drugs": "ਸਲਫ਼ਾ ਦਵਾਈਆਂ",
    "Dust": "ਧੂੜ",
    "No known allergies": "ਜਾਣੀ-ਪਛਾਣੀ ਕੋਈ ਐਲਰਜੀ ਨਹੀਂ",
    "e.g. penicillin, peanuts": "ਜਿਵੇਂ ਪੈਨਿਸਿਲਿਨ, ਮੂੰਗਫਲੀ",
    "e.g. aspirin upset my stomach": "ਜਿਵੇਂ ਐਸਪਰੀਨ ਨਾਲ ਮੇਰਾ ਪੇਟ ਖ਼ਰਾਬ ਹੋਇਆ",

    # --- Family and personal history ------------------------------------
    "Family health": "ਪਰਿਵਾਰਕ ਸਿਹਤ",
    "Some illnesses run in families.": "ਕੁਝ ਬਿਮਾਰੀਆਂ ਪਰਿਵਾਰ ਵਿੱਚ ਚੱਲਦੀਆਂ ਆਉਂਦੀਆਂ ਹਨ।",
    "Does any illness run in your close family?":
        "ਤੁਹਾਡੇ ਨੇੜਲੇ ਪਰਿਵਾਰ ਵਿੱਚ ਕੋਈ ਬਿਮਾਰੀ ਚੱਲਦੀ ਆਉਂਦੀ ਹੈ?",
    "Any illness that runs in your family?": "ਤੁਹਾਡੇ ਪਰਿਵਾਰ ਵਿੱਚ ਚੱਲਦੀ ਆਉਂਦੀ ਕੋਈ ਬਿਮਾਰੀ?",
    "Any illness in the family?": "ਪਰਿਵਾਰ ਵਿੱਚ ਕੋਈ ਬਿਮਾਰੀ?",
    "Parents, brothers, sisters or children.": "ਮਾਤਾ-ਪਿਤਾ, ਭਾਈ, ਭੈਣਾਂ ਜਾਂ ਬੱਚੇ।",
    "Family history": "ਪਰਿਵਾਰਕ ਇਤਿਹਾਸ",
    "e.g. mother has diabetes": "ਜਿਵੇਂ ਮਾਤਾ ਨੂੰ ਸ਼ੂਗਰ ਹੈ",
    "Daily habits": "ਰੋਜ਼ ਦੀਆਂ ਆਦਤਾਂ",
    "Daily life": "ਰੋਜ਼ ਦੀ ਜ਼ਿੰਦਗੀ",
    "A few questions about your habits and routine.":
        "ਤੁਹਾਡੀਆਂ ਆਦਤਾਂ ਅਤੇ ਦਿਨਚਰਿਆ ਬਾਰੇ ਕੁਝ ਸਵਾਲ।",
    "Anything about your habits your doctor should know?":
        "ਤੁਹਾਡੀਆਂ ਆਦਤਾਂ ਬਾਰੇ ਡਾਕਟਰ ਨੂੰ ਪਤਾ ਹੋਣਾ ਚਾਹੀਦਾ, ਇਹੋ ਜਿਹਾ ਕੁਝ ਹੈ?",
    "Which of these apply to you?": "ਇਨ੍ਹਾਂ ਵਿੱਚੋਂ ਕਿਹੜਾ ਤੁਹਾਡੇ ਉੱਤੇ ਲਾਗੂ ਹੁੰਦਾ ਹੈ?",
    "I do not smoke": "ਮੈਂ ਸਿਗਰਟ ਨਹੀਂ ਪੀਂਦਾ/ਪੀਂਦੀ",
    "I smoke": "ਮੈਂ ਸਿਗਰਟ ਪੀਂਦਾ/ਪੀਂਦੀ ਹਾਂ",
    "I do not drink alcohol": "ਮੈਂ ਸ਼ਰਾਬ ਨਹੀਂ ਪੀਂਦਾ/ਪੀਂਦੀ",
    "I drink alcohol": "ਮੈਂ ਸ਼ਰਾਬ ਪੀਂਦਾ/ਪੀਂਦੀ ਹਾਂ",
    "I exercise regularly": "ਮੈਂ ਨਿਯਮਿਤ ਕਸਰਤ ਕਰਦਾ/ਕਰਦੀ ਹਾਂ",
    "Vegetarian diet": "ਸ਼ਾਕਾਹਾਰੀ ਖ਼ੁਰਾਕ",
    "Non-smoker": "ਸਿਗਰਟ ਨਾ ਪੀਣ ਵਾਲਾ",
    "Smoker": "ਸਿਗਰਟ ਪੀਣ ਵਾਲਾ",
    "No alcohol": "ਸ਼ਰਾਬ ਨਹੀਂ",
    "What work do you do?": "ਤੁਸੀਂ ਕੀ ਕੰਮ ਕਰਦੇ ਹੋ?",
    "Some jobs affect health, so this can be useful.":
        "ਕੁਝ ਕੰਮਾਂ ਦਾ ਸਿਹਤ ਉੱਤੇ ਅਸਰ ਪੈਂਦਾ ਹੈ, ਇਸ ਲਈ ਇਹ ਲਾਭਦਾਇਕ ਹੋ ਸਕਦਾ ਹੈ।",
    "e.g. non-smoker, vegetarian diet": "ਜਿਵੇਂ ਸਿਗਰਟ ਨਾ ਪੀਣ ਵਾਲਾ, ਸ਼ਾਕਾਹਾਰੀ ਖ਼ੁਰਾਕ",
    "e.g. diabetes, high blood pressure": "ਜਿਵੇਂ ਸ਼ੂਗਰ, ਵੱਧ ਬਲੱਡ ਪ੍ਰੈਸ਼ਰ",

    # --- Investigations --------------------------------------------------
    "Earlier tests": "ਪਿਛਲੀਆਂ ਜਾਂਚਾਂ",
    "Earlier test results": "ਪਿਛਲੀਆਂ ਜਾਂਚਾਂ ਦੇ ਨਤੀਜੇ",
    "Any tests you have had done recently.": "ਹਾਲ ਵਿੱਚ ਤੁਹਾਡੀ ਕਰਵਾਈ ਕੋਈ ਜਾਂਚ।",
    "Have you had any blood test or scan recently?":
        "ਹਾਲ ਵਿੱਚ ਤੁਹਾਡੇ ਖ਼ੂਨ ਦੀ ਜਾਂਚ ਜਾਂ ਸਕੈਨ ਹੋਇਆ ਹੈ?",
    "Any recent test result you remember?":
        "ਹਾਲ ਦਾ ਕੋਈ ਜਾਂਚ ਨਤੀਜਾ ਤੁਹਾਨੂੰ ਯਾਦ ਹੈ?",
    "In the last year or so.": "ਪਿਛਲੇ ਇੱਕ ਸਾਲ ਵਿੱਚ।",
    "Which test, and what did it show?": "ਕਿਹੜੀ ਜਾਂਚ, ਅਤੇ ਉਸ ਵਿੱਚ ਕੀ ਆਇਆ?",
    "If you have the report, you can upload it in the next step instead.":
        "ਰਿਪੋਰਟ ਹੋਵੇ, ਤਾਂ ਅਗਲੇ ਪੜਾਅ ਵਿੱਚ ਤੁਸੀਂ ਉਹ ਅਪਲੋਡ ਕਰ ਸਕਦੇ ਹੋ।",
    "e.g. HbA1c 8.4% in March": "ਜਿਵੇਂ ਮਾਰਚ ਵਿੱਚ HbA1c ੮.੪%",

    # --- Anything else ---------------------------------------------------
    "Anything else": "ਕੁਝ ਹੋਰ",
    "Anything else you would like your doctor to know?":
        "ਤੁਹਾਡੇ ਡਾਕਟਰ ਨੂੰ ਪਤਾ ਹੋਣਾ ਚਾਹੀਦਾ, ਇਹੋ ਜਿਹਾ ਕੁਝ ਹੋਰ ਹੈ?",
    "Are you also feeling anything else?": "ਤੁਹਾਨੂੰ ਕੁਝ ਹੋਰ ਵੀ ਮਹਿਸੂਸ ਹੋ ਰਿਹਾ ਹੈ?",
    "Could you tell us a little more?": "ਤੁਸੀਂ ਥੋੜ੍ਹਾ ਹੋਰ ਦੱਸ ਸਕਦੇ ਹੋ?",
    "Yes or no is enough.": "ਹਾਂ ਜਾਂ ਨਹੀਂ ਹੀ ਕਾਫ਼ੀ ਹੈ।",
    "Choose as many as apply.": "ਜੋ ਲਾਗੂ ਹੋਣ, ਉਹ ਸਾਰੇ ਚੁਣੋ।",
    "This question was suggested from what you just said. You can skip it.":
        "ਤੁਸੀਂ ਹੁਣੇ ਜੋ ਕਿਹਾ, ਉਸ ਤੋਂ ਇਹ ਸਵਾਲ ਸੁਝਾਇਆ ਗਿਆ ਹੈ। ਤੁਸੀਂ ਇਹ ਛੱਡ ਸਕਦੇ ਹੋ।",
    "Optional questions used in Ayurvedic practice.":
        "ਆਯੁਰਵੈਦਿਕ ਇਲਾਜ ਵਿੱਚ ਵਰਤੇ ਜਾਂਦੇ ਮਰਜ਼ੀ ਦੇ ਸਵਾਲ।",

    # --- Encounter script (today's visit) -------------------------------
    "Type of treatment": "ਇਲਾਜ ਦੀ ਕਿਸਮ",
    "First, tell us which kind of care you are here for.":
        "ਪਹਿਲਾਂ, ਤੁਸੀਂ ਕਿਸ ਕਿਸਮ ਦੇ ਇਲਾਜ ਲਈ ਆਏ ਹੋ ਇਹ ਦੱਸੋ।",
    "Which kind of treatment are you here for?":
        "ਤੁਸੀਂ ਕਿਸ ਕਿਸਮ ਦੇ ਇਲਾਜ ਲਈ ਆਏ ਹੋ?",
    "Which treatment?": "ਕਿਹੜਾ ਇਲਾਜ?",
    "This decides which questions we ask. You can pick a different one next time.":
        "ਇਸ ਤੋਂ ਤੈਅ ਹੁੰਦਾ ਹੈ ਕਿ ਅਸੀਂ ਕਿਹੜੇ ਸਵਾਲ ਪੁੱਛਾਂਗੇ। ਅਗਲੀ ਵਾਰ ਤੁਸੀਂ ਵੱਖਰਾ ਚੁਣ ਸਕਦੇ ਹੋ।",
    "Modern medicine (Allopathy)": "ਆਧੁਨਿਕ ਇਲਾਜ (ਐਲੋਪੈਥੀ)",
    "Allopathy": "ਐਲੋਪੈਥੀ",
    "Ayurveda": "ਆਯੁਰਵੇਦ",
    "Homoeopathy": "ਹੋਮਿਓਪੈਥੀ",
    "Unani": "ਯੂਨਾਨੀ",
    "Siddha": "ਸਿੱਧ",
    "Yoga & Naturopathy": "ਯੋਗ ਅਤੇ ਕੁਦਰਤੀ ਇਲਾਜ",
    "Yoga and Naturopathy": "ਯੋਗ ਅਤੇ ਕੁਦਰਤੀ ਇਲਾਜ",
    "I am not sure": "ਮੈਨੂੰ ਪੱਕਾ ਪਤਾ ਨਹੀਂ",
    "Today's concern": "ਅੱਜ ਦੀ ਸ਼ਿਕਾਇਤ",
    "A few questions about this problem only.": "ਸਿਰਫ਼ ਇਸ ਸਮੱਸਿਆ ਬਾਰੇ ਕੁਝ ਸਵਾਲ।",
    "We already have your health history. Just tell us what is new.":
        "ਤੁਹਾਡਾ ਸਿਹਤ ਇਤਿਹਾਸ ਸਾਡੇ ਕੋਲ ਹੈ। ਸਿਰਫ਼ ਨਵਾਂ ਕੀ ਹੈ ਇਹ ਦੱਸੋ।",
    "Tell us what is troubling you today.": "ਅੱਜ ਤੁਹਾਨੂੰ ਕੀ ਤਕਲੀਫ਼ ਹੈ ਇਹ ਦੱਸੋ।",
    "What is troubling you today?": "ਅੱਜ ਤੁਹਾਨੂੰ ਕੀ ਤਕਲੀਫ਼ ਹੈ?",
    "What is troubling you?": "ਤੁਹਾਨੂੰ ਕੀ ਤਕਲੀਫ਼ ਹੈ?",
    "What brings you here today?": "ਅੱਜ ਤੁਸੀਂ ਕਿਸ ਲਈ ਆਏ ਹੋ?",
    "In your own words. You can speak instead of typing.":
        "ਆਪਣੇ ਸ਼ਬਦਾਂ ਵਿੱਚ। ਟਾਈਪ ਕਰਨ ਦੀ ਥਾਂ ਤੁਸੀਂ ਬੋਲ ਸਕਦੇ ਹੋ।",
    "When did it start?": "ਇਹ ਕਦੋਂ ਸ਼ੁਰੂ ਹੋਇਆ?",
    "Since when?": "ਕਦੋਂ ਤੋਂ?",
    "Today": "ਅੱਜ",
    "Yesterday": "ਕੱਲ੍ਹ",
    "2–3 days ago": "੨–੩ ਦਿਨ ਪਹਿਲਾਂ",
    "About a week ago": "ਲਗਭਗ ਇੱਕ ਹਫ਼ਤਾ ਪਹਿਲਾਂ",
    "Longer than a week": "ਇੱਕ ਹਫ਼ਤੇ ਤੋਂ ਵੱਧ",
    "A few details": "ਥੋੜ੍ਹਾ ਵੇਰਵਾ",
    "Can you describe it a little more?": "ਤੁਸੀਂ ਇਸ ਬਾਰੇ ਥੋੜ੍ਹਾ ਹੋਰ ਦੱਸ ਸਕਦੇ ਹੋ?",
    "For example where it is, what it feels like, or what makes it worse.":
        "ਜਿਵੇਂ ਇਹ ਕਿੱਥੇ ਹੈ, ਕਿਹੋ ਜਿਹਾ ਲੱਗਦਾ ਹੈ, ਜਾਂ ਕਿਸ ਨਾਲ ਵਧਦਾ ਹੈ।",
    "How bad is it?": "ਕਿੰਨੀ ਤਕਲੀਫ਼ ਹੈ?",
    "How much is it troubling you, from 1 to 10?":
        "ਇਹ ਤੁਹਾਨੂੰ ੧ ਤੋਂ ੧੦ ਵਿੱਚ ਕਿੰਨੀ ਤਕਲੀਫ਼ ਦੇ ਰਿਹਾ ਹੈ?",
    "Is anything else happening as well?": "ਇਸ ਦੇ ਨਾਲ ਕੁਝ ਹੋਰ ਵੀ ਹੋ ਰਿਹਾ ਹੈ?",
    "Only choose what you actually feel.": "ਜੋ ਤੁਹਾਨੂੰ ਸੱਚਮੁੱਚ ਮਹਿਸੂਸ ਹੁੰਦਾ ਹੈ, ਸਿਰਫ਼ ਉਹੀ ਚੁਣੋ।",
    "Have you taken anything for it?": "ਇਸ ਲਈ ਤੁਸੀਂ ਕੁਝ ਲਿਆ ਹੈ?",
    "Any medicine or home remedy, even if it did not help.":
        "ਕੋਈ ਵੀ ਦਵਾਈ ਜਾਂ ਘਰੇਲੂ ਨੁਸਖ਼ਾ, ਭਾਵੇਂ ਉਸ ਦਾ ਫ਼ਾਇਦਾ ਨਾ ਹੋਇਆ ਹੋਵੇ।",
    "Anything changed?": "ਕੁਝ ਬਦਲਿਆ ਹੈ?",
    "Have your regular medicines changed since your last visit?":
        "ਪਿਛਲੀ ਮੁਲਾਕਾਤ ਤੋਂ ਬਾਅਦ ਤੁਹਾਡੀਆਂ ਨਿਯਮਿਤ ਦਵਾਈਆਂ ਬਦਲੀਆਂ ਹਨ?",
    "We already have your earlier list — only tell us what changed.":
        "ਤੁਹਾਡੀ ਪਹਿਲੀ ਸੂਚੀ ਸਾਡੇ ਕੋਲ ਹੈ — ਸਿਰਫ਼ ਕੀ ਬਦਲਿਆ ਇਹ ਦੱਸੋ।",
    "What has changed?": "ਕੀ ਬਦਲਿਆ ਹੈ?",
    "A medicine you started, stopped, or now take differently.":
        "ਤੁਹਾਡੀ ਸ਼ੁਰੂ ਕੀਤੀ, ਬੰਦ ਕੀਤੀ, ਜਾਂ ਹੁਣ ਵੱਖਰੇ ਤਰੀਕੇ ਨਾਲ ਲਈ ਜਾਂਦੀ ਦਵਾਈ।",
    "Has a doctor told you about any new condition since then?":
        "ਉਸ ਤੋਂ ਬਾਅਦ ਡਾਕਟਰ ਨੇ ਤੁਹਾਨੂੰ ਕਿਸੇ ਨਵੀਂ ਬਿਮਾਰੀ ਬਾਰੇ ਦੱਸਿਆ ਹੈ?",
    "Only something new.": "ਸਿਰਫ਼ ਨਵਾਂ ਹੋਵੇ ਤਾਂ।",
    "What was it?": "ਉਹ ਕੀ ਸੀ?",
    "This is your space.": "ਇਹ ਤੁਹਾਡੀ ਥਾਂ ਹੈ।",
    "Anything else you want the doctor to know today?":
        "ਅੱਜ ਡਾਕਟਰ ਨੂੰ ਪਤਾ ਹੋਣਾ ਚਾਹੀਦਾ, ਇਹੋ ਜਿਹਾ ਕੁਝ ਹੋਰ ਹੈ?",
    "Only here for a check-up": "ਸਿਰਫ਼ ਜਾਂਚ ਲਈ ਆਇਆ/ਆਈ ਹਾਂ",
    "Hospital visit": "ਹਸਪਤਾਲ ਦੀ ਮੁਲਾਕਾਤ",

    # --- AYUSH: Dashavidha ----------------------------------------------
    "Ten-fold examination": "ਦਸ਼ਵਿਧ ਪਰੀਕਸ਼ਾ",
    "Dashavidha Pariksha — questions about your constitution.":
        "ਦਸ਼ਵਿਧ ਪਰੀਕਸ਼ਾ — ਤੁਹਾਡੀ ਪ੍ਰਕ੍ਰਿਤੀ ਬਾਰੇ ਸਵਾਲ।",
    "Prakriti": "ਪ੍ਰਕ੍ਰਿਤੀ",
    "Which best describes your natural build and temperament?":
        "ਤੁਹਾਡੇ ਕੁਦਰਤੀ ਸਰੀਰ ਅਤੇ ਸੁਭਾਅ ਨੂੰ ਕਿਹੜਾ ਸਭ ਤੋਂ ਵਧੀਆ ਬਿਆਨ ਕਰਦਾ ਹੈ?",
    "Your lifelong tendency, not how you feel today.":
        "ਤੁਹਾਡੀ ਸਾਰੀ ਉਮਰ ਦੀ ਪ੍ਰਵਿਰਤੀ, ਅੱਜ ਦੀ ਹਾਲਤ ਨਹੀਂ।",
    "Vikriti": "ਵਿਕ੍ਰਿਤੀ",
    "How do you feel compared with your usual self?":
        "ਆਪਣੀ ਆਮ ਹਾਲਤ ਦੇ ਮੁਕਾਬਲੇ ਤੁਹਾਨੂੰ ਕਿਹੋ ਜਿਹਾ ਲੱਗਦਾ ਹੈ?",
    "Your current state, today.": "ਤੁਹਾਡੀ ਅੱਜ ਦੀ ਮੌਜੂਦਾ ਹਾਲਤ।",
    "Sara": "ਸਾਰ",
    "How would you describe your overall vitality?":
        "ਆਪਣੀ ਸਮੁੱਚੀ ਤਾਕਤ ਨੂੰ ਤੁਸੀਂ ਕਿਵੇਂ ਬਿਆਨ ਕਰੋਗੇ?",
    "How strong and resilient you generally feel.":
        "ਤੁਸੀਂ ਆਮ ਤੌਰ ਤੇ ਕਿੰਨੇ ਤਾਕਤਵਰ ਅਤੇ ਸਹਿਣਸ਼ੀਲ ਮਹਿਸੂਸ ਕਰਦੇ ਹੋ।",
    "Samhanana": "ਸੰਹਨਨ",
    "How is your body build?": "ਤੁਹਾਡੇ ਸਰੀਰ ਦੀ ਬਣਤਰ ਕਿਹੋ ਜਿਹੀ ਹੈ?",
    "Muscle and frame, in your own view.": "ਮਾਸਪੇਸ਼ੀਆਂ ਅਤੇ ਢਾਂਚਾ, ਤੁਹਾਡੇ ਮੁਤਾਬਕ।",
    "Pramana": "ਪ੍ਰਮਾਣ",
    "How would you describe your height and weight together?":
        "ਆਪਣੇ ਕੱਦ ਅਤੇ ਭਾਰ ਨੂੰ ਇਕੱਠੇ ਦੇਖਦੇ ਹੋਏ ਤੁਸੀਂ ਕਿਵੇਂ ਬਿਆਨ ਕਰੋਗੇ?",
    "Roughly proportionate, or not.": "ਲਗਭਗ ਢੁਕਵਾਂ, ਜਾਂ ਨਹੀਂ।",
    "Satmya": "ਸਾਤਮਯ",
    "Which foods or conditions suit you well?":
        "ਕਿਹੜੇ ਖਾਣੇ ਜਾਂ ਹਾਲਤਾਂ ਤੁਹਾਨੂੰ ਚੰਗੀ ਤਰ੍ਹਾਂ ਰਾਸ ਆਉਂਦੇ ਹਨ?",
    "What you tolerate easily.": "ਜੋ ਤੁਸੀਂ ਸੌਖਿਆਂ ਸਹਿ ਸਕਦੇ ਹੋ।",
    "Sattva": "ਸੱਤਵ",
    "How do you usually handle stress?": "ਤਣਾਅ ਨੂੰ ਤੁਸੀਂ ਆਮ ਤੌਰ ਤੇ ਕਿਵੇਂ ਸੰਭਾਲਦੇ ਹੋ?",
    "Your mental steadiness.": "ਤੁਹਾਡੀ ਮਾਨਸਿਕ ਸਥਿਰਤਾ।",
    "Ahara Shakti": "ਆਹਾਰ ਸ਼ਕਤੀ",
    "How is your appetite and digestion?": "ਤੁਹਾਡੀ ਭੁੱਖ ਅਤੇ ਪਾਚਨ ਕਿਹੋ ਜਿਹਾ ਹੈ?",
    "How much you can eat and digest comfortably.":
        "ਤੁਸੀਂ ਸੌਖਿਆਂ ਕਿੰਨਾ ਖਾ ਅਤੇ ਪਚਾ ਸਕਦੇ ਹੋ।",
    "Vyayama Shakti": "ਵਿਆਯਾਮ ਸ਼ਕਤੀ",
    "How much physical exertion can you manage?": "ਤੁਸੀਂ ਕਿੰਨੀ ਸਰੀਰਕ ਮਿਹਨਤ ਕਰ ਸਕਦੇ ਹੋ?",
    "Before you need to rest.": "ਅਰਾਮ ਦੀ ਲੋੜ ਪੈਣ ਤੋਂ ਪਹਿਲਾਂ।",
    "Vaya": "ਵਯ",
    "Which life stage are you in?": "ਤੁਸੀਂ ਜ਼ਿੰਦਗੀ ਦੇ ਕਿਸ ਪੜਾਅ ਵਿੱਚ ਹੋ?",

    # --- AYUSH: Ashtasthana ----------------------------------------------
    "Eight-fold examination": "ਅਸ਼ਟਸਥਾਨ ਪਰੀਕਸ਼ਾ",
    "Ashtasthana Pariksha — your practitioner will confirm each of these.":
        "ਅਸ਼ਟਸਥਾਨ ਪਰੀਕਸ਼ਾ — ਇਨ੍ਹਾਂ ਵਿੱਚੋਂ ਹਰ ਇੱਕ ਦੀ ਤੁਹਾਡੇ ਵੈਦ ਪੁਸ਼ਟੀ ਕਰਨਗੇ।",
    "Only what you notice yourself.": "ਜੋ ਤੁਹਾਨੂੰ ਆਪ ਮਹਿਸੂਸ ਹੁੰਦਾ ਹੈ, ਸਿਰਫ਼ ਉਹੀ।",
    "Your own sense of it — a practitioner will check properly.":
        "ਇਸ ਬਾਰੇ ਤੁਹਾਡੀ ਆਪਣੀ ਸਮਝ — ਵੈਦ ਠੀਕ ਤਰ੍ਹਾਂ ਜਾਂਚਣਗੇ।",
    "Nadi": "ਨਾੜੀ",
    "How does your pulse or heartbeat usually feel?":
        "ਤੁਹਾਡੀ ਨਾੜੀ ਜਾਂ ਦਿਲ ਦੀ ਧੜਕਣ ਆਮ ਤੌਰ ਤੇ ਕਿਹੋ ਜਿਹੀ ਮਹਿਸੂਸ ਹੁੰਦੀ ਹੈ?",
    "Mutra": "ਮੂਤਰ",
    "How is your urine?": "ਤੁਹਾਡਾ ਪਿਸ਼ਾਬ ਕਿਹੋ ਜਿਹਾ ਹੈ?",
    "Colour, quantity and how often.": "ਰੰਗ, ਮਾਤਰਾ ਅਤੇ ਕਿੰਨੀ ਵਾਰ।",
    "Mala": "ਮਲ",
    "How are your bowel movements?": "ਤੁਹਾਡੀ ਟੱਟੀ ਕਿਹੋ ਜਿਹੀ ਆਉਂਦੀ ਹੈ?",
    "Regularity and consistency.": "ਨਿਯਮਿਤਤਾ ਅਤੇ ਗਾੜ੍ਹਾਪਣ।",
    "Jihva": "ਜਿਹਵਾ",
    "How does your tongue look and feel?": "ਤੁਹਾਡੀ ਜੀਭ ਕਿਹੋ ਜਿਹੀ ਦਿਖਦੀ ਅਤੇ ਲੱਗਦੀ ਹੈ?",
    "Coating, dryness or taste in the mouth.": "ਜੀਭ ਉੱਤੇ ਪਰਤ, ਖੁਸ਼ਕੀ ਜਾਂ ਮੂੰਹ ਦਾ ਸੁਆਦ।",
    "Shabda": "ਸ਼ਬਦ",
    "How is your voice at present?": "ਤੁਹਾਡੀ ਆਵਾਜ਼ ਹੁਣ ਕਿਹੋ ਜਿਹੀ ਹੈ?",
    "Strength and clarity when you speak.": "ਬੋਲਣ ਵੇਲੇ ਜ਼ੋਰ ਅਤੇ ਸਾਫ਼ਗੀ।",
    "Sparsha": "ਸਪਰਸ਼",
    "How does your skin feel to touch?": "ਤੁਹਾਡੀ ਚਮੜੀ ਛੂਹਣ ਉੱਤੇ ਕਿਹੋ ਜਿਹੀ ਲੱਗਦੀ ਹੈ?",
    "Temperature, dryness or sweating.": "ਤਾਪਮਾਨ, ਖੁਸ਼ਕੀ ਜਾਂ ਪਸੀਨਾ।",
    "Drik": "ਦ੍ਰਿਕ",
    "How are your eyes and vision?": "ਤੁਹਾਡੀਆਂ ਅੱਖਾਂ ਅਤੇ ਨਜ਼ਰ ਕਿਹੋ ਜਿਹੀ ਹੈ?",
    "Akriti": "ਆਕ੍ਰਿਤੀ",
    "How would you describe your overall appearance now?":
        "ਆਪਣੀ ਸਮੁੱਚੀ ਦਿੱਖ ਨੂੰ ਹੁਣ ਤੁਸੀਂ ਕਿਵੇਂ ਬਿਆਨ ਕਰੋਗੇ?",
    "How you look and feel compared with your usual self.":
        "ਆਪਣੀ ਆਮ ਹਾਲਤ ਦੇ ਮੁਕਾਬਲੇ ਤੁਸੀਂ ਕਿਹੋ ਜਿਹੇ ਦਿਖਦੇ ਅਤੇ ਮਹਿਸੂਸ ਕਰਦੇ ਹੋ।",

    # --- AYUSH: lifestyle -------------------------------------------------
    "Digestion, sleep and routine": "ਪਾਚਨ, ਨੀਂਦ ਅਤੇ ਦਿਨਚਰਿਆ",
    "Agni, Nidra, Ahara and Vihara — how you eat, sleep and live.":
        "ਅਗਨੀ, ਨਿਦ੍ਰਾ, ਆਹਾਰ ਅਤੇ ਵਿਹਾਰ — ਤੁਸੀਂ ਕਿਵੇਂ ਖਾਂਦੇ, ਸੌਂਦੇ ਅਤੇ ਜੀਉਂਦੇ ਹੋ।",
    "Agni": "ਅਗਨੀ",
    "How well do you digest your food?": "ਤੁਹਾਡਾ ਖਾਣਾ ਕਿੰਨਾ ਚੰਗਾ ਪਚਦਾ ਹੈ?",
    "Whether food feels heavy, or digests comfortably.":
        "ਖਾਣਾ ਭਾਰੀ ਲੱਗਦਾ ਹੈ, ਜਾਂ ਸੌਖਿਆਂ ਪਚਦਾ ਹੈ।",
    "Koshtha": "ਕੋਸ਼ਠ",
    "How does your gut normally behave?": "ਤੁਹਾਡਾ ਪੇਟ ਆਮ ਤੌਰ ਤੇ ਕਿਹੋ ਜਿਹਾ ਵਿਹਾਰ ਕਰਦਾ ਹੈ?",
    "Nidra": "ਨਿਦ੍ਰਾ",
    "How is your sleep?": "ਤੁਹਾਡੀ ਨੀਂਦ ਕਿਹੋ ਜਿਹੀ ਹੈ?",
    "Falling asleep, staying asleep, and feeling rested.":
        "ਨੀਂਦ ਆਉਣੀ, ਟਿਕਣੀ, ਅਤੇ ਅਰਾਮ ਮਿਲਿਆ ਮਹਿਸੂਸ ਹੋਣਾ।",
    "Manas": "ਮਨਸ",
    "How has your mind felt lately?": "ਹਾਲ ਵਿੱਚ ਤੁਹਾਡੇ ਮਨ ਨੂੰ ਕਿਹੋ ਜਿਹਾ ਲੱਗਿਆ ਹੈ?",
    "Only if you wish to say. This is recorded for your practitioner, not assessed here.":
        "ਤੁਸੀਂ ਦੱਸਣਾ ਚਾਹੋ ਤਾਂ ਹੀ। ਇਹ ਤੁਹਾਡੇ ਵੈਦ ਲਈ ਦਰਜ ਹੁੰਦਾ ਹੈ, ਇੱਥੇ ਇਸ ਦਾ ਮੁਲਾਂਕਣ ਨਹੀਂ ਹੁੰਦਾ।",
    "And your daily routine?": "ਅਤੇ ਤੁਹਾਡੀ ਦਿਨਚਰਿਆ?",
    "Which of these describe your diet?": "ਇਨ੍ਹਾਂ ਵਿੱਚੋਂ ਕਿਹੜਾ ਤੁਹਾਡੀ ਖ਼ੁਰਾਕ ਨੂੰ ਬਿਆਨ ਕਰਦਾ ਹੈ?",
    "Ayurveda assessment": "ਆਯੁਰਵੇਦ ਮੁਲਾਂਕਣ",
    "Your usual tendency, not just today.": "ਤੁਹਾਡੀ ਆਮ ਪ੍ਰਵਿਰਤੀ, ਸਿਰਫ਼ ਅੱਜ ਦੀ ਨਹੀਂ।",
    "These optional questions are used in Ayurvedic practice. They describe your "
    "constitution and routine — they are not a diagnosis, and you can skip any of them.":
        "ਇਹ ਮਰਜ਼ੀ ਦੇ ਸਵਾਲ ਆਯੁਰਵੈਦਿਕ ਇਲਾਜ ਵਿੱਚ ਵਰਤੇ ਜਾਂਦੇ ਹਨ। ਇਹ ਤੁਹਾਡੀ ਪ੍ਰਕ੍ਰਿਤੀ ਅਤੇ "
        "ਦਿਨਚਰਿਆ ਬਿਆਨ ਕਰਦੇ ਹਨ — ਇਹ ਨਿਦਾਨ ਨਹੀਂ ਹੈ, ਅਤੇ ਤੁਸੀਂ ਇਨ੍ਹਾਂ ਵਿੱਚੋਂ ਕੋਈ ਵੀ ਛੱਡ ਸਕਦੇ ਹੋ।",

    # --- Structured history section names --------------------------------
    "Chief complaint": "ਮੁੱਖ ਸ਼ਿਕਾਇਤ",
    "History of present illness": "ਮੌਜੂਦਾ ਬਿਮਾਰੀ ਦਾ ਇਤਿਹਾਸ",
    "Past medical history": "ਪਿਛਲਾ ਡਾਕਟਰੀ ਇਤਿਹਾਸ",
    "Past surgical history": "ਪਿਛਲਾ ਆਪਰੇਸ਼ਨ ਦਾ ਇਤਿਹਾਸ",
    "Medications": "ਦਵਾਈਆਂ",
    "Current medications": "ਮੌਜੂਦਾ ਦਵਾਈਆਂ",
    "Drug history": "ਦਵਾਈਆਂ ਦਾ ਇਤਿਹਾਸ",
    "Personal history": "ਨਿੱਜੀ ਇਤਿਹਾਸ",
    "Previous investigations": "ਪਿਛਲੀਆਂ ਜਾਂਚਾਂ",
    "Review of systems": "ਸਰੀਰ ਪ੍ਰਣਾਲੀਆਂ ਦੀ ਸਮੀਖਿਆ",
    "Additional information": "ਵਾਧੂ ਜਾਣਕਾਰੀ",
    "None reported": "ਕੁਝ ਨਹੀਂ ਦੱਸਿਆ",
    "Regarding this problem": "ਇਸ ਸਮੱਸਿਆ ਬਾਰੇ",
    "Also reports": "ਇਹ ਵੀ ਦੱਸਿਆ",

    # --- Narratives -------------------------------------------------------
    "The patient": "ਮਰੀਜ਼",
    "{age}-year-old": "{age} ਸਾਲ",
    "no specific complaint": "ਕੋਈ ਖ਼ਾਸ ਸ਼ਿਕਾਇਤ ਨਹੀਂ",
    "an unspecified concern": "ਅਸਪਸ਼ਟ ਸ਼ਿਕਾਇਤ",
    "{subject} reports: {complaint}.": "{subject} ਦੀ ਸ਼ਿਕਾਇਤ: {complaint}.",
    "{subject} presents reporting: {complaint}.": "{subject} ਦੀ ਸ਼ਿਕਾਇਤ: {complaint}.",
    "{subject} returns reporting: {complaint}.":
        "{subject} ਦੁਬਾਰਾ ਆਏ ਹਨ, ਸ਼ਿਕਾਇਤ: {complaint}.",
    "{lead}: {found}.": "{lead}: {found}.",
    "{lead}: none reported.": "{lead}: ਕੁਝ ਨਹੀਂ ਦੱਸਿਆ।",
    "About this problem today: {items}.": "ਅੱਜ ਇਸ ਸਮੱਸਿਆ ਬਾਰੇ: {items}.",
    "Severity reported by the patient: {value}.": "ਮਰੀਜ਼ ਵੱਲੋਂ ਦੱਸੀ ਤੀਬਰਤਾ: {value}.",
    "No further detail was given about the problem.":
        "ਸਮੱਸਿਆ ਬਾਰੇ ਇਸ ਤੋਂ ਵੱਧ ਵੇਰਵਾ ਨਹੀਂ ਦਿੱਤਾ ਗਿਆ।",
    "Also reported today: {items}.": "ਅੱਜ ਇਹ ਵੀ ਦੱਸਿਆ: {items}.",
    "Known conditions from earlier visits: {items}.":
        "ਪਿਛਲੀਆਂ ਮੁਲਾਕਾਤਾਂ ਤੋਂ ਜਾਣੀਆਂ ਬਿਮਾਰੀਆਂ: {items}.",
    "Medications on record: {items}.": "ਰਿਕਾਰਡ ਵਿੱਚ ਦਵਾਈਆਂ: {items}.",
    "Allergies on record: {items}.": "ਰਿਕਾਰਡ ਵਿੱਚ ਐਲਰਜੀ: {items}.",
    "No allergies recorded.": "ਕੋਈ ਐਲਰਜੀ ਦਰਜ ਨਹੀਂ ਹੈ।",
    "Medication changes reported today: {items}.": "ਅੱਜ ਦੱਸੇ ਦਵਾਈਆਂ ਦੇ ਬਦਲਾਅ: {items}.",
    "New conditions reported today: {items}.": "ਅੱਜ ਦੱਸੀਆਂ ਨਵੀਆਂ ਬਿਮਾਰੀਆਂ: {items}.",
    "This visit has been marked urgent because some described symptoms may require "
    "prompt attention.":
        "ਇਸ ਮੁਲਾਕਾਤ ਨੂੰ ਤੁਰੰਤ ਵਜੋਂ ਨਿਸ਼ਾਨਬੱਧ ਕੀਤਾ ਗਿਆ ਹੈ, ਕਿਉਂਕਿ ਦੱਸੇ ਗਏ ਕੁਝ ਲੱਛਣਾਂ ਵੱਲ "
        "ਛੇਤੀ ਧਿਆਨ ਦੇਣ ਦੀ ਲੋੜ ਹੋ ਸਕਦੀ ਹੈ।",
    "Recorded from the patient's own account and their existing records. "
    "This is not a diagnosis.":
        "ਮਰੀਜ਼ ਦੇ ਆਪਣੇ ਦੱਸੇ ਮੁਤਾਬਕ ਅਤੇ ਉਨ੍ਹਾਂ ਦੇ ਮੌਜੂਦਾ ਰਿਕਾਰਡ ਤੋਂ ਦਰਜ ਕੀਤਾ ਗਿਆ ਹੈ। "
        "ਇਹ ਨਿਦਾਨ ਨਹੀਂ ਹੈ।",
    "This is a record of information provided by the patient and read from their "
    "documents. It is not a diagnosis.":
        "ਇਹ ਮਰੀਜ਼ ਵੱਲੋਂ ਦਿੱਤੀ ਅਤੇ ਉਨ੍ਹਾਂ ਦੇ ਕਾਗਜ਼ਾਂ ਤੋਂ ਪੜ੍ਹੀ ਜਾਣਕਾਰੀ ਦਾ ਰਿਕਾਰਡ ਹੈ। "
        "ਇਹ ਨਿਦਾਨ ਨਹੀਂ ਹੈ।",
    "This records what you told us today alongside what we already knew. It is not a "
    "diagnosis, and a healthcare professional will review it with you.":
        "ਅੱਜ ਤੁਸੀਂ ਜੋ ਦੱਸਿਆ ਅਤੇ ਜੋ ਸਾਨੂੰ ਪਹਿਲਾਂ ਹੀ ਪਤਾ ਸੀ, ਇਨ੍ਹਾਂ ਦੋਵਾਂ ਦਾ ਇਹ ਰਿਕਾਰਡ ਹੈ। "
        "ਇਹ ਨਿਦਾਨ ਨਹੀਂ ਹੈ, ਅਤੇ ਇੱਕ ਸਿਹਤ ਪੇਸ਼ੇਵਰ ਤੁਹਾਡੇ ਨਾਲ ਇਸ ਨੂੰ ਦੇਖੇਗਾ।",

    # --- Gender and care-system labels used in prose ----------------------
    "male": "ਪੁਰਸ਼",
    "female": "ਔਰਤ",
    "other": "ਹੋਰ",
    "gender not stated": "ਲਿੰਗ ਨਹੀਂ ਦੱਸਿਆ",
    "not decided yet": "ਹਾਲੇ ਤੈਅ ਨਹੀਂ",

    # --- Demo patients ----------------------------------------------------
    "Rajesh Kumar · 52": "ਰਾਜੇਸ਼ ਕੁਮਾਰ · ੫੨",
    "Returning patient, comfortable with digital forms. Standard mode.":
        "ਪੁਰਾਣੇ ਮਰੀਜ਼, ਡਿਜੀਟਲ ਫ਼ਾਰਮ ਵਿੱਚ ਸਹਿਜ। ਮਿਆਰੀ ਤਰੀਕਾ।",
    "Kamla Devi · 71": "ਕਮਲਾ ਦੇਵੀ · ੭੧",
    "Prefers a simpler experience. Easy mode with audio guidance.":
        "ਸੌਖਾ ਤਰੀਕਾ ਪਸੰਦ ਕਰਦੇ ਹਨ। ਆਵਾਜ਼ ਸੇਧ ਨਾਲ ਸੌਖਾ ਤਰੀਕਾ।",
    "Anil Sharma · 45": "ਅਨਿਲ ਸ਼ਰਮਾ · ੪੫",
    "Low vision. Extra-large text and high contrast.":
        "ਘੱਟ ਨਜ਼ਰ। ਬਹੁਤ ਵੱਡੀ ਲਿਖਤ ਅਤੇ ਵਧੇਰੇ ਸਾਫ਼ ਰੰਗ-ਫ਼ਰਕ।",
    "Sunita Devi · 34": "ਸੁਨੀਤਾ ਦੇਵੀ · ੩੪",
    "First-time patient who stopped part-way through onboarding.":
        "ਪਹਿਲੀ ਵਾਰ ਆਏ ਮਰੀਜ਼, ਜਿਨ੍ਹਾਂ ਨੇ ਰਜਿਸਟਰੇਸ਼ਨ ਅੱਧ ਵਿਚਾਲੇ ਛੱਡ ਦਿੱਤੀ।",
    "e.g. three days, worse on walking": "ਜਿਵੇਂ ਤਿੰਨ ਦਿਨ, ਤੁਰਨ ਨਾਲ ਵੱਧ",
    "e.g. very tired, losing weight": "ਜਿਵੇਂ ਬਹੁਤ ਥਕਾਵਟ, ਭਾਰ ਘਟਣਾ",
}
