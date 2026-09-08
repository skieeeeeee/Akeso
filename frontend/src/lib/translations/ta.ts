/**
 * Tamil translations, keyed by the English source string.
 *
 * MACHINE-AUTHORED — pending review by a Tamil speaker, and this file needs
 * that review more than the other three. Devanagari is not read in Tamil
 * Nadu, so an untranslated Tamil string falls back to English rather than to
 * Hindi: a gap here is visible immediately, and a clumsy translation has no
 * second language behind it to soften it.
 *
 * Add or correct an entry by editing this file; nothing else needs to change.
 * An explicit `ta` key in `STRINGS` always overrides an entry here.
 *
 * Terminology matches the server overlay (`backend/app/shared/translations/
 * ta.py`): நோயாளி (patient), நோய் (illness), மருந்து (medicine),
 * வருகை (visit), குறை (complaint), நோய் கண்டறிதல் (diagnosis),
 * ஒப்புதல் (consent).
 */
export const TAMIL: Record<string, string> = {
  "about": "ஏறத்தாழ",
  // --- Landing statistics --------------------------------------------------
  "minutes": "நிமிடங்கள்",
  "the average primary-care consultation in India":
    "இந்தியாவில் அடிப்படை மருத்துவ ஆலோசனையின் சராசரி நேரம்",
  "Among the shortest measured anywhere. Almost all of it goes on collecting a history the clinic could already have had.":
    "உலகில் அளக்கப்பட்டவற்றில் மிகக் குறைந்தவற்றில் ஒன்று. அதன் கிட்டத்தட்ட முழு நேரமும், மருத்துவமனையிடம் ஏற்கெனவே இருக்கக்கூடிய வரலாற்றைச் சேகரிப்பதிலேயே செல்கிறது.",
  "million": "மில்லியன்",
  "people in India live with diabetes": "இந்தியாவில் சர்க்கரை நோயுடன் வாழும் மக்கள்",
  "A further 136 million are prediabetic — a group early detection actually changes.":
    "மேலும் 136 மில்லியன் பேர் சர்க்கரை நோய்க்கு முந்தைய நிலையில் உள்ளனர் — முன்கூட்டிய கண்டறிதல் உண்மையில் மாற்றத்தை ஏற்படுத்தும் குழு.",
  "adults live with hypertension": "உயர் இரத்த அழுத்தத்துடன் வாழும் பெரியவர்கள்",
  "Only a small fraction have it under control, and many do not know they have it.":
    "மிகச் சிலருக்கே அது கட்டுப்பாட்டில் உள்ளது, பலருக்கு அது இருப்பதே தெரியாது.",
  "%": "%",
  "of deaths in India are from NCDs":
    "இந்தியாவில் ஏற்படும் இறப்புகள் தொற்றா நோய்களால்",
  "Non-communicable disease — the category where a timely history and follow-up matter most.":
    "தொற்றா நோய் — சரியான நேரத்தில் கிடைக்கும் வரலாறும் தொடர் கண்காணிப்பும் மிக முக்கியமான பிரிவு.",
  "of health spending is out of pocket": "சொந்தப் பணத்தில் இருந்து செல்லும் மருத்துவச் செலவு",
  "Which is why a repeated test or a lost prescription is not a small inconvenience.":
    "அதனால்தான் மீண்டும் செய்ய வேண்டிய பரிசோதனையோ தொலைந்த மருந்துச் சீட்டோ சிறிய சிரமம் அல்ல.",

  // --- App identity and common actions ---------------------------------
  "MediKiosk": "மெடிகியாஸ்க்",
  "Share your health information before your visit":
    "உங்கள் வருகைக்கு முன் உங்கள் உடல்நல தகவலைப் பங்கிடுங்கள்",
  "Continue": "தொடரவும்",
  "Back": "பின்",
  "Cancel": "ரத்து செய்",
  "Save": "சேமி",
  "Saving…": "சேமிக்கப்படுகிறது…",
  "Saved": "சேமிக்கப்பட்டது",
  "Try again": "மீண்டும் முயற்சிக்கவும்",
  "Loading…": "ஏற்றப்படுகிறது…",
  "Skip for now": "இப்போது தவிர்க்கவும்",
  "Yes": "ஆம்",
  "No": "இல்லை",
  "Optional": "விருப்பத்திற்குரியது",
  "Add": "சேர்",
  "Remove": "நீக்கு",
  "Change": "மாற்று",
  "Done": "முடிந்தது",
  "Close": "மூடு",
  "Sign out": "வெளியேறு",
  "Not provided": "தரப்படவில்லை",
  "Finish": "நிறைவு செய்",
  "Start": "தொடங்கு",
  "Stop": "நிறுத்து",
  "Preview": "முன்னோட்டம்",
  "Section": "பகுதி",
  "Question": "கேள்வி",
  "of": "இல்",
  "Part": "பாகம்",
  "About": "பற்றி",
  "Why": "ஏன்",
  "years": "வயது",
  "added": "சேர்க்கப்பட்டது",
  "Sent": "அனுப்பப்பட்டது",
  "Language": "மொழி",
  "Languages": "மொழிகள்",
  "Settings": "அமைப்புகள்",
  "Records": "பதிவுகள்",
  "Visits": "வருகைகள்",
  "Consent": "ஒப்புதல்",
  "Gender": "பாலினம்",
  "Age": "வயது",
  "View all": "அனைத்தையும் காண்க",

  // --- Landing / welcome -----------------------------------------------
  "Tell us about your health before you see the doctor":
    "மருத்துவரைப் பார்ப்பதற்கு முன் உங்கள் உடல்நலம் பற்றிச் சொல்லுங்கள்",
  "Answer a few simple questions here. Your doctor sees your history before you walk in, so your visit is about you — not about filling forms.":
    "இங்கே சில எளிய கேள்விகளுக்குப் பதிலளியுங்கள். நீங்கள் உள்ளே வருவதற்கு முன்பே மருத்துவருக்கு உங்கள் வரலாறு தெரியும், எனவே உங்கள் வருகை உங்களைப் பற்றியதாக இருக்கும் — படிவம் நிரப்புவது பற்றியதாக அல்ல.",
  "I have used MediKiosk before": "நான் முன்பே மெடிகியாஸ்க் பயன்படுத்தியுள்ளேன்",
  "Choose your language": "உங்கள் மொழியைத் தேர்ந்தெடுங்கள்",
  "Make text bigger": "எழுத்தைப் பெரிதாக்கு",
  "How it works": "இது எப்படி வேலை செய்கிறது",
  "Sign in with your mobile": "உங்கள் கைபேசி மூலம் உள்நுழையுங்கள்",
  "We send a one-time code. No password to remember.":
    "நாங்கள் ஒரு முறை மட்டும் பயன்படும் குறியீட்டை அனுப்புகிறோம். கடவுச்சொல் நினைவில் வைக்க வேண்டாம்.",
  "Answer simple questions": "எளிய கேள்விகளுக்குப் பதிலளியுங்கள்",
  "Speak or tap — whichever is easier for you.":
    "பேசுங்கள் அல்லது தொடுங்கள் — உங்களுக்கு எது எளிதோ.",
  "Your doctor is ready": "உங்கள் மருத்துவர் தயார்",
  "Your history is waiting for them, so nothing gets repeated.":
    "உங்கள் வரலாறு அவர்களுக்குத் தயாராக இருக்கும், எனவே எதையும் மீண்டும் சொல்ல வேண்டியதில்லை.",
  "You choose what to share. You can withdraw your consent at any time.":
    "எதைப் பங்கிடுவது என்பதை நீங்களே தீர்மானிக்கிறீர்கள். உங்கள் ஒப்புதலை எப்போது வேண்டுமானாலும் திரும்பப் பெறலாம்.",

  // --- Sign in ----------------------------------------------------------
  "Sign in": "உள்நுழைவு",
  "Enter your mobile number and we will send a one-time code.":
    "உங்கள் கைபேசி எண்ணை உள்ளிடுங்கள், நாங்கள் ஒரு முறை பயன்படும் குறியீட்டை அனுப்புவோம்.",
  "Mobile number": "கைபேசி எண்",
  "10-digit number, for example 98765 43210":
    "10 இலக்க எண், எடுத்துக்காட்டாக 98765 43210",
  "Send code": "குறியீட்டை அனுப்பு",
  "Sending…": "அனுப்பப்படுகிறது…",
  "One-time code": "ஒரு முறை குறியீடு",
  "6 digits": "6 இலக்கங்கள்",
  "Verify and continue": "சரிபார்த்துத் தொடரவும்",
  "Verifying…": "சரிபார்க்கப்படுகிறது…",
  "Send a new code": "புதிய குறியீட்டை அனுப்பு",
  "Use a different number": "வேறு எண்ணைப் பயன்படுத்து",
  "Code sent to": "குறியீடு அனுப்பப்பட்டது",
  "Prototype": "முன்மாதிரி",
  "This demonstration does not send SMS. Use the code shown below.":
    "இந்த விளக்கக்காட்சி எஸ்எம்எஸ் அனுப்புவதில்லை. கீழே காட்டப்பட்ட குறியீட்டைப் பயன்படுத்துங்கள்.",
  "Or explore with a demo patient": "அல்லது மாதிரி நோயாளியுடன் பாருங்கள்",
  "Demo patient": "மாதிரி நோயாளி",
  "Fictional records for demonstration. No real patient data.":
    "விளக்கத்திற்கான கற்பனைப் பதிவுகள். உண்மையான நோயாளியின் தகவல் இல்லை.",
  "Demo patients are not loaded on this server yet.":
    "இந்த சேவையகத்தில் மாதிரி நோயாளிகள் இன்னும் ஏற்றப்படவில்லை.",
  "Log in": "உள்நுழைவு",
  "Register": "பதிவு செய்",

  // --- ABHA / health ID -------------------------------------------------
  "Connect your health ID": "உங்கள் உடல்நல அடையாள எண்ணை இணையுங்கள்",
  "If you have an ABHA number, connecting it keeps your records together between visits.":
    "உங்களுக்கு ஆபா எண் இருந்தால், அதை இணைப்பது உங்கள் பதிவுகளை வருகைகளுக்கு இடையே ஒன்றாக வைத்திருக்கும்.",
  "ABHA number or address": "ஆபா எண் அல்லது முகவரி",
  "14 digits, or an address like name@abdm": "14 இலக்கங்கள், அல்லது name@abdm போன்ற முகவரி",
  "Connect": "இணை",
  "Checking…": "சரிபார்க்கப்படுகிறது…",
  "I do not have one": "என்னிடம் இல்லை",
  "Prototype: this checks the number's format locally. It is not connected to the national ABDM network.":
    "முன்மாதிரி: இது எண்ணின் வடிவத்தை இங்கேயே சரிபார்க்கிறது. இது தேசிய ABDM வலையமைப்புடன் இணைக்கப்படவில்லை.",
  "Health ID connected": "உடல்நல அடையாள எண் இணைக்கப்பட்டது",
  "Why connect it?": "இதை ஏன் இணைக்க வேண்டும்?",
  "Your history follows you, so you never start from scratch at your next visit. You can also continue without it.":
    "உங்கள் வரலாறு உங்களுடன் வரும், எனவே அடுத்த வருகையில் புதிதாகத் தொடங்க வேண்டியதில்லை. இது இல்லாமலும் தொடரலாம்.",
  "Health ID": "உடல்நல அடையாள எண்",

  // --- Personal details -------------------------------------------------
  "Your details": "உங்கள் விவரங்கள்",
  "This helps the hospital identify you correctly.":
    "இது மருத்துவமனை உங்களைச் சரியாக அறியத் உதவுகிறது.",
  "Full name": "முழுப் பெயர்",
  "As written on your ID": "உங்கள் அடையாள அட்டையில் உள்ளது போல",
  "Date of birth": "பிறந்த தேதி",
  "We use this to work out your age": "இதன் மூலம் உங்கள் வயதைக் கணக்கிடுகிறோம்",
  "Male": "ஆண்",
  "Female": "பெண்",
  "Other": "மற்றவை",
  "Prefer not to say": "சொல்ல விரும்பவில்லை",
  "Preferred language": "விருப்ப மொழி",
  "Emergency contact": "அவசர தொடர்பு",
  "Someone the hospital can call if needed.":
    "தேவைப்பட்டால் மருத்துவமனை அழைக்கக்கூடிய ஒருவர்.",
  "Their name": "அவரது பெயர்",
  "Their mobile number": "அவரது கைபேசி எண்",
  "Relationship to you": "உங்களுடன் உறவு",
  "For example: spouse, son, neighbour": "எடுத்துக்காட்டாக: கணவர்/மனைவி, மகன், அருகில் இருப்பவர்",

  // --- Accessibility assessment ----------------------------------------
  "Let us set this up for you": "உங்களுக்காக இதை அமைப்போம்",
  "A few quick questions so the screens suit you. There are no wrong answers, and you can change everything later.":
    "திரைகள் உங்களுக்குப் பொருந்த சில விரைவான கேள்விகள். எந்தப் பதிலும் தவறு அல்ல, பிறகு அனைத்தையும் மாற்றிக்கொள்ளலாம்.",
  "Why we ask": "நாங்கள் ஏன் கேட்கிறோம்",
  "Your answers only change how this app looks and sounds. They are not medical questions and are never shared as a diagnosis.":
    "உங்கள் பதில்கள் இந்தச் செயலி எப்படித் தெரிகிறது, எப்படி ஒலிக்கிறது என்பதை மட்டுமே மாற்றுகின்றன. இவை மருத்துவக் கேள்விகள் அல்ல, நோய் கண்டறிதலாக ஒருபோதும் பங்கிடப்படுவதில்லை.",
  "Choose an option to continue": "தொடர ஒரு விருப்பத்தைத் தேர்ந்தெடுங்கள்",
  "We have set this up for you": "உங்களுக்காக இதை அமைத்துவிட்டோம்",
  "Based on your answers. Change anything you like — now or later.":
    "உங்கள் பதில்களின் அடிப்படையில். விரும்பியதை மாற்றுங்கள் — இப்போது அல்லது பிறகு.",
  "This looks good": "இது சரியாக உள்ளது",
  "Change these settings": "இந்த அமைப்புகளை மாற்று",
  "Applying…": "பயன்படுத்தப்படுகிறது…",
  "Your experience": "உங்கள் அனுபவம்",
  "Screen style": "திரையின் பாணி",
  "Text size": "எழுத்தின் அளவு",
  "Colours": "நிறங்கள்",
  "Read questions aloud": "கேள்விகளைச் சத்தமாக வாசி",
  "We will speak each question. You can turn this off any time.":
    "ஒவ்வொரு கேள்வியையும் பேசிச் சொல்வோம். இதை எப்போது வேண்டுமானாலும் நிறுத்தலாம்.",
  "How you answer": "நீங்கள் எப்படிப் பதிலளிக்கிறீர்கள்",
  "This is how text will look on your screens.":
    "உங்கள் திரைகளில் எழுத்து இப்படித் தெரியும்.",
  "You are never locked into a setting. Change it from your profile whenever you want.":
    "எந்த அமைப்பும் நிரந்தரம் அல்ல. வேண்டும்போது உங்கள் சுயவிவரத்தில் இருந்து மாற்றுங்கள்.",
  "Retake the comfort check": "வசதி சோதனையை மீண்டும் செய்",
  "Optional. We will suggest settings again based on your answers.":
    "விருப்பத்திற்குரியது. உங்கள் பதில்களின் அடிப்படையில் மீண்டும் அமைப்புகளைப் பரிந்துரைப்போம்.",
  "Change how MediKiosk looks and sounds. Your answers are not affected.":
    "மெடிகியாஸ்க் எப்படித் தெரிகிறது, எப்படி ஒலிக்கிறது என்பதை மாற்றுங்கள். உங்கள் பதில்கள் பாதிக்கப்படுவதில்லை.",
  "Settings saved": "அமைப்புகள் சேமிக்கப்பட்டன",

  // --- Consent ----------------------------------------------------------
  "Your consent": "உங்கள் ஒப்புதல்",
  "I agree": "நான் ஒப்புக்கொள்கிறேன்",
  "I do not agree": "நான் ஒப்புக்கொள்ளவில்லை",
  "Needed to continue": "தொடர்வதற்குத் தேவை",
  "Your choice": "உங்கள் விருப்பம்",
  "What we collect": "நாங்கள் என்ன சேகரிக்கிறோம்",
  "How it is used": "இது எப்படிப் பயன்படுகிறது",
  "Without this we cannot collect your health information. You can still see your doctor as usual — you would just fill the form there instead.":
    "இது இல்லாமல் உங்கள் உடல்நல தகவலைச் சேகரிக்க முடியாது. வழக்கம்போல் மருத்துவரைப் பார்க்கலாம் — படிவத்தை அங்கே நிரப்ப வேண்டியிருக்கும்.",
  "Listen to this": "இதைக் கேளுங்கள்",

  // --- Medical history form ---------------------------------------------
  "Your health history": "உங்கள் உடல்நல வரலாறு",
  "Tell us once. Next time you only describe what is new.":
    "ஒரு முறை சொல்லுங்கள். அடுத்த முறை புதிதாக என்ன என்பதை மட்டும் சொல்லுங்கள்.",
  "Type here and press Add": "இங்கே தட்டச்சு செய்து சேர் என்பதை அழுத்துங்கள்",
  "Nothing to add": "சேர்க்க எதுவும் இல்லை",
  "Common answers": "வழக்கமான பதில்கள்",
  "Health history": "உடல்நல வரலாறு",

  // --- Documents ---------------------------------------------------------
  "Previous medical records": "முந்தைய மருத்துவப் பதிவுகள்",
  "Add a photo of a prescription, lab report or discharge summary. This is optional.":
    "மருந்துச் சீட்டு, பரிசோதனை அறிக்கை அல்லது வெளியேற்ற சுருக்கத்தின் புகைப்படத்தைச் சேர்க்கவும். இது விருப்பத்திற்குரியது.",
  "Choose a photo or PDF": "புகைப்படம் அல்லது PDF தேர்ந்தெடுங்கள்",
  "Uploading…": "பதிவேற்றப்படுகிறது…",
  "What is this?": "இது என்ன?",
  "Short description": "சுருக்கமான விவரம்",
  "For example: Dr Mehta, March 2026": "எடுத்துக்காட்டாக: டாக்டர் மேத்தா, மார்ச் 2026",
  "No records added": "எந்தப் பதிவும் சேர்க்கப்படவில்லை",
  "You can add records now or later from your profile. Your doctor can see them either way.":
    "பதிவுகளை இப்போது அல்லது பிறகு உங்கள் சுயவிவரத்தில் இருந்து சேர்க்கலாம். இரண்டு வழியிலும் உங்கள் மருத்துவர் அவற்றைப் பார்க்க முடியும்.",
  "Your records are saved and shown to your doctor as you uploaded them.":
    "உங்கள் பதிவுகள் சேமிக்கப்பட்டு, நீங்கள் பதிவேற்றியது போலவே மருத்துவருக்குக் காட்டப்படும்.",
  "Prescription": "மருந்துச் சீட்டு",
  "Lab report": "பரிசோதனை அறிக்கை",
  "Discharge summary": "வெளியேற்ற சுருக்கம்",
  "Something else": "வேறு ஏதாவது",
  "Reading your document…": "உங்கள் ஆவணம் படிக்கப்படுகிறது…",
  "Read this document": "இந்த ஆவணத்தைப் படி",
  "Try reading again": "மீண்டும் படிக்க முயற்சிக்கவும்",
  "Information found in this document": "இந்த ஆவணத்தில் கிடைத்த தகவல்",
  "This is what the document appears to say. It is not a diagnosis — please check it and tell us if anything looks wrong.":
    "ஆவணத்தில் இது சொல்லப்பட்டுள்ளது போல் தெரிகிறது. இது நோய் கண்டறிதல் அல்ல — இதைச் சரிபார்த்து, ஏதேனும் தவறாகத் தெரிந்தால் சொல்லுங்கள்.",
  "That is correct": "அது சரி",
  "That is not right": "அது சரி இல்லை",
  "Confirmed by you": "நீங்கள் உறுதிப்படுத்தியது",
  "You marked this wrong": "இதைத் தவறு எனக் குறித்தீர்கள்",
  "Show the text we read": "நாங்கள் படித்த எழுத்தைக் காட்டு",
  "We read the text but did not recognise any medical details. Your doctor can still read the document.":
    "எழுத்தைப் படித்தோம், ஆனால் எந்த மருத்துவ விவரத்தையும் அறிய முடியவில்லை. உங்கள் மருத்துவர் இந்த ஆவணத்தைப் படிக்க முடியும்.",
  "Within the printed range": "அச்சிடப்பட்ட வரம்பிற்குள்",
  "Below the printed range": "அச்சிடப்பட்ட வரம்பிற்குக் கீழே",
  "Above the printed range": "அச்சிடப்பட்ட வரம்பிற்கு மேலே",
  "Could not be compared": "ஒப்பிட முடியவில்லை",
  "Values are compared only against the range printed on your report. A healthcare professional should review them.":
    "மதிப்புகள் உங்கள் அறிக்கையில் அச்சிடப்பட்ட வரம்புடன் மட்டுமே ஒப்பிடப்படுகின்றன. ஒரு மருத்துவப் பணியாளர் அவற்றைப் பரிசோதிக்க வேண்டும்.",

  // --- Timeline ----------------------------------------------------------
  "Your medical timeline": "உங்கள் மருத்துவ காலவரிசை",
  "Everything we know about, newest first.":
    "எங்களுக்குத் தெரிந்த அனைத்தும், புதியது முதலில்.",
  "Nothing here yet": "இங்கே இன்னும் எதுவும் இல்லை",
  "Once you answer questions or add a record, it will appear here.":
    "நீங்கள் கேள்விகளுக்குப் பதிலளித்தால் அல்லது பதிவு சேர்த்தால், அது இங்கே தோன்றும்.",
  "Everything": "அனைத்தும்",
  "Needs your check": "உங்கள் சரிபார்ப்பு தேவை",
  "No date on record": "பதிவில் தேதி இல்லை",

  // --- Review ------------------------------------------------------------
  "Check your information": "உங்கள் தகவலைச் சரிபார்க்கவும்",
  "Please look through this before we finish. You can change anything.":
    "முடிப்பதற்கு முன் இதைப் பாருங்கள். நீங்கள் எதையும் மாற்றலாம்.",
  "You told us": "நீங்கள் சொன்னீர்கள்",
  "From your documents": "உங்கள் ஆவணங்களிலிருந்து",
  "Still missing": "இன்னும் விடுபட்டவை",
  "These are usually useful for your doctor. You can add them now or later.":
    "இவை பொதுவாக உங்கள் மருத்துவருக்குப் பயனுள்ளவை. இவற்றை இப்போது அல்லது பிறகு சேர்க்கலாம்.",
  "Summary for your doctor": "உங்கள் மருத்துவருக்கான சுருக்கம்",
  "This is correct — finish": "இது சரி — நிறைவு செய்",
  "Change this": "இதை மாற்று",
  "You said this": "நீங்கள் இதைச் சொன்னீர்கள்",
  "Found in a document": "ஆவணத்தில் கிடைத்தது",
  "Nothing recorded": "எதுவும் பதிவு செய்யப்படவில்லை",

  // --- Profile / completion ---------------------------------------------
  "You are all set": "அனைத்தும் தயார்",
  "Your health profile is saved. Show this screen at the reception desk.":
    "உங்கள் உடல்நல சுயவிவரம் சேமிக்கப்பட்டது. இந்தத் திரையை வரவேற்பு மேசையில் காட்டுங்கள்.",
  "View my profile": "என் சுயவிவரத்தைக் காண்க",
  "Your health profile": "உங்கள் உடல்நல சுயவிவரம்",
  "No visits recorded yet": "இன்னும் எந்த வருகையும் பதிவு செய்யப்படவில்லை",
  "Finish setting up": "அமைப்பை நிறைவு செய்",
  "Your profile is not finished yet. Complete it so your doctor has your full history.":
    "உங்கள் சுயவிவரம் இன்னும் முடியவில்லை. உங்கள் மருத்துவரிடம் முழு வரலாறு இருக்க அதை நிறைவு செய்யுங்கள்.",
  "items recorded": "பதிவு செய்யப்பட்டன",
  "At your next visit you will only be asked what has changed.":
    "அடுத்த வருகையில் என்ன மாறியுள்ளது என்பது மட்டுமே கேட்கப்படும்.",

  // --- Voice --------------------------------------------------------------
  "Tap to speak": "பேச தொடுங்கள்",
  "Listening…": "கேட்கிறது…",
  "Working out what you said…": "நீங்கள் சொன்னதைப் புரிந்துகொள்கிறது…",
  "We heard": "நாங்கள் கேட்டோம்",
  "That is right": "அது சரி",
  "Say it again": "மீண்டும் சொல்லுங்கள்",
  "Type instead": "அதற்குப் பதிலாகத் தட்டச்சு செய்",
  "Recording…": "பதிவு செய்யப்படுகிறது…",
  "Voice input problem": "குரல் உள்ளீட்டில் சிக்கல்",
  "This device has no voice for the selected language, so questions cannot be read aloud. All text stays on screen.":
    "இந்தக் கருவியில் தேர்ந்தெடுத்த மொழிக்கான குரல் இல்லை, எனவே கேள்விகளைச் சத்தமாக வாசிக்க முடியாது. எழுத்து அனைத்தும் திரையில் இருக்கும்.",
  "Voice input is not available in this browser, so please type or tap your answers.":
    "இந்த உலாவியில் குரல் உள்ளீடு கிடைக்கவில்லை, எனவே உங்கள் பதில்களைத் தட்டச்சு செய்யுங்கள் அல்லது தொடுங்கள்.",

  // --- Interview ----------------------------------------------------------
  "We will ask a few questions, one at a time. Speak or tap — whichever is easier.":
    "ஒரு நேரத்தில் ஒன்றாகச் சில கேள்விகளைக் கேட்போம். பேசுங்கள் அல்லது தொடுங்கள் — எது எளிதோ.",
  "Continue where you left off": "நிறுத்திய இடத்தில் இருந்து தொடரவும்",
  "Follow-up question": "தொடர் கேள்வி",
  "Smart assistance is unavailable right now, so we are using our standard questions. Nothing you have answered is lost.":
    "நுண்ணறிவு உதவி இப்போது கிடைக்கவில்லை, எனவே வழக்கமான கேள்விகளைப் பயன்படுத்துகிறோம். நீங்கள் அளித்த எந்தப் பதிலும் இழக்கப்படவில்லை.",
  "That is everything we need": "எங்களுக்குத் தேவையான அனைத்தும் ஆயிற்று",
  "Next you can add old medical records, or go straight to reviewing what you told us.":
    "அடுத்து பழைய மருத்துவப் பதிவுகளைச் சேர்க்கலாம், அல்லது நீங்கள் சொன்னதை நேரடியாகச் சரிபார்க்கலாம்.",

  // --- AYUSH ---------------------------------------------------------------
  "Include Ayurveda questions": "ஆயுர்வேத கேள்விகளைச் சேர்",
  "Optional. Used at AYUSH facilities to record your constitution and routine.":
    "விருப்பத்திற்குரியது. உங்கள் உடல் இயல்பையும் அன்றாட வழக்கத்தையும் பதிவு செய்ய ஆயுஷ் நிலையங்களில் பயன்படுகிறது.",
  "Ayurveda assessment": "ஆயுர்வேத மதிப்பீடு",
  "Skip these questions": "இந்தக் கேள்விகளைத் தவிர்",
  "Include them": "அவற்றைச் சேர்",
  "Ten-fold examination": "தசவித பரீக்ஷை",
  "Dashavidha Pariksha — your constitution and current state.":
    "தசவித பரீக்ஷை — உங்கள் உடல் இயல்பும் தற்போதைய நிலையும்.",
  "Eight-fold examination": "அஷ்டஸ்தான பரீக்ஷை",
  "Ashtasthana Pariksha. You describe what you notice; your practitioner examines and confirms each of these.":
    "அஷ்டஸ்தான பரீக்ஷை. நீங்கள் உணர்வதை நீங்கள் சொல்கிறீர்கள்; உங்கள் மருத்துவர் பரிசோதித்து இவை ஒவ்வொன்றையும் உறுதிப்படுத்துகிறார்.",
  "Digestion, sleep and routine": "செரிமானம், தூக்கம் மற்றும் அன்றாட வழக்கம்",
  "Agni, Koshtha, Nidra and Manas.": "அக்னி, கோஷ்டம், நித்திரை மற்றும் மனஸ்.",
  "factors recorded": "காரணிகள் பதிவு",
  "Record your constitution, examination findings and routine for an Ayurvedic consultation.":
    "ஆயுர்வேத ஆலோசனைக்காக உங்கள் உடல் இயல்பு, பரிசோதனை முடிவுகள் மற்றும் அன்றாட வழக்கத்தைப் பதிவு செய்யுங்கள்.",
  "Open assessment": "மதிப்பீட்டைத் திற",
  "These answers are recorded for your practitioner. Nothing here is assessed or interpreted by the app.":
    "இந்தப் பதில்கள் உங்கள் மருத்துவருக்காகப் பதிவு செய்யப்படுகின்றன. இவற்றில் எதுவும் செயலியால் மதிப்பிடப்படுவதோ விளக்கப்படுவதோ இல்லை.",
  "Type of treatment": "சிகிச்சை வகை",
  "Modern medicine": "நவீன மருத்துவம்",
  "Ayurveda": "ஆயுர்வேதம்",
  "We record which system you chose and ask about your diet and routine. Examination questions specific to this system are not built yet.":
    "நீங்கள் தேர்ந்தெடுத்த முறையைப் பதிவு செய்து, உங்கள் உணவு மற்றும் அன்றாட வழக்கம் பற்றிக் கேட்கிறோம். இந்த முறைக்கே உரிய பரிசோதனைக் கேள்விகள் இன்னும் உருவாக்கப்படவில்லை.",
  "Your diet (Ahara)": "உங்கள் உணவு முறை",
  "Your routine (Vihara)": "உங்கள் அன்றாட வழக்கம்",
  "Ayurvedic examination you answered": "நீங்கள் பதிலளித்த ஆயுர்வேத பரீக்ஷை",
  "{count} of {total} factors recorded": "{total} இல் {count} காரணிகள் பதிவு",
  "Ayurveda details saved": "ஆயுர்வேத விவரங்கள் சேமிக்கப்பட்டன",

  // --- Landing page: problem, flow, features -----------------------------
  "Features": "அமைவுகள்",
  "For clinics": "மருத்துவமனைகளுக்கு",
  "Kiosk mode": "கியாஸ்க் முறை",
  "Your doctor should already know your history when you walk in":
    "நீங்கள் உள்ளே வரும்போதே உங்கள் மருத்துவருக்கு உங்கள் வரலாறு தெரிந்திருக்க வேண்டும்",
  "MediKiosk collects a patient's medical history before the consultation — by voice, in their own language — so the few minutes with the doctor are spent on the problem, not on paperwork.":
    "மெடிகியாஸ்க் ஆலோசனைக்கு முன்பே நோயாளியின் மருத்துவ வரலாற்றைச் சேகரிக்கிறது — குரல் மூலம், அவர்களின் சொந்த மொழியில் — இதனால் மருத்துவருடன் கிடைக்கும் சில நிமிடங்கள் காகித வேலையில் அல்ல, பிரச்சினையில் செலவாகும்.",
  "Try the patient flow": "நோயாளியின் வழியைப் பாருங்கள்",
  "See a demo patient": "மாதிரி நோயாளியைப் பாருங்கள்",
  "The problem is time": "பிரச்சினை நேரம்",
  "A patient repeats their history at every visit. The clinician spends most of a very short consultation writing it down. Both lose, and the record still ends up thin.":
    "நோயாளி ஒவ்வொரு வருகையிலும் தன் வரலாற்றை மீண்டும் சொல்கிறார். மிகக் குறுகிய ஆலோசனை நேரத்தின் பெரும் பகுதியை மருத்துவர் அதை எழுதுவதில் செலவிடுகிறார். இருவருக்கும் இழப்பு, பதிவும் இன்னும் குறைவாகவே இருக்கிறது.",
  "Why it matters here": "இது இங்கே ஏன் முக்கியம்",
  "Figures are published estimates, shown with their source and year. Please re-check them against the latest release before citing.":
    "எண்கள் வெளியிடப்பட்ட மதிப்பீடுகள், மூலமும் ஆண்டும் சேர்த்துக் காட்டப்பட்டுள்ளன. மேற்கோள் காட்டும் முன் சமீபத்திய வெளியீட்டுடன் மீண்டும் சரிபார்க்கவும்.",
  "Illustrative arithmetic": "விளக்கத்திற்கான கணக்கு",
  "In the": "இந்த",
  "you have spent on this page, a doctor working at India's average pace would have seen about":
    "நேரத்தை நீங்கள் இந்தப் பக்கத்தில் செலவிட்டீர்கள்; அதில் இந்தியாவின் சராசரி வேகத்தில் வேலை செய்யும் மருத்துவர் ஏறத்தாழ இந்த அளவு நோயாளிகளைப் பார்த்திருப்பார்",
  "patients.": "நோயாளிகள்.",
  "Derived from the average consultation length, not a live measurement":
    "சராசரி ஆலோசனை நேரத்தில் இருந்து கணக்கிடப்பட்டது, நேரடி அளவீடு அல்ல",
  "Before the visit": "வருகைக்கு முன்",
  "The patient answers simple questions at a kiosk or on their phone — speaking or tapping, in English or an Indian language.":
    "நோயாளி கியாஸ்கில் அல்லது தன் கைபேசியில் எளிய கேள்விகளுக்குப் பதிலளிக்கிறார் — பேசியோ தொட்டோ, ஆங்கிலத்திலோ ஒரு இந்திய மொழியிலோ.",
  "Old records are read": "பழைய பதிவுகள் படிக்கப்படுகின்றன",
  "A photo of a prescription or lab report is scanned, and the medicines, diagnoses and test values found in it are listed for the patient to confirm.":
    "மருந்துச் சீட்டு அல்லது பரிசோதனை அறிக்கையின் புகைப்படம் வருடப்படுகிறது, அதில் கிடைத்த மருந்துகள், நோய்க் குறிப்புகள், பரிசோதனை மதிப்புகள் நோயாளியின் உறுதிப்படுத்தலுக்காகக் காட்டப்படுகின்றன.",
  "The clinician gets a history": "மருத்துவருக்கு வரலாறு கிடைக்கிறது",
  "A structured summary, with each fact labelled as reported by the patient, read from a document, or already on record.":
    "ஒரு ஒழுங்கான சுருக்கம்; ஒவ்வொரு தகவலும் நோயாளி சொன்னதா, ஆவணத்தில் இருந்து படித்ததா, ஏற்கெனவே பதிவில் இருந்ததா என்று குறிக்கப்பட்டிருக்கும்.",
  "The second visit is the point": "உண்மையான பயன் இரண்டாம் வருகையில்",
  "A returning patient does not repeat anything. They describe what is wrong today, and the questions adapt around what is already known.":
    "மீண்டும் வரும் நோயாளி எதையும் மீண்டும் சொல்வதில்லை. இன்று என்ன பிரச்சினை என்பதை மட்டும் சொல்கிறார், ஏற்கெனவே தெரிந்ததற்கு ஏற்ப கேள்விகள் மாறுகின்றன.",
  "What it does": "இது என்ன செய்கிறது",
  "Voice, in your language": "குரல், உங்கள் மொழியில்",
  "Speak your answers and correct the transcription before it is saved. Typing and tapping are always available — voice is never required.":
    "உங்கள் பதில்களைப் பேசி, சேமிக்கப்படுவதற்கு முன் எழுத்தைச் சரிசெய்யுங்கள். தட்டச்சும் தொடுதலும் எப்போதும் கிடைக்கும் — குரல் ஒருபோதும் கட்டாயம் அல்ல.",
  "Built for every patient": "எல்லா நோயாளிக்காகவும் கட்டப்பட்டது",
  "A short comfort check suggests text size, contrast, audio and a simpler screen layout. Age alone never decides it, and the patient can override anything.":
    "ஒரு சிறு வசதி சோதனை எழுத்தின் அளவு, நிற வேறுபாடு, ஒலி, எளிய திரை அமைப்பைப் பரிந்துரைக்கிறது. வயது மட்டுமே இதைத் தீர்மானிப்பதில்லை, நோயாளி எதையும் மாற்றிக்கொள்ளலாம்.",
  "Reads old records": "பழைய பதிவுகளைப் படிக்கிறது",
  "Prescriptions and lab reports are scanned on the server. Lab values are compared only against the range printed on the report — never guessed.":
    "மருந்துச் சீட்டுகளும் பரிசோதனை அறிக்கைகளும் சேவையகத்தில் வருடப்படுகின்றன. பரிசோதனை மதிப்புகள் அறிக்கையில் அச்சிடப்பட்ட வரம்புடன் மட்டுமே ஒப்பிடப்படுகின்றன — ஊகிக்கப்படுவதில்லை.",
  "Flags what should not wait": "காத்திருக்கக் கூடாததைக் குறிக்கிறது",
  "Answers are screened for presentations that need prompt attention. The patient is told to speak to staff, and the flag cannot be switched off from the kiosk.":
    "விரைவான கவனம் தேவைப்படும் அறிகுறிகளுக்குப் பதில்கள் பரிசோதிக்கப்படுகின்றன. நோயாளியிடம் பணியாளர்களுடன் பேசச் சொல்லப்படுகிறது, இந்தக் குறியீட்டைக் கியாஸ்கில் இருந்து நிறுத்த முடியாது.",
  "Allopathy and AYUSH": "அலோபதி மற்றும் ஆயுஷ்",
  "The patient chooses which system of medicine they are here for. An Ayurvedic visit adds the Dashavidha and Ashtasthana examination; an allopathic visit stays short.":
    "எந்த மருத்துவ முறைக்காக வந்திருக்கிறார் என்பதை நோயாளி தேர்ந்தெடுக்கிறார். ஆயுர்வேத வருகையில் தசவித, அஷ்டஸ்தான பரீக்ஷை சேர்க்கப்படுகிறது; அலோபதி வருகை குறுகியதாகவே இருக்கும்.",
  "Consent, and nothing implied": "ஒப்புதல், ஊகம் ஏதுமில்லை",
  "Health information is collected only after the patient agrees, per purpose, and consent can be withdrawn. Health-ID linkage is prepared for ABDM but not connected.":
    "நோயாளி ஒப்புக்கொண்ட பிறகே, ஒவ்வொரு நோக்கத்திற்கும் தனியாக உடல்நல தகவல் சேகரிக்கப்படுகிறது, ஒப்புதலைத் திரும்பப் பெறலாம். உடல்நல அடையாள இணைப்பு ABDM-க்குத் தயாராக உள்ளது, ஆனால் இணைக்கப்படவில்லை.",
  "What it does not do": "இது என்ன செய்யாது",
  "MediKiosk does not diagnose, does not prescribe, and does not replace a clinician. It organises what the patient tells us and what their documents say, and labels which is which.":
    "மெடிகியாஸ்க் நோயைக் கண்டறிவதில்லை, மருந்து பரிந்துரைப்பதில்லை, மருத்துவருக்குப் பதிலாக வருவதில்லை. நோயாளி சொல்வதையும் அவரது ஆவணங்களில் உள்ளதையும் ஒழுங்குபடுத்தி, எது எது என்று குறிக்கிறது.",
  "Specifications": "விவரக்குறிப்புகள்",
  "Stack": "தொழில்நுட்பம்",
  "React and TypeScript on the front, FastAPI and PostgreSQL behind, as a modular monolith. Alembic migrations, Docker images for both halves.":
    "முன்பக்கத்தில் React மற்றும் TypeScript, பின்பக்கத்தில் FastAPI மற்றும் PostgreSQL, ஒரு தொகுதிவாரி ஒற்றைக் கட்டமைப்பாக. Alembic இடப்பெயர்வுகள், இரு பகுதிகளுக்கும் Docker படிமங்கள்.",
  "Clinical data": "மருத்துவத் தகவல்",
  "Every fact carries its source, confidence and whether a person has verified it. A new visit never overwrites the historical record.":
    "ஒவ்வொரு தகவலுடனும் அதன் மூலம், நம்பகத்தன்மை, ஒருவர் அதைச் சரிபார்த்தாரா என்பது இருக்கும். புதிய வருகை பழைய பதிவை ஒருபோதும் அழிப்பதில்லை.",
  "AI": "ஏஐ",
  "The interview is a deterministic state machine. A model may help read an answer or a document, but its output is schema-validated and every path works with AI switched off.":
    "நேர்காணல் ஒரு நிலையான நிலை-இயந்திரம். ஒரு பதிலையோ ஆவணத்தையோ படிக்க மாதிரி உதவலாம், ஆனால் அதன் விளைவு திட்டவரையின்படி சரிபார்க்கப்படுகிறது, ஏஐ நிறுத்தப்பட்டிருந்தாலும் எல்லா வழிகளும் வேலை செய்யும்.",
  "All six languages are complete: English, Hindi, Marathi, Tamil, Gujarati and Punjabi. The four regional translations are machine-authored and marked for review by a speaker of each; anything still untranslated falls back rather than breaking.":
    "ஆறு மொழிகளும் முழுமையானவை: ஆங்கிலம், இந்தி, மராத்தி, தமிழ், குஜராத்தி, பஞ்சாபி. நான்கு பிராந்திய மொழிபெயர்ப்புகளும் இயந்திரத்தால் செய்யப்பட்டவை, அந்த மொழி பேசுபவரின் பரிசோதனைக்காகக் குறிக்கப்பட்டுள்ளன; இன்னும் மொழிபெயர்க்கப்படாதது உடைவதற்குப் பதிலாக மாற்று மொழியில் தோன்றும்.",
  "Failure behaviour": "செயலிழப்பின் போது நடத்தை",
  "No workflow depends on one external service. If AI, voice, scanning or the health-ID service is unavailable, the patient keeps going and nothing already entered is lost.":
    "எந்த வேலைப்பாதையும் ஒரே வெளிச் சேவையை நம்பியிருப்பதில்லை. ஏஐ, குரல், வருடல் அல்லது உடல்நல அடையாள சேவை கிடைக்காவிட்டாலும் நோயாளி தொடர்ந்து செல்கிறார், ஏற்கெனவே உள்ளிட்டது எதுவும் இழக்கப்படுவதில்லை.",
  "Accessibility": "அணுகல் எளிமை",
  "Keyboard navigable, visible focus, semantic landmarks, large touch targets, and status never conveyed by colour alone.":
    "விசைப்பலகையால் இயக்கக்கூடியது, தெரியும் கவனக்குறி, பொருள்தரும் அடையாளங்கள், பெரிய தொடு இடங்கள், நிலை ஒருபோதும் நிறத்தால் மட்டும் சொல்லப்படுவதில்லை.",
  "Runs on a tablet at reception or on the patient's own phone. Records live in your PostgreSQL database, and the schema is shaped for the clinician view that comes next.":
    "வரவேற்பறை டேப்லெட்டிலோ நோயாளியின் சொந்தக் கைபேசியிலோ இயங்குகிறது. பதிவுகள் உங்கள் PostgreSQL தரவுத்தளத்தில் இருக்கும், திட்டவரை அடுத்து வரும் மருத்துவர் பார்வைக்கு ஏற்ப வடிவமைக்கப்பட்டுள்ளது.",
  "See it work": "இது இயங்குவதைப் பாருங்கள்",
  "Sign in with a mobile number, or open a demo patient with a full history already on file.":
    "கைபேசி எண்ணுடன் உள்நுழையுங்கள், அல்லது முழு வரலாறு உள்ள மாதிரி நோயாளியைத் திறங்கள்.",
  "Prototype. All demo patients and medical records are fictional. Health-ID verification is simulated and not connected to ABDM.":
    "முன்மாதிரி. எல்லா மாதிரி நோயாளிகளும் மருத்துவப் பதிவுகளும் கற்பனையானவை. உடல்நல அடையாள சரிபார்ப்பு போலியானது, ABDM-உடன் இணைக்கப்படவில்லை.",

  // --- Returning-patient home ---------------------------------------------
  "Start a new health visit": "புதிய உடல்நல வருகையைத் தொடங்கு",
  "Tell us what is troubling you today. We already have your history.":
    "இன்று உங்களுக்கு என்ன தொந்தரவு என்று சொல்லுங்கள். உங்கள் வரலாறு எங்களிடம் உள்ளது.",
  "Continue your visit": "உங்கள் வருகையைத் தொடரவும்",
  "Your health summary": "உங்கள் உடல்நல சுருக்கம்",
  "Ongoing conditions": "தொடர்கின்ற நோய்கள்",
  "Your medicines": "உங்கள் மருந்துகள்",
  "Allergies": "ஒவ்வாமைகள்",
  "Recent records": "சமீபத்திய பதிவுகள்",
  "Recent activity": "சமீபத்திய செயல்பாடு",
  "Last visit": "கடைசி வருகை",
  "visits recorded": "வருகைகள் பதிவு",
  "Finish setting up your profile": "உங்கள் சுயவிவரத்தை நிறைவு செய்யுங்கள்",
  "Nothing recorded yet": "இன்னும் எதுவும் பதிவு செய்யப்படவில்லை",
  "You have not added any medical records yet":
    "நீங்கள் இன்னும் எந்த மருத்துவப் பதிவையும் சேர்க்கவில்லை",
  "A photo of a prescription or lab report helps your doctor see your history.":
    "மருந்துச் சீட்டு அல்லது பரிசோதனை அறிக்கையின் புகைப்படம் உங்கள் மருத்துவர் உங்கள் வரலாற்றைப் பார்க்க உதவுகிறது.",
  "No allergies recorded": "எந்த ஒவ்வாமையும் பதிவு செய்யப்படவில்லை",
  "Update my health history": "என் உடல்நல வரலாற்றைப் புதுப்பி",

  // --- Encounter (today's visit) -------------------------------------------
  "What brings you here today?": "இன்று நீங்கள் எதற்காக வந்தீர்கள்?",
  "Describe it in your own words — speak, type, or tap a common answer.":
    "உங்கள் சொற்களில் சொல்லுங்கள் — பேசுங்கள், தட்டச்சு செய்யுங்கள், அல்லது வழக்கமான பதிலைத் தொடுங்கள்.",
  "We already know about": "எங்களுக்கு ஏற்கெனவே தெரிந்தவை",
  "You will not be asked about these again. You can update them from your profile.":
    "இவை பற்றி மீண்டும் கேட்கப்படாது. உங்கள் சுயவிவரத்தில் இருந்து இவற்றைப் புதுப்பிக்கலாம்.",
  "About today only": "இன்று பற்றி மட்டும்",
  "New today": "இன்று புதியது",
  "Already on record": "ஏற்கெனவே பதிவில்",
  "That is everything for today": "இன்றைக்கு இதுவே அனைத்தும்",
  "Please check what you told us before we send it to the care team.":
    "மருத்துவக் குழுவுக்கு அனுப்பும் முன் நீங்கள் சொன்னதைச் சரிபார்க்கவும்.",
  "Check and submit": "சரிபார்த்து அனுப்பு",
  "Marked urgent": "அவசரம் எனக் குறிக்கப்பட்டது",
  "Marked urgent — please stay near the staff desk.":
    "அவசரம் எனக் குறிக்கப்பட்டது — பணியாளர் மேசைக்கு அருகில் இருங்கள்.",
  "What you told us": "நீங்கள் எங்களுக்குச் சொன்னது",
  "A member of staff will review this with you. This cannot be turned off from here.":
    "ஒரு பணியாளர் இதை உங்களுடன் பரிசோதிப்பார். இதை இங்கிருந்து நிறுத்த முடியாது.",
  "Staff have been notified. Please stay where you are.":
    "பணியாளர்களுக்குத் தெரிவிக்கப்பட்டுள்ளது. நீங்கள் இருக்கும் இடத்திலேயே இருங்கள்.",
  "Check today's visit": "இன்றைய வருகையைச் சரிபார்க்கவும்",
  "Please make sure this is right. You can change today's answers.":
    "இது சரியா என்பதை உறுதிப்படுத்துங்கள். இன்றைய பதில்களை மாற்றலாம்.",
  "Today's concern": "இன்றைய குறை",
  "What you told us today": "இன்று நீங்கள் சொன்னது",
  "questions you chose to skip": "நீங்கள் தவிர்த்த கேள்விகள்",
  "How much it troubles you": "இது உங்களை எவ்வளவு தொந்தரவு செய்கிறது",
  "out of 10": "10 இல்",
  "This rating is not what made your visit urgent — that came from the symptoms you described.":
    "இந்த மதிப்பெண்ணால் உங்கள் வருகை அவசரமாகவில்லை — அது நீங்கள் சொன்ன அறிகுறிகளால் வந்தது.",
  "Relevant existing history": "தொடர்புடைய ஏற்கெனவே உள்ள வரலாறு",
  "From your earlier visits. Editing this happens in your health history, not here.":
    "உங்கள் முந்தைய வருகைகளிலிருந்து. இதில் மாற்றம் உங்கள் உடல்நல வரலாற்றில் நடக்கும், இங்கே அல்ல.",
  "Records added today": "இன்று சேர்க்கப்பட்ட பதிவுகள்",
  "Change today's answers": "இன்றைய பதில்களை மாற்று",
  "Summary for the care team": "மருத்துவக் குழுவுக்கான சுருக்கம்",
  "Still needed": "இன்னும் தேவை",
  "Before you send this": "இதை அனுப்பும் முன்",
  "My current symptoms were recorded correctly":
    "என் தற்போதைய அறிகுறிகள் சரியாகப் பதிவு செய்யப்பட்டுள்ளன",
  "I have reviewed the information above": "மேலே உள்ள தகவலை நான் பரிசோதித்துவிட்டேன்",
  "I understand this will be used to support my healthcare visit":
    "இது என் மருத்துவ வருகைக்கு உதவப் பயன்படும் என்பதை நான் புரிந்துகொள்கிறேன்",
  "Send to the care team": "மருத்துவக் குழுவுக்கு அனுப்பு",
  "Your visit has been sent": "உங்கள் வருகை அனுப்பப்பட்டுவிட்டது",
  "Back to home": "முதல் பக்கத்திற்குத் திரும்பு",
  "This visit has already been sent. Start a new visit if something has changed.":
    "இந்த வருகை ஏற்கெனவே அனுப்பப்பட்டுவிட்டது. ஏதேனும் மாறியிருந்தால் புதிய வருகையைத் தொடங்குங்கள்.",

  // --- Errors and chrome ---------------------------------------------------
  "Something went wrong. Please try again.":
    "ஏதோ தவறாகிவிட்டது. மீண்டும் முயற்சிக்கவும்.",
  "We could not reach the server. Check the connection and try again.":
    "சேவையகத்தை அணுக முடியவில்லை. இணைப்பைச் சரிபார்த்து மீண்டும் முயற்சிக்கவும்.",
  "Your session has ended. Please sign in again.":
    "உங்கள் அமர்வு முடிந்தது. மீண்டும் உள்நுழையுங்கள்.",
  "This is needed to continue": "தொடர்வதற்கு இது தேவை",
  "Skip to main content": "முதன்மை உள்ளடக்கத்திற்குச் செல்",
  "Found in {name}": "{name} இல் கிடைத்தது",
  "Your answers are saved as you go — you can stop and come back.":
    "உங்கள் பதில்கள் அப்போதே சேமிக்கப்படுகின்றன — நிறுத்தி மீண்டும் வரலாம்.",

  // --- Enum labels -----------------------------------------------------------
  "Pending": "நிலுவையில்",
  "Processing": "செயலாக்கத்தில்",
  "Completed": "முடிந்தது",
  "Could not be read": "படிக்க முடியவில்லை",
  "Needs your review": "உங்கள் பரிசோதனை தேவை",
  "Not verified": "சரிபார்க்கப்படவில்லை",
  "Verified": "சரிபார்க்கப்பட்டது",
  "Skipped": "தவிர்க்கப்பட்டது",
  "Given": "அளிக்கப்பட்டது",
  "Declined": "மறுக்கப்பட்டது",
  "Withdrawn": "திரும்பப் பெறப்பட்டது",
  "Collecting your health information": "உங்கள் உடல்நல தகவலைச் சேகரிப்பது",
  "Sharing with the doctor treating you":
    "உங்களுக்குச் சிகிச்சை அளிக்கும் மருத்துவருடன் பங்கிடுவது",
  "Linking your ABHA number": "உங்கள் ஆபா எண்ணை இணைப்பது",
  "Standard": "நிலையான",
  "Easy Mode": "எளிய முறை",
  "Normal": "இயல்பு",
  "Large": "பெரியது",
  "Extra large": "மிகப் பெரியது",
  "High": "அதிகம்",
  "Voice": "குரல்",
  "Touch": "தொடுதல்",
  "Voice and touch": "குரலும் தொடுதலும்",
  "Typing": "தட்டச்சு",
  "Recommended for you": "உங்களுக்குப் பரிந்துரைக்கப்பட்டது",
  "Chosen by you": "நீங்கள் தேர்ந்தெடுத்தது",
  "Not started": "தொடங்கவில்லை",
  "In progress": "நடைபெறுகிறது",
  "Awaiting your review": "உங்கள் பரிசோதனைக்குக் காத்திருக்கிறது",
  "Cancelled": "ரத்து செய்யப்பட்டது",
  "Confirmed": "உறுதிப்படுத்தப்பட்டது",
  "Routine": "வழக்கமானது",
  "Priority": "முன்னுரிமை",
  "Urgent": "அவசரம்",
  "First visit": "முதல் வருகை",
  "Follow-up visit": "தொடர் வருகை",
  "From a document": "ஆவணத்தில் இருந்து",
  "From an earlier visit": "முந்தைய வருகையில் இருந்து",
  "From a clinician": "மருத்துவரிடம் இருந்து",
  "Condition": "நிலை",
  "Medicine": "மருந்து",
  "Test": "பரிசோதனை",
  "Procedure": "செயல்முறை",
  "Surgery": "அறுவை சிகிச்சை",
  "Allergy": "ஒவ்வாமை",
  "Vital sign": "உயிர்க் குறி",
  "Note": "குறிப்பு",
  "Visit": "வருகை",
  "Low": "குறைவு",
  "Unclear": "தெளிவற்றது",
  "Not reviewed": "பரிசோதிக்கப்படவில்லை",
  "Kept": "வைக்கப்பட்டது",
  "Removed": "நீக்கப்பட்டது",
  "Allopathy": "அலோபதி",
  "Homoeopathy": "ஹோமியோபதி",
  "Unani": "யுனானி",
  "Siddha": "சித்த மருத்துவம்",
  "Yoga and Naturopathy": "யோகா மற்றும் இயற்கை மருத்துவம்",
  "Not sure yet": "இன்னும் உறுதியில்லை",
  "Document you uploaded": "நீங்கள் பதிவேற்றிய ஆவணம்",
  "Visit record": "வருகைப் பதிவு",
  "Understood from what you said": "நீங்கள் சொன்னதிலிருந்து புரிந்துகொள்ளப்பட்டது",
};
