/**
 * Punjabi translations, keyed by the English source string.
 *
 * MACHINE-AUTHORED — pending review by a Punjabi speaker. Written in
 * Gurmukhi, as used in Indian Punjab. Add or correct an entry by editing this
 * file; nothing else needs to change. An explicit `pa` key in `STRINGS`
 * always overrides an entry here.
 *
 * Terminology matches the server overlay (`backend/app/shared/translations/
 * pa.py`): ਮਰੀਜ਼ (patient), ਬਿਮਾਰੀ (illness), ਦਵਾਈ (medicine),
 * ਮੁਲਾਕਾਤ (visit), ਸ਼ਿਕਾਇਤ (complaint), ਨਿਦਾਨ (diagnosis), ਸਹਿਮਤੀ (consent).
 */
export const PUNJABI: Record<string, string> = {
  "about": "ਲਗਭਗ",
  // --- Landing statistics --------------------------------------------------
  "minutes": "ਮਿੰਟ",
  "the average primary-care consultation in India":
    "ਭਾਰਤ ਵਿੱਚ ਮੁੱਢਲੀ ਸਿਹਤ ਸਲਾਹ ਦਾ ਔਸਤ ਸਮਾਂ",
  "Among the shortest measured anywhere. Almost all of it goes on collecting a history the clinic could already have had.":
    "ਦੁਨੀਆ ਵਿੱਚ ਮਿਣੇ ਗਏ ਸਭ ਤੋਂ ਛੋਟੇ ਸਮਿਆਂ ਵਿੱਚੋਂ ਇੱਕ। ਇਸ ਦਾ ਲਗਭਗ ਸਾਰਾ ਸਮਾਂ ਉਹ ਇਤਿਹਾਸ ਇਕੱਠਾ ਕਰਨ ਵਿੱਚ ਲੱਗ ਜਾਂਦਾ ਹੈ ਜੋ ਕਲੀਨਿਕ ਕੋਲ ਪਹਿਲਾਂ ਹੀ ਹੋ ਸਕਦਾ ਸੀ।",
  "million": "ਲੱਖ",
  "people in India live with diabetes": "ਭਾਰਤ ਵਿੱਚ ਸ਼ੂਗਰ ਵਾਲੇ ਲੋਕ",
  "A further 136 million are prediabetic — a group early detection actually changes.":
    "ਹੋਰ ੧੩.੬ ਕਰੋੜ ਲੋਕ ਪੂਰਵ-ਸ਼ੂਗਰ ਵਾਲੇ ਹਨ — ਜਿਨ੍ਹਾਂ ਲਈ ਛੇਤੀ ਪਛਾਣ ਅਸਲ ਵਿੱਚ ਫ਼ਰਕ ਪਾਉਂਦੀ ਹੈ।",
  "adults live with hypertension": "ਵੱਧ ਬਲੱਡ ਪ੍ਰੈਸ਼ਰ ਵਾਲੇ ਬਾਲਗ",
  "Only a small fraction have it under control, and many do not know they have it.":
    "ਬਹੁਤ ਥੋੜ੍ਹਿਆਂ ਦਾ ਹੀ ਇਹ ਕਾਬੂ ਵਿੱਚ ਹੈ, ਅਤੇ ਬਹੁਤਿਆਂ ਨੂੰ ਪਤਾ ਹੀ ਨਹੀਂ ਕਿ ਉਨ੍ਹਾਂ ਨੂੰ ਹੈ।",
  "%": "%",
  "of deaths in India are from NCDs":
    "ਭਾਰਤ ਵਿੱਚ ਹੋਣ ਵਾਲੀਆਂ ਮੌਤਾਂ ਗ਼ੈਰ-ਸੰਚਾਰੀ ਬਿਮਾਰੀਆਂ ਕਾਰਨ",
  "Non-communicable disease — the category where a timely history and follow-up matter most.":
    "ਗ਼ੈਰ-ਸੰਚਾਰੀ ਬਿਮਾਰੀ — ਜਿੱਥੇ ਸਮੇਂ ਸਿਰ ਮਿਲਿਆ ਇਤਿਹਾਸ ਅਤੇ ਅਗਲੀ ਜਾਂਚ ਸਭ ਤੋਂ ਵੱਧ ਮਾਇਨੇ ਰੱਖਦੇ ਹਨ।",
  "of health spending is out of pocket": "ਸਿਹਤ ਖ਼ਰਚ ਜੋ ਆਪਣੀ ਜੇਬ ਤੋਂ ਹੁੰਦਾ ਹੈ",
  "Which is why a repeated test or a lost prescription is not a small inconvenience.":
    "ਇਸੇ ਲਈ ਦੁਬਾਰਾ ਕਰਵਾਉਣੀ ਪੈਂਦੀ ਜਾਂਚ ਜਾਂ ਗੁਆਚੀ ਦਵਾਈ ਦੀ ਪਰਚੀ ਛੋਟੀ ਪਰੇਸ਼ਾਨੀ ਨਹੀਂ ਹੈ।",

  // --- App identity and common actions ---------------------------------
  "MediKiosk": "ਮੈਡੀਕਿਓਸਕ",
  "Share your health information before your visit":
    "ਆਪਣੀ ਮੁਲਾਕਾਤ ਤੋਂ ਪਹਿਲਾਂ ਆਪਣੀ ਸਿਹਤ ਜਾਣਕਾਰੀ ਸਾਂਝੀ ਕਰੋ",
  "Continue": "ਅੱਗੇ ਵਧੋ",
  "Back": "ਪਿੱਛੇ",
  "Cancel": "ਰੱਦ ਕਰੋ",
  "Save": "ਸੰਭਾਲੋ",
  "Saving…": "ਸੰਭਾਲਿਆ ਜਾ ਰਿਹਾ ਹੈ…",
  "Saved": "ਸੰਭਾਲ ਲਿਆ",
  "Try again": "ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ",
  "Loading…": "ਲੋਡ ਹੋ ਰਿਹਾ ਹੈ…",
  "Skip for now": "ਹੁਣ ਲਈ ਛੱਡੋ",
  "Yes": "ਹਾਂ",
  "No": "ਨਹੀਂ",
  "Optional": "ਮਰਜ਼ੀ ਦਾ",
  "Add": "ਜੋੜੋ",
  "Remove": "ਹਟਾਓ",
  "Change": "ਬਦਲੋ",
  "Done": "ਪੂਰਾ",
  "Close": "ਬੰਦ ਕਰੋ",
  "Sign out": "ਸਾਈਨ ਆਉਟ",
  "Not provided": "ਨਹੀਂ ਦਿੱਤਾ",
  "Finish": "ਖ਼ਤਮ ਕਰੋ",
  "Start": "ਸ਼ੁਰੂ ਕਰੋ",
  "Stop": "ਰੋਕੋ",
  "Preview": "ਪਹਿਲੀ ਝਲਕ",
  "Section": "ਭਾਗ",
  "Question": "ਸਵਾਲ",
  "of": "ਵਿੱਚੋਂ",
  "Part": "ਹਿੱਸਾ",
  "About": "ਬਾਰੇ",
  "Why": "ਕਿਉਂ",
  "years": "ਸਾਲ",
  "added": "ਜੋੜਿਆ",
  "Sent": "ਭੇਜ ਦਿੱਤਾ",
  "Language": "ਭਾਸ਼ਾ",
  "Languages": "ਭਾਸ਼ਾਵਾਂ",
  "Settings": "ਸੈਟਿੰਗ",
  "Records": "ਰਿਕਾਰਡ",
  "Visits": "ਮੁਲਾਕਾਤਾਂ",
  "Consent": "ਸਹਿਮਤੀ",
  "Gender": "ਲਿੰਗ",
  "Age": "ਉਮਰ",
  "View all": "ਸਾਰੇ ਦੇਖੋ",

  // --- Landing / welcome -----------------------------------------------
  "Tell us about your health before you see the doctor":
    "ਡਾਕਟਰ ਨੂੰ ਮਿਲਣ ਤੋਂ ਪਹਿਲਾਂ ਆਪਣੀ ਸਿਹਤ ਬਾਰੇ ਦੱਸੋ",
  "Answer a few simple questions here. Your doctor sees your history before you walk in, so your visit is about you — not about filling forms.":
    "ਇੱਥੇ ਕੁਝ ਸੌਖੇ ਸਵਾਲਾਂ ਦੇ ਜਵਾਬ ਦਿਓ। ਤੁਹਾਡੇ ਅੰਦਰ ਆਉਣ ਤੋਂ ਪਹਿਲਾਂ ਹੀ ਡਾਕਟਰ ਨੂੰ ਤੁਹਾਡਾ ਇਤਿਹਾਸ ਦਿਖਦਾ ਹੈ, ਇਸ ਲਈ ਤੁਹਾਡੀ ਮੁਲਾਕਾਤ ਤੁਹਾਡੇ ਬਾਰੇ ਹੁੰਦੀ ਹੈ — ਫ਼ਾਰਮ ਭਰਨ ਬਾਰੇ ਨਹੀਂ।",
  "I have used MediKiosk before": "ਮੈਂ ਪਹਿਲਾਂ ਮੈਡੀਕਿਓਸਕ ਵਰਤਿਆ ਹੈ",
  "Choose your language": "ਆਪਣੀ ਭਾਸ਼ਾ ਚੁਣੋ",
  "Make text bigger": "ਲਿਖਤ ਵੱਡੀ ਕਰੋ",
  "How it works": "ਇਹ ਕਿਵੇਂ ਕੰਮ ਕਰਦਾ ਹੈ",
  "Sign in with your mobile": "ਆਪਣੇ ਮੋਬਾਈਲ ਨਾਲ ਸਾਈਨ ਇਨ ਕਰੋ",
  "We send a one-time code. No password to remember.":
    "ਅਸੀਂ ਇੱਕ-ਵਾਰੀ ਕੋਡ ਭੇਜਦੇ ਹਾਂ। ਪਾਸਵਰਡ ਯਾਦ ਰੱਖਣ ਦੀ ਲੋੜ ਨਹੀਂ।",
  "Answer simple questions": "ਸੌਖੇ ਸਵਾਲਾਂ ਦੇ ਜਵਾਬ ਦਿਓ",
  "Speak or tap — whichever is easier for you.":
    "ਬੋਲੋ ਜਾਂ ਛੂਹੋ — ਜੋ ਤੁਹਾਨੂੰ ਸੌਖਾ ਲੱਗੇ।",
  "Your doctor is ready": "ਤੁਹਾਡੇ ਡਾਕਟਰ ਤਿਆਰ ਹਨ",
  "Your history is waiting for them, so nothing gets repeated.":
    "ਤੁਹਾਡਾ ਇਤਿਹਾਸ ਉਨ੍ਹਾਂ ਲਈ ਤਿਆਰ ਹੁੰਦਾ ਹੈ, ਇਸ ਲਈ ਕੁਝ ਵੀ ਦੁਬਾਰਾ ਨਹੀਂ ਦੱਸਣਾ ਪੈਂਦਾ।",
  "You choose what to share. You can withdraw your consent at any time.":
    "ਕੀ ਸਾਂਝਾ ਕਰਨਾ ਹੈ, ਇਹ ਤੁਸੀਂ ਤੈਅ ਕਰਦੇ ਹੋ। ਆਪਣੀ ਸਹਿਮਤੀ ਤੁਸੀਂ ਕਦੇ ਵੀ ਵਾਪਸ ਲੈ ਸਕਦੇ ਹੋ।",

  // --- Sign in ----------------------------------------------------------
  "Sign in": "ਸਾਈਨ ਇਨ",
  "Enter your mobile number and we will send a one-time code.":
    "ਆਪਣਾ ਮੋਬਾਈਲ ਨੰਬਰ ਪਾਓ ਅਤੇ ਅਸੀਂ ਇੱਕ-ਵਾਰੀ ਕੋਡ ਭੇਜਾਂਗੇ।",
  "Mobile number": "ਮੋਬਾਈਲ ਨੰਬਰ",
  "10-digit number, for example 98765 43210":
    "੧੦ ਅੰਕਾਂ ਦਾ ਨੰਬਰ, ਜਿਵੇਂ ੯੮੭੬੫ ੪੩੨੧੦",
  "Send code": "ਕੋਡ ਭੇਜੋ",
  "Sending…": "ਭੇਜਿਆ ਜਾ ਰਿਹਾ ਹੈ…",
  "One-time code": "ਇੱਕ-ਵਾਰੀ ਕੋਡ",
  "6 digits": "੬ ਅੰਕ",
  "Verify and continue": "ਪੁਸ਼ਟੀ ਕਰੋ ਅਤੇ ਅੱਗੇ ਵਧੋ",
  "Verifying…": "ਪੁਸ਼ਟੀ ਹੋ ਰਹੀ ਹੈ…",
  "Send a new code": "ਨਵਾਂ ਕੋਡ ਭੇਜੋ",
  "Use a different number": "ਵੱਖਰਾ ਨੰਬਰ ਵਰਤੋ",
  "Code sent to": "ਕੋਡ ਭੇਜਿਆ",
  "Prototype": "ਨਮੂਨਾ",
  "This demonstration does not send SMS. Use the code shown below.":
    "ਇਹ ਪ੍ਰਦਰਸ਼ਨ ਐਸਐਮਐਸ ਨਹੀਂ ਭੇਜਦਾ। ਹੇਠਾਂ ਦਿਖਾਇਆ ਕੋਡ ਵਰਤੋ।",
  "Or explore with a demo patient": "ਜਾਂ ਡੈਮੋ ਮਰੀਜ਼ ਨਾਲ ਦੇਖੋ",
  "Demo patient": "ਡੈਮੋ ਮਰੀਜ਼",
  "Fictional records for demonstration. No real patient data.":
    "ਪ੍ਰਦਰਸ਼ਨ ਲਈ ਕਲਪਿਤ ਰਿਕਾਰਡ। ਕਿਸੇ ਅਸਲ ਮਰੀਜ਼ ਦੀ ਜਾਣਕਾਰੀ ਨਹੀਂ।",
  "Demo patients are not loaded on this server yet.":
    "ਇਸ ਸਰਵਰ ਉੱਤੇ ਡੈਮੋ ਮਰੀਜ਼ ਹਾਲੇ ਲੋਡ ਨਹੀਂ ਕੀਤੇ ਗਏ।",
  "Log in": "ਲੌਗ ਇਨ",
  "Register": "ਰਜਿਸਟਰ ਕਰੋ",

  // --- ABHA / health ID -------------------------------------------------
  "Connect your health ID": "ਆਪਣਾ ਹੈਲਥ ਆਈਡੀ ਜੋੜੋ",
  "If you have an ABHA number, connecting it keeps your records together between visits.":
    "ਤੁਹਾਡੇ ਕੋਲ ਆਭਾ ਨੰਬਰ ਹੋਵੇ, ਤਾਂ ਉਸ ਨੂੰ ਜੋੜਨ ਨਾਲ ਤੁਹਾਡੇ ਰਿਕਾਰਡ ਮੁਲਾਕਾਤਾਂ ਵਿਚਕਾਰ ਇਕੱਠੇ ਰਹਿੰਦੇ ਹਨ।",
  "ABHA number or address": "ਆਭਾ ਨੰਬਰ ਜਾਂ ਪਤਾ",
  "14 digits, or an address like name@abdm": "੧੪ ਅੰਕ, ਜਾਂ name@abdm ਵਰਗਾ ਪਤਾ",
  "Connect": "ਜੋੜੋ",
  "Checking…": "ਜਾਂਚ ਹੋ ਰਹੀ ਹੈ…",
  "I do not have one": "ਮੇਰੇ ਕੋਲ ਨਹੀਂ ਹੈ",
  "Prototype: this checks the number's format locally. It is not connected to the national ABDM network.":
    "ਨਮੂਨਾ: ਇਹ ਨੰਬਰ ਦੀ ਬਣਤਰ ਸਥਾਨਕ ਤੌਰ ਤੇ ਜਾਂਚਦਾ ਹੈ। ਇਹ ਰਾਸ਼ਟਰੀ ABDM ਨੈੱਟਵਰਕ ਨਾਲ ਜੁੜਿਆ ਨਹੀਂ ਹੈ।",
  "Health ID connected": "ਹੈਲਥ ਆਈਡੀ ਜੁੜ ਗਿਆ",
  "Why connect it?": "ਇਹ ਕਿਉਂ ਜੋੜਨਾ?",
  "Your history follows you, so you never start from scratch at your next visit. You can also continue without it.":
    "ਤੁਹਾਡਾ ਇਤਿਹਾਸ ਤੁਹਾਡੇ ਨਾਲ ਰਹਿੰਦਾ ਹੈ, ਇਸ ਲਈ ਅਗਲੀ ਮੁਲਾਕਾਤ ਉੱਤੇ ਨਵੇਂ ਸਿਰੇ ਤੋਂ ਸ਼ੁਰੂ ਨਹੀਂ ਕਰਨਾ ਪੈਂਦਾ। ਤੁਸੀਂ ਇਸ ਤੋਂ ਬਿਨਾਂ ਵੀ ਅੱਗੇ ਵਧ ਸਕਦੇ ਹੋ।",
  "Health ID": "ਹੈਲਥ ਆਈਡੀ",

  // --- Personal details -------------------------------------------------
  "Your details": "ਤੁਹਾਡੀ ਜਾਣਕਾਰੀ",
  "This helps the hospital identify you correctly.":
    "ਇਸ ਨਾਲ ਹਸਪਤਾਲ ਤੁਹਾਨੂੰ ਸਹੀ ਪਛਾਣ ਸਕਦਾ ਹੈ।",
  "Full name": "ਪੂਰਾ ਨਾਂ",
  "As written on your ID": "ਤੁਹਾਡੇ ਪਛਾਣ-ਪੱਤਰ ਉੱਤੇ ਲਿਖੇ ਅਨੁਸਾਰ",
  "Date of birth": "ਜਨਮ ਤਾਰੀਖ਼",
  "We use this to work out your age": "ਇਸ ਤੋਂ ਅਸੀਂ ਤੁਹਾਡੀ ਉਮਰ ਕੱਢਦੇ ਹਾਂ",
  "Male": "ਪੁਰਸ਼",
  "Female": "ਔਰਤ",
  "Other": "ਹੋਰ",
  "Prefer not to say": "ਦੱਸਣਾ ਨਹੀਂ ਚਾਹੁੰਦਾ",
  "Preferred language": "ਪਸੰਦੀਦਾ ਭਾਸ਼ਾ",
  "Emergency contact": "ਸੰਕਟ ਸਮੇਂ ਸੰਪਰਕ",
  "Someone the hospital can call if needed.":
    "ਲੋੜ ਪੈਣ ਉੱਤੇ ਹਸਪਤਾਲ ਜਿਸ ਨੂੰ ਫ਼ੋਨ ਕਰ ਸਕੇ, ਉਹ ਵਿਅਕਤੀ।",
  "Their name": "ਉਨ੍ਹਾਂ ਦਾ ਨਾਂ",
  "Their mobile number": "ਉਨ੍ਹਾਂ ਦਾ ਮੋਬਾਈਲ ਨੰਬਰ",
  "Relationship to you": "ਤੁਹਾਡੇ ਨਾਲ ਰਿਸ਼ਤਾ",
  "For example: spouse, son, neighbour": "ਜਿਵੇਂ: ਜੀਵਨ-ਸਾਥੀ, ਪੁੱਤਰ, ਗੁਆਂਢੀ",

  // --- Accessibility assessment ----------------------------------------
  "Let us set this up for you": "ਤੁਹਾਡੇ ਲਈ ਇਹ ਸੈੱਟ ਕਰੀਏ",
  "A few quick questions so the screens suit you. There are no wrong answers, and you can change everything later.":
    "ਸਕਰੀਨਾਂ ਤੁਹਾਡੇ ਅਨੁਕੂਲ ਹੋਣ ਲਈ ਕੁਝ ਛੇਤੀ ਸਵਾਲ। ਕੋਈ ਜਵਾਬ ਗ਼ਲਤ ਨਹੀਂ, ਅਤੇ ਤੁਸੀਂ ਬਾਅਦ ਵਿੱਚ ਸਭ ਬਦਲ ਸਕਦੇ ਹੋ।",
  "Why we ask": "ਅਸੀਂ ਕਿਉਂ ਪੁੱਛਦੇ ਹਾਂ",
  "Your answers only change how this app looks and sounds. They are not medical questions and are never shared as a diagnosis.":
    "ਤੁਹਾਡੇ ਜਵਾਬ ਸਿਰਫ਼ ਇਹ ਬਦਲਦੇ ਹਨ ਕਿ ਇਹ ਐਪ ਕਿਹੋ ਜਿਹਾ ਦਿਖਦਾ ਅਤੇ ਸੁਣਦਾ ਹੈ। ਇਹ ਡਾਕਟਰੀ ਸਵਾਲ ਨਹੀਂ ਹਨ ਅਤੇ ਨਿਦਾਨ ਵਜੋਂ ਕਦੇ ਸਾਂਝੇ ਨਹੀਂ ਕੀਤੇ ਜਾਂਦੇ।",
  "Choose an option to continue": "ਅੱਗੇ ਵਧਣ ਲਈ ਇੱਕ ਵਿਕਲਪ ਚੁਣੋ",
  "We have set this up for you": "ਅਸੀਂ ਤੁਹਾਡੇ ਲਈ ਇਹ ਸੈੱਟ ਕਰ ਦਿੱਤਾ ਹੈ",
  "Based on your answers. Change anything you like — now or later.":
    "ਤੁਹਾਡੇ ਜਵਾਬਾਂ ਦੇ ਆਧਾਰ ਉੱਤੇ। ਜੋ ਚਾਹੋ ਬਦਲੋ — ਹੁਣ ਜਾਂ ਬਾਅਦ ਵਿੱਚ।",
  "This looks good": "ਇਹ ਠੀਕ ਲੱਗਦਾ ਹੈ",
  "Change these settings": "ਇਹ ਸੈਟਿੰਗ ਬਦਲੋ",
  "Applying…": "ਲਾਗੂ ਹੋ ਰਿਹਾ ਹੈ…",
  "Your experience": "ਤੁਹਾਡਾ ਅਨੁਭਵ",
  "Screen style": "ਸਕਰੀਨ ਦੀ ਸ਼ੈਲੀ",
  "Text size": "ਲਿਖਤ ਦਾ ਆਕਾਰ",
  "Colours": "ਰੰਗ",
  "Read questions aloud": "ਸਵਾਲ ਉੱਚੀ ਆਵਾਜ਼ ਵਿੱਚ ਪੜ੍ਹੋ",
  "We will speak each question. You can turn this off any time.":
    "ਅਸੀਂ ਹਰ ਸਵਾਲ ਬੋਲ ਕੇ ਦੱਸਾਂਗੇ। ਤੁਸੀਂ ਇਹ ਕਦੇ ਵੀ ਬੰਦ ਕਰ ਸਕਦੇ ਹੋ।",
  "How you answer": "ਤੁਸੀਂ ਜਵਾਬ ਕਿਵੇਂ ਦਿੰਦੇ ਹੋ",
  "This is how text will look on your screens.":
    "ਤੁਹਾਡੀਆਂ ਸਕਰੀਨਾਂ ਉੱਤੇ ਲਿਖਤ ਇਸ ਤਰ੍ਹਾਂ ਦਿਖੇਗੀ।",
  "You are never locked into a setting. Change it from your profile whenever you want.":
    "ਕੋਈ ਵੀ ਸੈਟਿੰਗ ਪੱਕੀ ਨਹੀਂ ਹੁੰਦੀ। ਜਦੋਂ ਚਾਹੋ ਆਪਣੀ ਪ੍ਰੋਫ਼ਾਈਲ ਤੋਂ ਬਦਲੋ।",
  "Retake the comfort check": "ਸਹੂਲਤ ਜਾਂਚ ਦੁਬਾਰਾ ਕਰੋ",
  "Optional. We will suggest settings again based on your answers.":
    "ਮਰਜ਼ੀ ਦਾ। ਤੁਹਾਡੇ ਜਵਾਬਾਂ ਤੋਂ ਅਸੀਂ ਦੁਬਾਰਾ ਸੈਟਿੰਗ ਸੁਝਾਵਾਂਗੇ।",
  "Change how MediKiosk looks and sounds. Your answers are not affected.":
    "ਮੈਡੀਕਿਓਸਕ ਕਿਹੋ ਜਿਹਾ ਦਿਖਦਾ ਅਤੇ ਸੁਣਦਾ ਹੈ, ਉਹ ਬਦਲੋ। ਤੁਹਾਡੇ ਜਵਾਬਾਂ ਉੱਤੇ ਅਸਰ ਨਹੀਂ ਪੈਂਦਾ।",
  "Settings saved": "ਸੈਟਿੰਗ ਸੰਭਾਲ ਲਈ",

  // --- Consent ----------------------------------------------------------
  "Your consent": "ਤੁਹਾਡੀ ਸਹਿਮਤੀ",
  "I agree": "ਮੈਂ ਸਹਿਮਤ ਹਾਂ",
  "I do not agree": "ਮੈਂ ਸਹਿਮਤ ਨਹੀਂ ਹਾਂ",
  "Needed to continue": "ਅੱਗੇ ਵਧਣ ਲਈ ਲੋੜੀਂਦਾ",
  "Your choice": "ਤੁਹਾਡੀ ਚੋਣ",
  "What we collect": "ਅਸੀਂ ਕੀ ਇਕੱਠਾ ਕਰਦੇ ਹਾਂ",
  "How it is used": "ਇਹ ਕਿਵੇਂ ਵਰਤਿਆ ਜਾਂਦਾ ਹੈ",
  "Without this we cannot collect your health information. You can still see your doctor as usual — you would just fill the form there instead.":
    "ਇਸ ਤੋਂ ਬਿਨਾਂ ਅਸੀਂ ਤੁਹਾਡੀ ਸਿਹਤ ਜਾਣਕਾਰੀ ਇਕੱਠੀ ਨਹੀਂ ਕਰ ਸਕਦੇ। ਤੁਸੀਂ ਆਮ ਵਾਂਗ ਡਾਕਟਰ ਨੂੰ ਮਿਲ ਸਕਦੇ ਹੋ — ਸਿਰਫ਼ ਫ਼ਾਰਮ ਉੱਥੇ ਭਰਨਾ ਪਵੇਗਾ।",
  "Listen to this": "ਇਹ ਸੁਣੋ",

  // --- Medical history form ---------------------------------------------
  "Your health history": "ਤੁਹਾਡਾ ਸਿਹਤ ਇਤਿਹਾਸ",
  "Tell us once. Next time you only describe what is new.":
    "ਇੱਕ ਵਾਰ ਦੱਸੋ। ਅਗਲੀ ਵਾਰ ਸਿਰਫ਼ ਨਵਾਂ ਕੀ ਹੈ ਉਹੀ ਦੱਸੋ।",
  "Type here and press Add": "ਇੱਥੇ ਲਿਖੋ ਅਤੇ ਜੋੜੋ ਦਬਾਓ",
  "Nothing to add": "ਜੋੜਨ ਵਾਲਾ ਕੁਝ ਨਹੀਂ",
  "Common answers": "ਆਮ ਜਵਾਬ",
  "Health history": "ਸਿਹਤ ਇਤਿਹਾਸ",

  // --- Documents ---------------------------------------------------------
  "Previous medical records": "ਪਿਛਲੇ ਡਾਕਟਰੀ ਰਿਕਾਰਡ",
  "Add a photo of a prescription, lab report or discharge summary. This is optional.":
    "ਦਵਾਈ ਦੀ ਪਰਚੀ, ਜਾਂਚ ਰਿਪੋਰਟ ਜਾਂ ਡਿਸਚਾਰਜ ਸਾਰ ਦੀ ਫ਼ੋਟੋ ਜੋੜੋ। ਇਹ ਮਰਜ਼ੀ ਦਾ ਹੈ।",
  "Choose a photo or PDF": "ਫ਼ੋਟੋ ਜਾਂ ਪੀਡੀਐਫ਼ ਚੁਣੋ",
  "Uploading…": "ਅਪਲੋਡ ਹੋ ਰਿਹਾ ਹੈ…",
  "What is this?": "ਇਹ ਕੀ ਹੈ?",
  "Short description": "ਛੋਟਾ ਵੇਰਵਾ",
  "For example: Dr Mehta, March 2026": "ਜਿਵੇਂ: ਡਾ. ਮਹਿਤਾ, ਮਾਰਚ ੨੦੨੬",
  "No records added": "ਕੋਈ ਰਿਕਾਰਡ ਨਹੀਂ ਜੋੜਿਆ",
  "You can add records now or later from your profile. Your doctor can see them either way.":
    "ਤੁਸੀਂ ਰਿਕਾਰਡ ਹੁਣ ਜਾਂ ਬਾਅਦ ਵਿੱਚ ਪ੍ਰੋਫ਼ਾਈਲ ਤੋਂ ਜੋੜ ਸਕਦੇ ਹੋ। ਦੋਵੇਂ ਤਰ੍ਹਾਂ ਤੁਹਾਡੇ ਡਾਕਟਰ ਉਹ ਦੇਖ ਸਕਦੇ ਹਨ।",
  "Your records are saved and shown to your doctor as you uploaded them.":
    "ਤੁਹਾਡੇ ਰਿਕਾਰਡ ਸੰਭਾਲੇ ਜਾਂਦੇ ਹਨ ਅਤੇ ਜਿਵੇਂ ਤੁਸੀਂ ਅਪਲੋਡ ਕੀਤੇ, ਉਸੇ ਤਰ੍ਹਾਂ ਡਾਕਟਰ ਨੂੰ ਦਿਖਾਏ ਜਾਂਦੇ ਹਨ।",
  "Prescription": "ਦਵਾਈ ਦੀ ਪਰਚੀ",
  "Lab report": "ਜਾਂਚ ਰਿਪੋਰਟ",
  "Discharge summary": "ਡਿਸਚਾਰਜ ਸਾਰ",
  "Something else": "ਕੁਝ ਹੋਰ",
  "Reading your document…": "ਤੁਹਾਡਾ ਕਾਗਜ਼ ਪੜ੍ਹਿਆ ਜਾ ਰਿਹਾ ਹੈ…",
  "Read this document": "ਇਹ ਕਾਗਜ਼ ਪੜ੍ਹੋ",
  "Try reading again": "ਦੁਬਾਰਾ ਪੜ੍ਹਨ ਦੀ ਕੋਸ਼ਿਸ਼ ਕਰੋ",
  "Information found in this document": "ਇਸ ਕਾਗਜ਼ ਵਿੱਚ ਮਿਲੀ ਜਾਣਕਾਰੀ",
  "This is what the document appears to say. It is not a diagnosis — please check it and tell us if anything looks wrong.":
    "ਕਾਗਜ਼ ਵਿੱਚ ਇਹ ਲਿਖਿਆ ਜਾਪਦਾ ਹੈ। ਇਹ ਨਿਦਾਨ ਨਹੀਂ ਹੈ — ਕਿਰਪਾ ਕਰਕੇ ਇਸ ਨੂੰ ਦੇਖੋ ਅਤੇ ਕੁਝ ਗ਼ਲਤ ਲੱਗੇ ਤਾਂ ਦੱਸੋ।",
  "That is correct": "ਉਹ ਸਹੀ ਹੈ",
  "That is not right": "ਉਹ ਸਹੀ ਨਹੀਂ ਹੈ",
  "Confirmed by you": "ਤੁਸੀਂ ਪੁਸ਼ਟੀ ਕੀਤੀ",
  "You marked this wrong": "ਤੁਸੀਂ ਇਸ ਨੂੰ ਗ਼ਲਤ ਨਿਸ਼ਾਨਬੱਧ ਕੀਤਾ",
  "Show the text we read": "ਅਸੀਂ ਪੜ੍ਹੀ ਲਿਖਤ ਦਿਖਾਓ",
  "We read the text but did not recognise any medical details. Your doctor can still read the document.":
    "ਅਸੀਂ ਲਿਖਤ ਪੜ੍ਹੀ ਪਰ ਕੋਈ ਡਾਕਟਰੀ ਵੇਰਵਾ ਨਹੀਂ ਪਛਾਣ ਸਕੇ। ਤੁਹਾਡੇ ਡਾਕਟਰ ਇਹ ਕਾਗਜ਼ ਪੜ੍ਹ ਸਕਦੇ ਹਨ।",
  "Within the printed range": "ਛਪੀ ਹੱਦ ਦੇ ਅੰਦਰ",
  "Below the printed range": "ਛਪੀ ਹੱਦ ਤੋਂ ਹੇਠਾਂ",
  "Above the printed range": "ਛਪੀ ਹੱਦ ਤੋਂ ਉੱਪਰ",
  "Could not be compared": "ਤੁਲਨਾ ਨਹੀਂ ਹੋ ਸਕੀ",
  "Values are compared only against the range printed on your report. A healthcare professional should review them.":
    "ਮੁੱਲਾਂ ਦੀ ਤੁਲਨਾ ਸਿਰਫ਼ ਤੁਹਾਡੀ ਰਿਪੋਰਟ ਉੱਤੇ ਛਪੀ ਹੱਦ ਨਾਲ ਕੀਤੀ ਜਾਂਦੀ ਹੈ। ਕਿਸੇ ਸਿਹਤ ਪੇਸ਼ੇਵਰ ਨੂੰ ਇਹ ਦੇਖਣੇ ਚਾਹੀਦੇ ਹਨ।",

  // --- Timeline ----------------------------------------------------------
  "Your medical timeline": "ਤੁਹਾਡੀ ਡਾਕਟਰੀ ਸਮਾਂ-ਰੇਖਾ",
  "Everything we know about, newest first.":
    "ਸਾਨੂੰ ਪਤਾ ਹੋਵੇ ਉਹ ਸਭ, ਨਵੇਂ ਪਹਿਲਾਂ।",
  "Nothing here yet": "ਇੱਥੇ ਹਾਲੇ ਕੁਝ ਨਹੀਂ",
  "Once you answer questions or add a record, it will appear here.":
    "ਤੁਸੀਂ ਸਵਾਲਾਂ ਦੇ ਜਵਾਬ ਦਿਓ ਜਾਂ ਰਿਕਾਰਡ ਜੋੜੋ, ਫਿਰ ਉਹ ਇੱਥੇ ਦਿਖੇਗਾ।",
  "Everything": "ਸਭ ਕੁਝ",
  "Needs your check": "ਤੁਹਾਡੀ ਜਾਂਚ ਦੀ ਲੋੜ",
  "No date on record": "ਰਿਕਾਰਡ ਵਿੱਚ ਤਾਰੀਖ਼ ਨਹੀਂ",

  // --- Review ------------------------------------------------------------
  "Check your information": "ਆਪਣੀ ਜਾਣਕਾਰੀ ਜਾਂਚੋ",
  "Please look through this before we finish. You can change anything.":
    "ਅਸੀਂ ਖ਼ਤਮ ਕਰਨ ਤੋਂ ਪਹਿਲਾਂ ਕਿਰਪਾ ਕਰਕੇ ਇਹ ਦੇਖੋ। ਤੁਸੀਂ ਕੁਝ ਵੀ ਬਦਲ ਸਕਦੇ ਹੋ।",
  "You told us": "ਤੁਸੀਂ ਦੱਸਿਆ",
  "From your documents": "ਤੁਹਾਡੇ ਕਾਗਜ਼ਾਂ ਤੋਂ",
  "Still missing": "ਹਾਲੇ ਬਾਕੀ",
  "These are usually useful for your doctor. You can add them now or later.":
    "ਇਹ ਆਮ ਤੌਰ ਤੇ ਤੁਹਾਡੇ ਡਾਕਟਰ ਲਈ ਲਾਭਦਾਇਕ ਹੁੰਦੇ ਹਨ। ਤੁਸੀਂ ਇਹ ਹੁਣ ਜਾਂ ਬਾਅਦ ਵਿੱਚ ਜੋੜ ਸਕਦੇ ਹੋ।",
  "Summary for your doctor": "ਤੁਹਾਡੇ ਡਾਕਟਰ ਲਈ ਸਾਰ",
  "This is correct — finish": "ਇਹ ਸਹੀ ਹੈ — ਖ਼ਤਮ ਕਰੋ",
  "Change this": "ਇਹ ਬਦਲੋ",
  "You said this": "ਤੁਸੀਂ ਇਹ ਕਿਹਾ",
  "Found in a document": "ਕਾਗਜ਼ ਵਿੱਚ ਮਿਲਿਆ",
  "Nothing recorded": "ਕੁਝ ਦਰਜ ਨਹੀਂ",

  // --- Profile / completion ---------------------------------------------
  "You are all set": "ਸਭ ਤਿਆਰ ਹੈ",
  "Your health profile is saved. Show this screen at the reception desk.":
    "ਤੁਹਾਡੀ ਸਿਹਤ ਪ੍ਰੋਫ਼ਾਈਲ ਸੰਭਾਲ ਲਈ ਗਈ। ਇਹ ਸਕਰੀਨ ਰਿਸੈਪਸ਼ਨ ਡੈਸਕ ਉੱਤੇ ਦਿਖਾਓ।",
  "View my profile": "ਮੇਰੀ ਪ੍ਰੋਫ਼ਾਈਲ ਦੇਖੋ",
  "Your health profile": "ਤੁਹਾਡੀ ਸਿਹਤ ਪ੍ਰੋਫ਼ਾਈਲ",
  "No visits recorded yet": "ਹਾਲੇ ਕੋਈ ਮੁਲਾਕਾਤ ਦਰਜ ਨਹੀਂ",
  "Finish setting up": "ਸੈੱਟ ਕਰਨਾ ਪੂਰਾ ਕਰੋ",
  "Your profile is not finished yet. Complete it so your doctor has your full history.":
    "ਤੁਹਾਡੀ ਪ੍ਰੋਫ਼ਾਈਲ ਹਾਲੇ ਪੂਰੀ ਨਹੀਂ ਹੋਈ। ਡਾਕਟਰ ਕੋਲ ਤੁਹਾਡਾ ਪੂਰਾ ਇਤਿਹਾਸ ਹੋਵੇ, ਇਸ ਲਈ ਇਹ ਪੂਰੀ ਕਰੋ।",
  "items recorded": "ਦਰਜ ਹੋਏ",
  "At your next visit you will only be asked what has changed.":
    "ਅਗਲੀ ਮੁਲਾਕਾਤ ਉੱਤੇ ਤੁਹਾਨੂੰ ਸਿਰਫ਼ ਇਹ ਪੁੱਛਿਆ ਜਾਵੇਗਾ ਕਿ ਕੀ ਬਦਲਿਆ ਹੈ।",

  // --- Voice --------------------------------------------------------------
  "Tap to speak": "ਬੋਲਣ ਲਈ ਛੂਹੋ",
  "Listening…": "ਸੁਣ ਰਿਹਾ ਹੈ…",
  "Working out what you said…": "ਤੁਸੀਂ ਕੀ ਕਿਹਾ, ਸਮਝਿਆ ਜਾ ਰਿਹਾ ਹੈ…",
  "We heard": "ਅਸੀਂ ਸੁਣਿਆ",
  "That is right": "ਉਹ ਸਹੀ ਹੈ",
  "Say it again": "ਦੁਬਾਰਾ ਕਹੋ",
  "Type instead": "ਇਸ ਦੀ ਥਾਂ ਲਿਖੋ",
  "Recording…": "ਰਿਕਾਰਡ ਹੋ ਰਿਹਾ ਹੈ…",
  "Voice input problem": "ਆਵਾਜ਼ ਇਨਪੁੱਟ ਵਿੱਚ ਦਿੱਕਤ",
  "This device has no voice for the selected language, so questions cannot be read aloud. All text stays on screen.":
    "ਇਸ ਯੰਤਰ ਵਿੱਚ ਚੁਣੀ ਭਾਸ਼ਾ ਲਈ ਆਵਾਜ਼ ਨਹੀਂ ਹੈ, ਇਸ ਲਈ ਸਵਾਲ ਉੱਚੀ ਆਵਾਜ਼ ਵਿੱਚ ਨਹੀਂ ਪੜ੍ਹੇ ਜਾ ਸਕਦੇ। ਸਾਰੀ ਲਿਖਤ ਸਕਰੀਨ ਉੱਤੇ ਰਹਿੰਦੀ ਹੈ।",
  "Voice input is not available in this browser, so please type or tap your answers.":
    "ਇਸ ਬ੍ਰਾਊਜ਼ਰ ਵਿੱਚ ਆਵਾਜ਼ ਇਨਪੁੱਟ ਉਪਲਬਧ ਨਹੀਂ, ਇਸ ਲਈ ਕਿਰਪਾ ਕਰਕੇ ਆਪਣੇ ਜਵਾਬ ਲਿਖੋ ਜਾਂ ਛੂਹ ਕੇ ਦਿਓ।",

  // --- Interview ----------------------------------------------------------
  "We will ask a few questions, one at a time. Speak or tap — whichever is easier.":
    "ਅਸੀਂ ਇੱਕ ਵਾਰੀ ਇੱਕ ਕਰਕੇ ਕੁਝ ਸਵਾਲ ਪੁੱਛਾਂਗੇ। ਬੋਲੋ ਜਾਂ ਛੂਹੋ — ਜੋ ਸੌਖਾ ਹੋਵੇ।",
  "Continue where you left off": "ਜਿੱਥੇ ਛੱਡਿਆ ਸੀ ਉੱਥੋਂ ਅੱਗੇ ਵਧੋ",
  "Follow-up question": "ਅਗਲਾ ਸਵਾਲ",
  "Smart assistance is unavailable right now, so we are using our standard questions. Nothing you have answered is lost.":
    "ਸਮਾਰਟ ਸਹਾਇਤਾ ਹੁਣ ਉਪਲਬਧ ਨਹੀਂ, ਇਸ ਲਈ ਅਸੀਂ ਆਪਣੇ ਆਮ ਸਵਾਲ ਵਰਤ ਰਹੇ ਹਾਂ। ਤੁਹਾਡਾ ਦਿੱਤਾ ਕੋਈ ਜਵਾਬ ਗੁਆਚਿਆ ਨਹੀਂ।",
  "That is everything we need": "ਸਾਨੂੰ ਲੋੜੀਂਦਾ ਸਭ ਹੋ ਗਿਆ",
  "Next you can add old medical records, or go straight to reviewing what you told us.":
    "ਹੁਣ ਤੁਸੀਂ ਪੁਰਾਣੇ ਡਾਕਟਰੀ ਰਿਕਾਰਡ ਜੋੜ ਸਕਦੇ ਹੋ, ਜਾਂ ਜੋ ਦੱਸਿਆ ਉਹ ਸਿੱਧਾ ਜਾਂਚ ਸਕਦੇ ਹੋ।",

  // --- AYUSH ---------------------------------------------------------------
  "Include Ayurveda questions": "ਆਯੁਰਵੇਦ ਦੇ ਸਵਾਲ ਸ਼ਾਮਲ ਕਰੋ",
  "Optional. Used at AYUSH facilities to record your constitution and routine.":
    "ਮਰਜ਼ੀ ਦਾ। ਆਯੁਸ਼ ਕੇਂਦਰਾਂ ਵਿੱਚ ਤੁਹਾਡੀ ਪ੍ਰਕ੍ਰਿਤੀ ਅਤੇ ਦਿਨਚਰਿਆ ਦਰਜ ਕਰਨ ਲਈ ਵਰਤਿਆ ਜਾਂਦਾ ਹੈ।",
  "Ayurveda assessment": "ਆਯੁਰਵੇਦ ਮੁਲਾਂਕਣ",
  "Skip these questions": "ਇਹ ਸਵਾਲ ਛੱਡੋ",
  "Include them": "ਇਹ ਸ਼ਾਮਲ ਕਰੋ",
  "Ten-fold examination": "ਦਸ਼ਵਿਧ ਪਰੀਕਸ਼ਾ",
  "Dashavidha Pariksha — your constitution and current state.":
    "ਦਸ਼ਵਿਧ ਪਰੀਕਸ਼ਾ — ਤੁਹਾਡੀ ਪ੍ਰਕ੍ਰਿਤੀ ਅਤੇ ਮੌਜੂਦਾ ਹਾਲਤ।",
  "Eight-fold examination": "ਅਸ਼ਟਸਥਾਨ ਪਰੀਕਸ਼ਾ",
  "Ashtasthana Pariksha. You describe what you notice; your practitioner examines and confirms each of these.":
    "ਅਸ਼ਟਸਥਾਨ ਪਰੀਕਸ਼ਾ। ਜੋ ਤੁਹਾਨੂੰ ਮਹਿਸੂਸ ਹੁੰਦਾ ਹੈ ਉਹ ਤੁਸੀਂ ਦੱਸਦੇ ਹੋ; ਤੁਹਾਡੇ ਵੈਦ ਜਾਂਚ ਕੇ ਇਨ੍ਹਾਂ ਵਿੱਚੋਂ ਹਰ ਇੱਕ ਦੀ ਪੁਸ਼ਟੀ ਕਰਦੇ ਹਨ।",
  "Digestion, sleep and routine": "ਪਾਚਨ, ਨੀਂਦ ਅਤੇ ਦਿਨਚਰਿਆ",
  "Agni, Koshtha, Nidra and Manas.": "ਅਗਨੀ, ਕੋਸ਼ਠ, ਨਿਦ੍ਰਾ ਅਤੇ ਮਨਸ।",
  "factors recorded": "ਕਾਰਕ ਦਰਜ",
  "Record your constitution, examination findings and routine for an Ayurvedic consultation.":
    "ਆਯੁਰਵੈਦਿਕ ਸਲਾਹ ਲਈ ਆਪਣੀ ਪ੍ਰਕ੍ਰਿਤੀ, ਜਾਂਚ ਦੇ ਨਤੀਜੇ ਅਤੇ ਦਿਨਚਰਿਆ ਦਰਜ ਕਰੋ।",
  "Open assessment": "ਮੁਲਾਂਕਣ ਖੋਲ੍ਹੋ",
  "These answers are recorded for your practitioner. Nothing here is assessed or interpreted by the app.":
    "ਇਹ ਜਵਾਬ ਤੁਹਾਡੇ ਵੈਦ ਲਈ ਦਰਜ ਹੁੰਦੇ ਹਨ। ਇਨ੍ਹਾਂ ਵਿੱਚੋਂ ਕੁਝ ਵੀ ਐਪ ਵੱਲੋਂ ਜਾਂਚਿਆ ਜਾਂ ਅਰਥ ਨਹੀਂ ਕੱਢਿਆ ਜਾਂਦਾ।",
  "Type of treatment": "ਇਲਾਜ ਦੀ ਕਿਸਮ",
  "Modern medicine": "ਆਧੁਨਿਕ ਇਲਾਜ",
  "Ayurveda": "ਆਯੁਰਵੇਦ",
  "We record which system you chose and ask about your diet and routine. Examination questions specific to this system are not built yet.":
    "ਤੁਸੀਂ ਕਿਹੜੀ ਪ੍ਰਣਾਲੀ ਚੁਣੀ ਉਹ ਅਸੀਂ ਦਰਜ ਕਰਦੇ ਹਾਂ ਅਤੇ ਤੁਹਾਡੀ ਖ਼ੁਰਾਕ ਤੇ ਦਿਨਚਰਿਆ ਬਾਰੇ ਪੁੱਛਦੇ ਹਾਂ। ਇਸ ਪ੍ਰਣਾਲੀ ਲਈ ਖ਼ਾਸ ਜਾਂਚ ਸਵਾਲ ਹਾਲੇ ਬਣਾਏ ਨਹੀਂ ਗਏ।",
  "Your diet (Ahara)": "ਤੁਹਾਡੀ ਖ਼ੁਰਾਕ",
  "Your routine (Vihara)": "ਤੁਹਾਡਾ ਵਿਹਾਰ",
  "Ayurvedic examination you answered": "ਤੁਹਾਡੀ ਦਿੱਤੀ ਆਯੁਰਵੈਦਿਕ ਪਰੀਕਸ਼ਾ",
  "{count} of {total} factors recorded": "{total} ਵਿੱਚੋਂ {count} ਕਾਰਕ ਦਰਜ",
  "Ayurveda details saved": "ਆਯੁਰਵੇਦ ਜਾਣਕਾਰੀ ਸੰਭਾਲ ਲਈ",

  // --- Landing page: problem, flow, features -----------------------------
  "Features": "ਵਿਸ਼ੇਸ਼ਤਾਵਾਂ",
  "For clinics": "ਕਲੀਨਿਕਾਂ ਲਈ",
  "Kiosk mode": "ਕਿਓਸਕ ਮੋਡ",
  "Your doctor should already know your history when you walk in":
    "ਤੁਹਾਡੇ ਅੰਦਰ ਆਉਣ ਵੇਲੇ ਤੁਹਾਡੇ ਡਾਕਟਰ ਨੂੰ ਤੁਹਾਡਾ ਇਤਿਹਾਸ ਪਹਿਲਾਂ ਹੀ ਪਤਾ ਹੋਣਾ ਚਾਹੀਦਾ ਹੈ",
  "MediKiosk collects a patient's medical history before the consultation — by voice, in their own language — so the few minutes with the doctor are spent on the problem, not on paperwork.":
    "ਮੈਡੀਕਿਓਸਕ ਸਲਾਹ ਤੋਂ ਪਹਿਲਾਂ ਹੀ ਮਰੀਜ਼ ਦਾ ਡਾਕਟਰੀ ਇਤਿਹਾਸ ਇਕੱਠਾ ਕਰਦਾ ਹੈ — ਆਵਾਜ਼ ਨਾਲ, ਉਨ੍ਹਾਂ ਦੀ ਆਪਣੀ ਭਾਸ਼ਾ ਵਿੱਚ — ਤਾਂ ਜੋ ਡਾਕਟਰ ਨਾਲ ਬਿਤਾਏ ਥੋੜ੍ਹੇ ਮਿੰਟ ਕਾਗਜ਼ੀ ਕੰਮ ਉੱਤੇ ਨਹੀਂ, ਸਗੋਂ ਸਮੱਸਿਆ ਉੱਤੇ ਲੱਗਣ।",
  "Try the patient flow": "ਮਰੀਜ਼ ਦਾ ਪ੍ਰਵਾਹ ਦੇਖੋ",
  "See a demo patient": "ਡੈਮੋ ਮਰੀਜ਼ ਦੇਖੋ",
  "The problem is time": "ਸਮੱਸਿਆ ਸਮੇਂ ਦੀ ਹੈ",
  "A patient repeats their history at every visit. The clinician spends most of a very short consultation writing it down. Both lose, and the record still ends up thin.":
    "ਮਰੀਜ਼ ਹਰ ਮੁਲਾਕਾਤ ਉੱਤੇ ਆਪਣਾ ਇਤਿਹਾਸ ਦੁਬਾਰਾ ਦੱਸਦਾ ਹੈ। ਡਾਕਟਰ ਬਹੁਤ ਥੋੜ੍ਹੀ ਸਲਾਹ ਦਾ ਵੱਡਾ ਹਿੱਸਾ ਉਹ ਲਿਖਣ ਵਿੱਚ ਲਾ ਦਿੰਦਾ ਹੈ। ਦੋਵਾਂ ਦਾ ਨੁਕਸਾਨ ਹੁੰਦਾ ਹੈ, ਅਤੇ ਰਿਕਾਰਡ ਫਿਰ ਵੀ ਅਧੂਰਾ ਰਹਿੰਦਾ ਹੈ।",
  "Why it matters here": "ਇਹ ਇੱਥੇ ਕਿਉਂ ਮਾਇਨੇ ਰੱਖਦਾ ਹੈ",
  "Figures are published estimates, shown with their source and year. Please re-check them against the latest release before citing.":
    "ਅੰਕੜੇ ਪ੍ਰਕਾਸ਼ਿਤ ਅਨੁਮਾਨ ਹਨ, ਸਰੋਤ ਅਤੇ ਸਾਲ ਸਮੇਤ ਦਿੱਤੇ। ਹਵਾਲਾ ਦੇਣ ਤੋਂ ਪਹਿਲਾਂ ਕਿਰਪਾ ਕਰਕੇ ਇਨ੍ਹਾਂ ਨੂੰ ਤਾਜ਼ਾ ਪ੍ਰਕਾਸ਼ਨ ਨਾਲ ਦੁਬਾਰਾ ਜਾਂਚੋ।",
  "Illustrative arithmetic": "ਸਮਝਾਉਣ ਲਈ ਹਿਸਾਬ",
  "In the": "ਇਸ",
  "you have spent on this page, a doctor working at India's average pace would have seen about":
    "ਸਮੇਂ ਵਿੱਚ ਜੋ ਤੁਸੀਂ ਇਸ ਪੰਨੇ ਉੱਤੇ ਲਾਇਆ, ਭਾਰਤ ਦੀ ਔਸਤ ਰਫ਼ਤਾਰ ਨਾਲ ਕੰਮ ਕਰਦੇ ਡਾਕਟਰ ਨੇ ਲਗਭਗ ਇੰਨੇ ਮਰੀਜ਼ ਦੇਖ ਲਏ ਹੁੰਦੇ",
  "patients.": "ਮਰੀਜ਼।",
  "Derived from the average consultation length, not a live measurement":
    "ਔਸਤ ਸਲਾਹ-ਸਮੇਂ ਤੋਂ ਕੱਢਿਆ, ਸਿੱਧੀ ਮਿਣਤੀ ਨਹੀਂ",
  "Before the visit": "ਮੁਲਾਕਾਤ ਤੋਂ ਪਹਿਲਾਂ",
  "The patient answers simple questions at a kiosk or on their phone — speaking or tapping, in English or an Indian language.":
    "ਮਰੀਜ਼ ਕਿਓਸਕ ਉੱਤੇ ਜਾਂ ਆਪਣੇ ਫ਼ੋਨ ਉੱਤੇ ਸੌਖੇ ਸਵਾਲਾਂ ਦੇ ਜਵਾਬ ਦਿੰਦਾ ਹੈ — ਬੋਲ ਕੇ ਜਾਂ ਛੂਹ ਕੇ, ਅੰਗਰੇਜ਼ੀ ਜਾਂ ਕਿਸੇ ਭਾਰਤੀ ਭਾਸ਼ਾ ਵਿੱਚ।",
  "Old records are read": "ਪੁਰਾਣੇ ਰਿਕਾਰਡ ਪੜ੍ਹੇ ਜਾਂਦੇ ਹਨ",
  "A photo of a prescription or lab report is scanned, and the medicines, diagnoses and test values found in it are listed for the patient to confirm.":
    "ਦਵਾਈ ਦੀ ਪਰਚੀ ਜਾਂ ਜਾਂਚ ਰਿਪੋਰਟ ਦੀ ਫ਼ੋਟੋ ਸਕੈਨ ਕੀਤੀ ਜਾਂਦੀ ਹੈ, ਅਤੇ ਉਸ ਵਿੱਚ ਮਿਲੀਆਂ ਦਵਾਈਆਂ, ਨਿਦਾਨ ਤੇ ਜਾਂਚ ਮੁੱਲ ਮਰੀਜ਼ ਦੀ ਪੁਸ਼ਟੀ ਲਈ ਦਿਖਾਏ ਜਾਂਦੇ ਹਨ।",
  "The clinician gets a history": "ਡਾਕਟਰ ਨੂੰ ਇਤਿਹਾਸ ਮਿਲਦਾ ਹੈ",
  "A structured summary, with each fact labelled as reported by the patient, read from a document, or already on record.":
    "ਇੱਕ ਵਿਵਸਥਿਤ ਸਾਰ, ਜਿਸ ਵਿੱਚ ਹਰ ਗੱਲ ਮਰੀਜ਼ ਨੇ ਦੱਸੀ, ਕਾਗਜ਼ ਤੋਂ ਪੜ੍ਹੀ, ਜਾਂ ਪਹਿਲਾਂ ਹੀ ਰਿਕਾਰਡ ਵਿੱਚ ਸੀ — ਇਹ ਸਾਫ਼ ਲਿਖਿਆ ਹੁੰਦਾ ਹੈ।",
  "The second visit is the point": "ਅਸਲ ਗੱਲ ਦੂਜੀ ਮੁਲਾਕਾਤ ਦੀ ਹੈ",
  "A returning patient does not repeat anything. They describe what is wrong today, and the questions adapt around what is already known.":
    "ਪੁਰਾਣਾ ਮਰੀਜ਼ ਕੁਝ ਵੀ ਦੁਬਾਰਾ ਨਹੀਂ ਦੱਸਦਾ। ਅੱਜ ਕੀ ਤਕਲੀਫ਼ ਹੈ ਉਹੀ ਦੱਸਦਾ ਹੈ, ਅਤੇ ਪਹਿਲਾਂ ਪਤਾ ਹੋਣ ਦੇ ਹਿਸਾਬ ਨਾਲ ਸਵਾਲ ਬਦਲ ਜਾਂਦੇ ਹਨ।",
  "What it does": "ਇਹ ਕੀ ਕਰਦਾ ਹੈ",
  "Voice, in your language": "ਆਵਾਜ਼, ਤੁਹਾਡੀ ਭਾਸ਼ਾ ਵਿੱਚ",
  "Speak your answers and correct the transcription before it is saved. Typing and tapping are always available — voice is never required.":
    "ਆਪਣੇ ਜਵਾਬ ਬੋਲੋ ਅਤੇ ਸੰਭਾਲੇ ਜਾਣ ਤੋਂ ਪਹਿਲਾਂ ਲਿਖਤ ਸੁਧਾਰੋ। ਲਿਖਣਾ ਅਤੇ ਛੂਹਣਾ ਹਮੇਸ਼ਾ ਉਪਲਬਧ ਹੈ — ਆਵਾਜ਼ ਕਦੇ ਜ਼ਰੂਰੀ ਨਹੀਂ।",
  "Built for every patient": "ਹਰ ਮਰੀਜ਼ ਲਈ ਬਣਾਇਆ",
  "A short comfort check suggests text size, contrast, audio and a simpler screen layout. Age alone never decides it, and the patient can override anything.":
    "ਇੱਕ ਛੋਟੀ ਸਹੂਲਤ ਜਾਂਚ ਲਿਖਤ ਦਾ ਆਕਾਰ, ਰੰਗ-ਫ਼ਰਕ, ਆਵਾਜ਼ ਅਤੇ ਸੌਖੀ ਸਕਰੀਨ ਬਣਤਰ ਸੁਝਾਉਂਦੀ ਹੈ। ਸਿਰਫ਼ ਉਮਰ ਤੋਂ ਇਹ ਕਦੇ ਤੈਅ ਨਹੀਂ ਹੁੰਦਾ, ਅਤੇ ਮਰੀਜ਼ ਕੁਝ ਵੀ ਬਦਲ ਸਕਦਾ ਹੈ।",
  "Reads old records": "ਪੁਰਾਣੇ ਰਿਕਾਰਡ ਪੜ੍ਹਦਾ ਹੈ",
  "Prescriptions and lab reports are scanned on the server. Lab values are compared only against the range printed on the report — never guessed.":
    "ਦਵਾਈ ਦੀਆਂ ਪਰਚੀਆਂ ਅਤੇ ਜਾਂਚ ਰਿਪੋਰਟਾਂ ਸਰਵਰ ਉੱਤੇ ਸਕੈਨ ਹੁੰਦੀਆਂ ਹਨ। ਜਾਂਚ ਮੁੱਲਾਂ ਦੀ ਤੁਲਨਾ ਸਿਰਫ਼ ਰਿਪੋਰਟ ਉੱਤੇ ਛਪੀ ਹੱਦ ਨਾਲ ਹੁੰਦੀ ਹੈ — ਅੰਦਾਜ਼ਾ ਕਦੇ ਨਹੀਂ ਲਾਇਆ ਜਾਂਦਾ।",
  "Flags what should not wait": "ਜੋ ਰੁਕ ਨਹੀਂ ਸਕਦਾ ਉਸ ਨੂੰ ਨਿਸ਼ਾਨਬੱਧ ਕਰਦਾ ਹੈ",
  "Answers are screened for presentations that need prompt attention. The patient is told to speak to staff, and the flag cannot be switched off from the kiosk.":
    "ਛੇਤੀ ਧਿਆਨ ਦੀ ਲੋੜ ਵਾਲੇ ਲੱਛਣਾਂ ਲਈ ਜਵਾਬ ਜਾਂਚੇ ਜਾਂਦੇ ਹਨ। ਮਰੀਜ਼ ਨੂੰ ਸਟਾਫ਼ ਨਾਲ ਗੱਲ ਕਰਨ ਲਈ ਕਿਹਾ ਜਾਂਦਾ ਹੈ, ਅਤੇ ਇਹ ਨਿਸ਼ਾਨ ਕਿਓਸਕ ਤੋਂ ਬੰਦ ਨਹੀਂ ਕੀਤਾ ਜਾ ਸਕਦਾ।",
  "Allopathy and AYUSH": "ਐਲੋਪੈਥੀ ਅਤੇ ਆਯੁਸ਼",
  "The patient chooses which system of medicine they are here for. An Ayurvedic visit adds the Dashavidha and Ashtasthana examination; an allopathic visit stays short.":
    "ਮਰੀਜ਼ ਚੁਣਦਾ ਹੈ ਕਿ ਉਹ ਕਿਸ ਇਲਾਜ ਪ੍ਰਣਾਲੀ ਲਈ ਆਇਆ ਹੈ। ਆਯੁਰਵੈਦਿਕ ਮੁਲਾਕਾਤ ਵਿੱਚ ਦਸ਼ਵਿਧ ਅਤੇ ਅਸ਼ਟਸਥਾਨ ਪਰੀਕਸ਼ਾ ਜੁੜ ਜਾਂਦੀ ਹੈ; ਐਲੋਪੈਥਿਕ ਮੁਲਾਕਾਤ ਛੋਟੀ ਰਹਿੰਦੀ ਹੈ।",
  "Consent, and nothing implied": "ਸਹਿਮਤੀ, ਅਤੇ ਮੰਨ ਲਿਆ ਕੁਝ ਨਹੀਂ",
  "Health information is collected only after the patient agrees, per purpose, and consent can be withdrawn. Health-ID linkage is prepared for ABDM but not connected.":
    "ਸਿਹਤ ਜਾਣਕਾਰੀ ਮਰੀਜ਼ ਦੀ ਰਜ਼ਾਮੰਦੀ ਤੋਂ ਬਾਅਦ ਹੀ, ਹਰ ਮਕਸਦ ਲਈ ਵੱਖਰੀ ਇਕੱਠੀ ਕੀਤੀ ਜਾਂਦੀ ਹੈ, ਅਤੇ ਸਹਿਮਤੀ ਵਾਪਸ ਲਈ ਜਾ ਸਕਦੀ ਹੈ। ਹੈਲਥ ਆਈਡੀ ਜੋੜ ABDM ਲਈ ਤਿਆਰ ਹੈ ਪਰ ਜੁੜਿਆ ਨਹੀਂ।",
  "What it does not do": "ਇਹ ਕੀ ਨਹੀਂ ਕਰਦਾ",
  "MediKiosk does not diagnose, does not prescribe, and does not replace a clinician. It organises what the patient tells us and what their documents say, and labels which is which.":
    "ਮੈਡੀਕਿਓਸਕ ਨਿਦਾਨ ਨਹੀਂ ਕਰਦਾ, ਦਵਾਈ ਨਹੀਂ ਲਿਖਦਾ, ਅਤੇ ਡਾਕਟਰ ਦੀ ਥਾਂ ਨਹੀਂ ਲੈਂਦਾ। ਮਰੀਜ਼ ਜੋ ਦੱਸਦਾ ਹੈ ਅਤੇ ਉਨ੍ਹਾਂ ਦੇ ਕਾਗਜ਼ਾਂ ਵਿੱਚ ਜੋ ਲਿਖਿਆ ਹੈ, ਉਸ ਨੂੰ ਵਿਵਸਥਿਤ ਕਰਦਾ ਹੈ, ਅਤੇ ਕਿਹੜਾ ਕਿਹੜਾ ਹੈ ਇਹ ਸਾਫ਼ ਕਰਦਾ ਹੈ।",
  "Specifications": "ਵੇਰਵੇ",
  "Stack": "ਤਕਨਾਲੋਜੀ",
  "React and TypeScript on the front, FastAPI and PostgreSQL behind, as a modular monolith. Alembic migrations, Docker images for both halves.":
    "ਅੱਗੇ React ਅਤੇ TypeScript, ਪਿੱਛੇ FastAPI ਅਤੇ PostgreSQL, ਇੱਕ ਮਾਡਿਊਲਰ ਮੋਨੋਲਿਥ ਵਜੋਂ। Alembic ਮਾਈਗ੍ਰੇਸ਼ਨ, ਦੋਵਾਂ ਹਿੱਸਿਆਂ ਲਈ Docker ਇਮੇਜ।",
  "Clinical data": "ਡਾਕਟਰੀ ਜਾਣਕਾਰੀ",
  "Every fact carries its source, confidence and whether a person has verified it. A new visit never overwrites the historical record.":
    "ਹਰ ਗੱਲ ਨਾਲ ਉਸ ਦਾ ਸਰੋਤ, ਭਰੋਸੇਯੋਗਤਾ ਅਤੇ ਕਿਸੇ ਵਿਅਕਤੀ ਨੇ ਉਸ ਦੀ ਪੁਸ਼ਟੀ ਕੀਤੀ ਹੈ ਜਾਂ ਨਹੀਂ, ਇਹ ਹੁੰਦਾ ਹੈ। ਨਵੀਂ ਮੁਲਾਕਾਤ ਪੁਰਾਣਾ ਰਿਕਾਰਡ ਕਦੇ ਮਿਟਾਉਂਦੀ ਨਹੀਂ।",
  "AI": "ਏਆਈ",
  "The interview is a deterministic state machine. A model may help read an answer or a document, but its output is schema-validated and every path works with AI switched off.":
    "ਇੰਟਰਵਿਊ ਇੱਕ ਪੱਕੀ ਹਾਲਤ-ਮਸ਼ੀਨ ਹੈ। ਜਵਾਬ ਜਾਂ ਕਾਗਜ਼ ਪੜ੍ਹਨ ਵਿੱਚ ਮਾਡਲ ਮਦਦ ਕਰ ਸਕਦਾ ਹੈ, ਪਰ ਉਸ ਦਾ ਨਤੀਜਾ ਸਕੀਮਾ ਅਨੁਸਾਰ ਜਾਂਚਿਆ ਜਾਂਦਾ ਹੈ ਅਤੇ ਏਆਈ ਬੰਦ ਹੋਣ ਉੱਤੇ ਵੀ ਹਰ ਰਾਹ ਕੰਮ ਕਰਦਾ ਹੈ।",
  "All six languages are complete: English, Hindi, Marathi, Tamil, Gujarati and Punjabi. The four regional translations are machine-authored and marked for review by a speaker of each; anything still untranslated falls back rather than breaking.":
    "ਸਾਰੀਆਂ ਛੇ ਭਾਸ਼ਾਵਾਂ ਪੂਰੀਆਂ ਹਨ: ਅੰਗਰੇਜ਼ੀ, ਹਿੰਦੀ, ਮਰਾਠੀ, ਤਮਿਲ, ਗੁਜਰਾਤੀ ਅਤੇ ਪੰਜਾਬੀ। ਚਾਰੇ ਖੇਤਰੀ ਅਨੁਵਾਦ ਮਸ਼ੀਨ ਨਾਲ ਕੀਤੇ ਗਏ ਹਨ ਅਤੇ ਉਨ੍ਹਾਂ ਭਾਸ਼ਾਵਾਂ ਦੇ ਬੋਲਣ ਵਾਲਿਆਂ ਦੀ ਜਾਂਚ ਲਈ ਨਿਸ਼ਾਨਬੱਧ ਹਨ; ਜੋ ਹਾਲੇ ਅਨੁਵਾਦ ਨਹੀਂ ਹੋਇਆ ਉਹ ਟੁੱਟਣ ਦੀ ਥਾਂ ਬਦਲਵੀਂ ਭਾਸ਼ਾ ਵਿੱਚ ਦਿਖਦਾ ਹੈ।",
  "Failure behaviour": "ਖ਼ਰਾਬੀ ਵੇਲੇ ਦਾ ਵਿਹਾਰ",
  "No workflow depends on one external service. If AI, voice, scanning or the health-ID service is unavailable, the patient keeps going and nothing already entered is lost.":
    "ਕੋਈ ਵੀ ਕੰਮ ਇੱਕੋ ਬਾਹਰੀ ਸੇਵਾ ਉੱਤੇ ਨਿਰਭਰ ਨਹੀਂ। ਏਆਈ, ਆਵਾਜ਼, ਸਕੈਨਿੰਗ ਜਾਂ ਹੈਲਥ ਆਈਡੀ ਸੇਵਾ ਉਪਲਬਧ ਨਾ ਹੋਵੇ, ਤਾਂ ਵੀ ਮਰੀਜ਼ ਅੱਗੇ ਵਧਦਾ ਰਹਿੰਦਾ ਹੈ ਅਤੇ ਪਹਿਲਾਂ ਭਰਿਆ ਕੁਝ ਗੁਆਚਦਾ ਨਹੀਂ।",
  "Accessibility": "ਸੁਲਭਤਾ",
  "Keyboard navigable, visible focus, semantic landmarks, large touch targets, and status never conveyed by colour alone.":
    "ਕੀਬੋਰਡ ਨਾਲ ਵਰਤਣਯੋਗ, ਦਿਖਦਾ ਫ਼ੋਕਸ, ਅਰਥਪੂਰਨ ਨਿਸ਼ਾਨ, ਵੱਡੇ ਛੋਹ-ਖੇਤਰ, ਅਤੇ ਹਾਲਤ ਸਿਰਫ਼ ਰੰਗ ਨਾਲ ਕਦੇ ਨਹੀਂ ਦੱਸੀ ਜਾਂਦੀ।",
  "Runs on a tablet at reception or on the patient's own phone. Records live in your PostgreSQL database, and the schema is shaped for the clinician view that comes next.":
    "ਰਿਸੈਪਸ਼ਨ ਦੇ ਟੈਬਲੇਟ ਉੱਤੇ ਜਾਂ ਮਰੀਜ਼ ਦੇ ਆਪਣੇ ਫ਼ੋਨ ਉੱਤੇ ਚੱਲਦਾ ਹੈ। ਰਿਕਾਰਡ ਤੁਹਾਡੇ PostgreSQL ਡੇਟਾਬੇਸ ਵਿੱਚ ਰਹਿੰਦੇ ਹਨ, ਅਤੇ ਸਕੀਮਾ ਅੱਗੇ ਆਉਣ ਵਾਲੇ ਡਾਕਟਰ-ਦ੍ਰਿਸ਼ ਲਈ ਘੜੀ ਗਈ ਹੈ।",
  "See it work": "ਇਹ ਚੱਲਦਾ ਦੇਖੋ",
  "Sign in with a mobile number, or open a demo patient with a full history already on file.":
    "ਮੋਬਾਈਲ ਨੰਬਰ ਨਾਲ ਸਾਈਨ ਇਨ ਕਰੋ, ਜਾਂ ਪੂਰਾ ਇਤਿਹਾਸ ਰੱਖਣ ਵਾਲਾ ਡੈਮੋ ਮਰੀਜ਼ ਖੋਲ੍ਹੋ।",
  "Prototype. All demo patients and medical records are fictional. Health-ID verification is simulated and not connected to ABDM.":
    "ਨਮੂਨਾ। ਸਾਰੇ ਡੈਮੋ ਮਰੀਜ਼ ਅਤੇ ਡਾਕਟਰੀ ਰਿਕਾਰਡ ਕਲਪਿਤ ਹਨ। ਹੈਲਥ ਆਈਡੀ ਪੁਸ਼ਟੀ ਬਣਾਵਟੀ ਹੈ ਅਤੇ ABDM ਨਾਲ ਜੁੜੀ ਨਹੀਂ।",

  // --- Returning-patient home ---------------------------------------------
  "Start a new health visit": "ਨਵੀਂ ਸਿਹਤ ਮੁਲਾਕਾਤ ਸ਼ੁਰੂ ਕਰੋ",
  "Tell us what is troubling you today. We already have your history.":
    "ਅੱਜ ਤੁਹਾਨੂੰ ਕੀ ਤਕਲੀਫ਼ ਹੈ ਇਹ ਦੱਸੋ। ਤੁਹਾਡਾ ਇਤਿਹਾਸ ਸਾਡੇ ਕੋਲ ਹੈ।",
  "Continue your visit": "ਆਪਣੀ ਮੁਲਾਕਾਤ ਜਾਰੀ ਰੱਖੋ",
  "Your health summary": "ਤੁਹਾਡਾ ਸਿਹਤ ਸਾਰ",
  "Ongoing conditions": "ਚੱਲ ਰਹੀਆਂ ਬਿਮਾਰੀਆਂ",
  "Your medicines": "ਤੁਹਾਡੀਆਂ ਦਵਾਈਆਂ",
  "Allergies": "ਐਲਰਜੀ",
  "Recent records": "ਹਾਲ ਦੇ ਰਿਕਾਰਡ",
  "Recent activity": "ਹਾਲ ਦੀ ਗਤੀਵਿਧੀ",
  "Last visit": "ਪਿਛਲੀ ਮੁਲਾਕਾਤ",
  "visits recorded": "ਮੁਲਾਕਾਤਾਂ ਦਰਜ",
  "Finish setting up your profile": "ਆਪਣੀ ਪ੍ਰੋਫ਼ਾਈਲ ਪੂਰੀ ਕਰੋ",
  "Nothing recorded yet": "ਹਾਲੇ ਕੁਝ ਦਰਜ ਨਹੀਂ",
  "You have not added any medical records yet":
    "ਤੁਸੀਂ ਹਾਲੇ ਕੋਈ ਡਾਕਟਰੀ ਰਿਕਾਰਡ ਨਹੀਂ ਜੋੜਿਆ",
  "A photo of a prescription or lab report helps your doctor see your history.":
    "ਦਵਾਈ ਦੀ ਪਰਚੀ ਜਾਂ ਜਾਂਚ ਰਿਪੋਰਟ ਦੀ ਫ਼ੋਟੋ ਤੁਹਾਡੇ ਡਾਕਟਰ ਨੂੰ ਤੁਹਾਡਾ ਇਤਿਹਾਸ ਦੇਖਣ ਵਿੱਚ ਮਦਦ ਕਰਦੀ ਹੈ।",
  "No allergies recorded": "ਕੋਈ ਐਲਰਜੀ ਦਰਜ ਨਹੀਂ",
  "Update my health history": "ਮੇਰਾ ਸਿਹਤ ਇਤਿਹਾਸ ਅੱਪਡੇਟ ਕਰੋ",

  // --- Encounter (today's visit) -------------------------------------------
  "What brings you here today?": "ਅੱਜ ਤੁਸੀਂ ਕਿਸ ਲਈ ਆਏ ਹੋ?",
  "Describe it in your own words — speak, type, or tap a common answer.":
    "ਆਪਣੇ ਸ਼ਬਦਾਂ ਵਿੱਚ ਦੱਸੋ — ਬੋਲੋ, ਲਿਖੋ, ਜਾਂ ਕਿਸੇ ਆਮ ਜਵਾਬ ਨੂੰ ਛੂਹੋ।",
  "We already know about": "ਸਾਨੂੰ ਪਹਿਲਾਂ ਹੀ ਪਤਾ ਹੈ",
  "You will not be asked about these again. You can update them from your profile.":
    "ਇਨ੍ਹਾਂ ਬਾਰੇ ਤੁਹਾਨੂੰ ਦੁਬਾਰਾ ਨਹੀਂ ਪੁੱਛਿਆ ਜਾਵੇਗਾ। ਤੁਸੀਂ ਇਹ ਆਪਣੀ ਪ੍ਰੋਫ਼ਾਈਲ ਤੋਂ ਅੱਪਡੇਟ ਕਰ ਸਕਦੇ ਹੋ।",
  "About today only": "ਸਿਰਫ਼ ਅੱਜ ਬਾਰੇ",
  "New today": "ਅੱਜ ਨਵਾਂ",
  "Already on record": "ਪਹਿਲਾਂ ਹੀ ਰਿਕਾਰਡ ਵਿੱਚ",
  "That is everything for today": "ਅੱਜ ਲਈ ਇੰਨਾ ਹੀ",
  "Please check what you told us before we send it to the care team.":
    "ਦੇਖਭਾਲ ਟੀਮ ਨੂੰ ਭੇਜਣ ਤੋਂ ਪਹਿਲਾਂ ਜੋ ਤੁਸੀਂ ਦੱਸਿਆ ਕਿਰਪਾ ਕਰਕੇ ਉਹ ਜਾਂਚੋ।",
  "Check and submit": "ਜਾਂਚੋ ਅਤੇ ਭੇਜੋ",
  "Marked urgent": "ਤੁਰੰਤ ਵਜੋਂ ਨਿਸ਼ਾਨਬੱਧ",
  "Marked urgent — please stay near the staff desk.":
    "ਤੁਰੰਤ ਵਜੋਂ ਨਿਸ਼ਾਨਬੱਧ — ਕਿਰਪਾ ਕਰਕੇ ਸਟਾਫ਼ ਡੈਸਕ ਦੇ ਨੇੜੇ ਰਹੋ।",
  "What you told us": "ਤੁਸੀਂ ਸਾਨੂੰ ਕੀ ਦੱਸਿਆ",
  "A member of staff will review this with you. This cannot be turned off from here.":
    "ਇੱਕ ਸਟਾਫ਼ ਮੈਂਬਰ ਇਹ ਤੁਹਾਡੇ ਨਾਲ ਦੇਖੇਗਾ। ਇਹ ਇੱਥੋਂ ਬੰਦ ਨਹੀਂ ਕੀਤਾ ਜਾ ਸਕਦਾ।",
  "Staff have been notified. Please stay where you are.":
    "ਸਟਾਫ਼ ਨੂੰ ਦੱਸ ਦਿੱਤਾ ਗਿਆ ਹੈ। ਕਿਰਪਾ ਕਰਕੇ ਜਿੱਥੇ ਹੋ ਉੱਥੇ ਹੀ ਰਹੋ।",
  "Check today's visit": "ਅੱਜ ਦੀ ਮੁਲਾਕਾਤ ਜਾਂਚੋ",
  "Please make sure this is right. You can change today's answers.":
    "ਕਿਰਪਾ ਕਰਕੇ ਇਹ ਸਹੀ ਹੋਣ ਦੀ ਪੁਸ਼ਟੀ ਕਰੋ। ਤੁਸੀਂ ਅੱਜ ਦੇ ਜਵਾਬ ਬਦਲ ਸਕਦੇ ਹੋ।",
  "Today's concern": "ਅੱਜ ਦੀ ਸ਼ਿਕਾਇਤ",
  "What you told us today": "ਅੱਜ ਤੁਸੀਂ ਕੀ ਦੱਸਿਆ",
  "questions you chose to skip": "ਤੁਹਾਡੇ ਛੱਡੇ ਹੋਏ ਸਵਾਲ",
  "How much it troubles you": "ਇਹ ਤੁਹਾਨੂੰ ਕਿੰਨੀ ਤਕਲੀਫ਼ ਦਿੰਦਾ ਹੈ",
  "out of 10": "੧੦ ਵਿੱਚੋਂ",
  "This rating is not what made your visit urgent — that came from the symptoms you described.":
    "ਇਸ ਅੰਕ ਨਾਲ ਤੁਹਾਡੀ ਮੁਲਾਕਾਤ ਤੁਰੰਤ ਨਹੀਂ ਬਣੀ — ਉਹ ਤੁਹਾਡੇ ਦੱਸੇ ਲੱਛਣਾਂ ਕਰਕੇ ਹੋਇਆ।",
  "Relevant existing history": "ਸੰਬੰਧਿਤ ਮੌਜੂਦਾ ਇਤਿਹਾਸ",
  "From your earlier visits. Editing this happens in your health history, not here.":
    "ਤੁਹਾਡੀਆਂ ਪਿਛਲੀਆਂ ਮੁਲਾਕਾਤਾਂ ਤੋਂ। ਇਸ ਵਿੱਚ ਤਬਦੀਲੀ ਤੁਹਾਡੇ ਸਿਹਤ ਇਤਿਹਾਸ ਵਿੱਚ ਹੁੰਦੀ ਹੈ, ਇੱਥੇ ਨਹੀਂ।",
  "Records added today": "ਅੱਜ ਜੋੜੇ ਰਿਕਾਰਡ",
  "Change today's answers": "ਅੱਜ ਦੇ ਜਵਾਬ ਬਦਲੋ",
  "Summary for the care team": "ਦੇਖਭਾਲ ਟੀਮ ਲਈ ਸਾਰ",
  "Still needed": "ਹਾਲੇ ਲੋੜੀਂਦਾ",
  "Before you send this": "ਇਹ ਭੇਜਣ ਤੋਂ ਪਹਿਲਾਂ",
  "My current symptoms were recorded correctly":
    "ਮੇਰੇ ਮੌਜੂਦਾ ਲੱਛਣ ਸਹੀ ਦਰਜ ਹੋਏ ਹਨ",
  "I have reviewed the information above": "ਮੈਂ ਉੱਪਰ ਦਿੱਤੀ ਜਾਣਕਾਰੀ ਦੇਖ ਲਈ ਹੈ",
  "I understand this will be used to support my healthcare visit":
    "ਇਹ ਮੇਰੀ ਸਿਹਤ ਮੁਲਾਕਾਤ ਵਿੱਚ ਮਦਦ ਲਈ ਵਰਤਿਆ ਜਾਵੇਗਾ, ਇਹ ਮੈਂ ਸਮਝਦਾ ਹਾਂ",
  "Send to the care team": "ਦੇਖਭਾਲ ਟੀਮ ਨੂੰ ਭੇਜੋ",
  "Your visit has been sent": "ਤੁਹਾਡੀ ਮੁਲਾਕਾਤ ਭੇਜ ਦਿੱਤੀ ਗਈ ਹੈ",
  "Back to home": "ਮੁੱਖ ਪੰਨੇ ਉੱਤੇ ਵਾਪਸ",
  "This visit has already been sent. Start a new visit if something has changed.":
    "ਇਹ ਮੁਲਾਕਾਤ ਪਹਿਲਾਂ ਹੀ ਭੇਜ ਦਿੱਤੀ ਗਈ ਹੈ। ਕੁਝ ਬਦਲਿਆ ਹੋਵੇ ਤਾਂ ਨਵੀਂ ਮੁਲਾਕਾਤ ਸ਼ੁਰੂ ਕਰੋ।",

  // --- Errors and chrome ---------------------------------------------------
  "Something went wrong. Please try again.":
    "ਕੁਝ ਗ਼ਲਤ ਹੋ ਗਿਆ। ਕਿਰਪਾ ਕਰਕੇ ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ।",
  "We could not reach the server. Check the connection and try again.":
    "ਅਸੀਂ ਸਰਵਰ ਤੱਕ ਨਹੀਂ ਪਹੁੰਚ ਸਕੇ। ਜੋੜ ਜਾਂਚੋ ਅਤੇ ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ।",
  "Your session has ended. Please sign in again.":
    "ਤੁਹਾਡਾ ਸੈਸ਼ਨ ਖ਼ਤਮ ਹੋ ਗਿਆ। ਕਿਰਪਾ ਕਰਕੇ ਦੁਬਾਰਾ ਸਾਈਨ ਇਨ ਕਰੋ।",
  "This is needed to continue": "ਅੱਗੇ ਵਧਣ ਲਈ ਇਹ ਲੋੜੀਂਦਾ ਹੈ",
  "Skip to main content": "ਮੁੱਖ ਸਮੱਗਰੀ ਉੱਤੇ ਜਾਓ",
  "Found in {name}": "{name} ਵਿੱਚ ਮਿਲਿਆ",
  "Your answers are saved as you go — you can stop and come back.":
    "ਤੁਹਾਡੇ ਜਵਾਬ ਨਾਲ-ਨਾਲ ਸੰਭਾਲੇ ਜਾਂਦੇ ਹਨ — ਤੁਸੀਂ ਰੁਕ ਕੇ ਵਾਪਸ ਆ ਸਕਦੇ ਹੋ।",

  // --- Enum labels -----------------------------------------------------------
  "Pending": "ਬਾਕੀ",
  "Processing": "ਪ੍ਰਕਿਰਿਆ ਵਿੱਚ",
  "Completed": "ਪੂਰਾ",
  "Could not be read": "ਪੜ੍ਹਿਆ ਨਹੀਂ ਜਾ ਸਕਿਆ",
  "Needs your review": "ਤੁਹਾਡੀ ਜਾਂਚ ਦੀ ਲੋੜ",
  "Not verified": "ਪੁਸ਼ਟੀ ਨਹੀਂ ਹੋਈ",
  "Verified": "ਪੁਸ਼ਟੀ ਹੋਈ",
  "Skipped": "ਛੱਡਿਆ",
  "Given": "ਦਿੱਤੀ",
  "Declined": "ਨਾਂਹ ਕੀਤੀ",
  "Withdrawn": "ਵਾਪਸ ਲਈ",
  "Collecting your health information": "ਤੁਹਾਡੀ ਸਿਹਤ ਸੰਬੰਧੀ ਜਾਣਕਾਰੀ ਇਕੱਠੀ ਕਰਨੀ",
  "Sharing with the doctor treating you":
    "ਤੁਹਾਡਾ ਇਲਾਜ ਕਰਨ ਵਾਲੇ ਡਾਕਟਰ ਨਾਲ ਸਾਂਝਾ ਕਰਨਾ",
  "Linking your ABHA number": "ਤੁਹਾਡਾ ਆਭਾ ਨੰਬਰ ਜੋੜਨਾ",
  "Standard": "ਮਿਆਰੀ",
  "Easy Mode": "ਸੌਖਾ ਮੋਡ",
  "Normal": "ਆਮ",
  "Large": "ਵੱਡਾ",
  "Extra large": "ਬਹੁਤ ਵੱਡਾ",
  "High": "ਉੱਚਾ",
  "Voice": "ਆਵਾਜ਼",
  "Touch": "ਛੋਹ",
  "Voice and touch": "ਆਵਾਜ਼ ਅਤੇ ਛੋਹ",
  "Typing": "ਲਿਖ ਕੇ",
  "Recommended for you": "ਤੁਹਾਡੇ ਲਈ ਸੁਝਾਇਆ",
  "Chosen by you": "ਤੁਹਾਡਾ ਚੁਣਿਆ",
  "Not started": "ਸ਼ੁਰੂ ਨਹੀਂ ਹੋਇਆ",
  "In progress": "ਚੱਲ ਰਿਹਾ ਹੈ",
  "Awaiting your review": "ਤੁਹਾਡੀ ਜਾਂਚ ਦੀ ਉਡੀਕ",
  "Cancelled": "ਰੱਦ",
  "Confirmed": "ਪੁਸ਼ਟੀ ਹੋਈ",
  "Routine": "ਆਮ",
  "Priority": "ਪਹਿਲ",
  "Urgent": "ਤੁਰੰਤ",
  "First visit": "ਪਹਿਲੀ ਮੁਲਾਕਾਤ",
  "Follow-up visit": "ਅਗਲੀ ਮੁਲਾਕਾਤ",
  "From a document": "ਕਾਗਜ਼ ਤੋਂ",
  "From an earlier visit": "ਪਿਛਲੀ ਮੁਲਾਕਾਤ ਤੋਂ",
  "From a clinician": "ਡਾਕਟਰ ਤੋਂ",
  "Condition": "ਹਾਲਤ",
  "Medicine": "ਦਵਾਈ",
  "Test": "ਜਾਂਚ",
  "Procedure": "ਪ੍ਰਕਿਰਿਆ",
  "Surgery": "ਆਪਰੇਸ਼ਨ",
  "Allergy": "ਐਲਰਜੀ",
  "Vital sign": "ਜੀਵਨ-ਚਿੰਨ੍ਹ",
  "Note": "ਟਿੱਪਣੀ",
  "Visit": "ਮੁਲਾਕਾਤ",
  "Low": "ਘੱਟ",
  "Unclear": "ਅਸਪਸ਼ਟ",
  "Not reviewed": "ਜਾਂਚਿਆ ਨਹੀਂ",
  "Kept": "ਰੱਖਿਆ",
  "Removed": "ਹਟਾਇਆ",
  "Allopathy": "ਐਲੋਪੈਥੀ",
  "Homoeopathy": "ਹੋਮਿਓਪੈਥੀ",
  "Unani": "ਯੂਨਾਨੀ",
  "Siddha": "ਸਿੱਧ",
  "Yoga and Naturopathy": "ਯੋਗ ਅਤੇ ਕੁਦਰਤੀ ਇਲਾਜ",
  "Not sure yet": "ਹਾਲੇ ਪੱਕਾ ਪਤਾ ਨਹੀਂ",
  "Document you uploaded": "ਤੁਹਾਡਾ ਅਪਲੋਡ ਕੀਤਾ ਕਾਗਜ਼",
  "Visit record": "ਮੁਲਾਕਾਤ ਦਾ ਰਿਕਾਰਡ",
  "Understood from what you said": "ਤੁਸੀਂ ਜੋ ਕਿਹਾ ਉਸ ਤੋਂ ਸਮਝਿਆ",
};
