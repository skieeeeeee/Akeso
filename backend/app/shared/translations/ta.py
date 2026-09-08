"""Tamil translations, keyed by the English source string.

MACHINE-AUTHORED — pending review by a Tamil speaker. Clinical phrasing in
particular should be checked: a question that reads oddly to a patient gets a
worse answer, and a worse answer reaches a doctor.

Tamil needs this review more than the other three, not less. Devanagari is not
read in Tamil Nadu, so an untranslated Tamil string falls back to English
rather than to Hindi — a gap here is visible immediately, and a clumsy
translation has no second language behind it to soften it.

Add or correct an entry by editing this file; nothing else needs to change.
An inline `ta=` argument at a `t()` call site always overrides an entry here.

Terminology held consistent throughout: நோயாளி (patient), நோய் (illness),
மருந்து (medicine), பரிசோதனை (test/examination), வருகை (visit),
குறை (complaint), நோய் கண்டறிதல் (diagnosis), ஒப்புதல் (consent).
"""

from __future__ import annotations

TAMIL: dict[str, str] = {
    # --- Onboarding steps, greetings and status messages ------------------
    "Health ID": "உடல்நல அடையாள எண்",
    "Your details": "உங்கள் விவரங்கள்",
    "Comfort check": "வசதி சோதனை",
    "Your experience": "உங்கள் அனுபவம்",
    "Consent": "ஒப்புதல்",
    "Health history": "உடல்நல வரலாறு",
    "Done": "முடிந்தது",
    "Welcome": "வருக",
    "Welcome back": "மீண்டும் வருக",
    "Sorry, I did not catch that. Please try again, or tap an option.":
        "மன்னிக்கவும், எனக்குப் புரியவில்லை. மீண்டும் சொல்லுங்கள், அல்லது ஒரு "
        "விருப்பத்தைத் தொடுங்கள்.",
    "Saved. Ready to be read.": "சேமிக்கப்பட்டது. படிக்கத் தயார்.",
    "Reading your document. This usually takes a few seconds.":
        "உங்கள் ஆவணம் படிக்கப்படுகிறது. இதற்குப் பொதுவாகச் சில வினாடிகள் ஆகும்.",
    "We found some information in this document. Please check it.":
        "இந்த ஆவணத்தில் சில தகவல்கள் கிடைத்தன. அவற்றைச் சரிபார்க்கவும்.",
    "We read the text but could not pick out medical details. "
    "Your doctor can still read it.":
        "எழுத்தைப் படித்தோம், ஆனால் மருத்துவ விவரங்களைப் பிரித்தெடுக்க முடியவில்லை. "
        "உங்கள் மருத்துவர் இதைப் படிக்க முடியும்.",
    "We could not read this document. It is saved and you can try again.":
        "இந்த ஆவணத்தைப் படிக்க முடியவில்லை. இது சேமிக்கப்பட்டுள்ளது, மீண்டும் "
        "முயற்சிக்கலாம்.",
    "This summarises what you told us and what your documents say. "
    "It is not a diagnosis, and your doctor will go through it with you.":
        "நீங்கள் சொன்னதையும், உங்கள் ஆவணங்களில் உள்ளதையும் இது சுருக்கமாகத் தருகிறது. "
        "இது நோய் கண்டறிதல் அல்ல; உங்கள் மருத்துவர் இதை உங்களுடன் பார்ப்பார்.",
    "Your visit details have been sent to the care team. Please wait to be called.":
        "உங்கள் வருகை விவரங்கள் மருத்துவக் குழுவுக்கு அனுப்பப்பட்டுவிட்டன. "
        "அழைக்கப்படும் வரை காத்திருக்கவும்.",
    "Your visit has been sent and marked urgent. Please stay near the staff desk.":
        "உங்கள் விவரங்கள் அனுப்பப்பட்டு, அவசரம் எனக் குறிக்கப்பட்டுள்ளன. "
        "பணியாளர் மேசைக்கு அருகில் இருங்கள்.",

    # --- Accessibility assessment -------------------------------------
    "How comfortable are you using smartphones or digital devices?":
        "ஸ்மார்ட்போன் அல்லது டிஜிட்டல் கருவிகளைப் பயன்படுத்துவது உங்களுக்கு எவ்வளவு எளிதாக இருக்கிறது?",
    "This helps us choose how much detail to show on each screen.":
        "ஒவ்வொரு திரையிலும் எவ்வளவு விவரம் காட்ட வேண்டும் என்பதை இது தீர்மானிக்கிறது.",
    "Very comfortable": "மிகவும் எளிது",
    "Somewhat comfortable": "ஓரளவு எளிது",
    "I sometimes need help": "எனக்கு சில நேரங்களில் உதவி தேவை",
    "I prefer a simpler experience": "எனக்கு எளிமையான முறை பிடிக்கும்",
    "How would you prefer to answer questions?":
        "கேள்விகளுக்கு எப்படி பதிலளிக்க விரும்புகிறீர்கள்?",
    "You can always switch between speaking and tapping later.":
        "பேசுவது, தொடுவது — இவற்றுக்கு இடையே பிறகு எப்போதும் மாற்றிக்கொள்ளலாம்.",
    "By speaking": "பேசி",
    "By touching options": "விருப்பங்களைத் தொட்டு",
    "Both": "இரண்டும்",
    "Do you have difficulty reading text on screens?":
        "திரையில் உள்ள எழுத்துகளைப் படிப்பதில் உங்களுக்குச் சிரமம் உள்ளதா?",
    "If reading is hard, we can make text larger and read questions aloud.":
        "படிப்பது கடினமாக இருந்தால், எழுத்தைப் பெரிதாக்கி, கேள்விகளைச் சத்தமாக வாசிக்க முடியும்.",
    "Do you have difficulty seeing content on screens?":
        "திரையில் உள்ளதைப் பார்ப்பதில் உங்களுக்குச் சிரமம் உள்ளதா?",
    "We can increase the text size and use stronger colour contrast.":
        "எழுத்தின் அளவை அதிகரித்து, நிற வேறுபாட்டை இன்னும் தெளிவாக்க முடியும்.",
    "Do you have difficulty hearing audio instructions?":
        "ஒலி வழிகாட்டுதல்களைக் கேட்பதில் உங்களுக்குச் சிரமம் உள்ளதா?",
    "If hearing is hard, nothing in this app will depend on sound.":
        "கேட்பது கடினமாக இருந்தால், இந்தச் செயலியில் எதுவும் ஒலியை நம்பியிருக்காது.",
    "No difficulty": "சிரமம் இல்லை",
    "Sometimes": "சில நேரங்களில்",
    "Yes": "ஆம்",
    "No": "இல்லை",
    "Is there anything else that would make this easier for you?":
        "இது உங்களுக்கு இன்னும் எளிதாக அமைய வேறு ஏதாவது உள்ளதா?",
    "This is completely optional. Share only what you want to.":
        "இது முழுக்க முழுக்க விருப்பத்திற்குரியது. நீங்கள் சொல்ல விரும்புவதை மட்டும் சொல்லுங்கள்.",
    "I find reading and writing difficult": "படிப்பதும் எழுதுவதும் எனக்குக் கடினம்",
    "I have low vision": "எனக்குப் பார்வை குறைவு",
    "I am hard of hearing": "எனக்குக் கேட்கும் திறன் குறைவு",
    "Tapping the screen is tiring": "திரையைத் தொடுவது சோர்வாக இருக்கிறது",
    "Someone is helping me today": "இன்று ஒருவர் எனக்கு உதவுகிறார்",
    "I use sign language": "நான் சைகை மொழியைப் பயன்படுத்துகிறேன்",
    "Before we begin": "தொடங்குவதற்கு முன்",
    "Speak your answers": "உங்கள் பதில்களைப் பேசுங்கள்",
    "Speak or tap, whichever suits": "பேசுங்கள் அல்லது தொடுங்கள் — எது வசதியோ",
    "Tap to choose answers": "பதில்களைத் தேர்ந்தெடுக்கத் தொடுங்கள்",
    "One question at a time, large buttons": "ஒரு நேரத்தில் ஒரு கேள்வி, பெரிய பொத்தான்கள்",
    "All options on one screen": "எல்லா விருப்பங்களும் ஒரே திரையில்",
    "Standard": "நிலையான",
    "Easy": "எளிய",
    "Normal": "இயல்பு",
    "Large": "பெரியது",
    "Extra large": "மிகப் பெரியது",
    "Normal colours": "இயல்பான நிறங்கள்",
    "High contrast": "அதிக நிற வேறுபாடு",
    "Voice": "குரல்",
    "Touch": "தொடுதல்",
    "Optional": "விருப்பத்திற்குரியது",
    "Usually filled in from your date of birth.":
        "பொதுவாக உங்கள் பிறந்த தேதியிலிருந்து நிரப்பப்படுகிறது.",
    "Your doctor needs this to understand your case before you walk in.":
        "நீங்கள் உள்ளே வருவதற்கு முன் உங்கள் நிலையைப் புரிந்துகொள்ள மருத்துவருக்கு இது தேவை.",

    # --- Consent -------------------------------------------------------
    "Collecting your health information": "உங்கள் உடல்நல தகவலைச் சேகரிப்பது",
    "Your symptoms, past illnesses, surgeries, medicines, allergies and family history.":
        "உங்கள் அறிகுறிகள், முந்தைய நோய்கள், அறுவை சிகிச்சைகள், மருந்துகள், ஒவ்வாமைகள் "
        "மற்றும் குடும்ப வரலாறு.",
    "So your doctor already knows your history and can spend the visit on your actual problem.":
        "உங்கள் மருத்துவருக்கு உங்கள் வரலாறு ஏற்கெனவே தெரிந்திருக்கும், வருகையின் நேரம் "
        "உங்கள் உண்மையான பிரச்சினைக்கே செல்லும்.",
    "It is stored against your patient record and shown to the clinician treating you.":
        "இது உங்கள் நோயாளி பதிவுடன் சேமிக்கப்பட்டு, உங்களுக்குச் சிகிச்சை அளிக்கும் "
        "மருத்துவருக்குக் காட்டப்படுகிறது.",
    "Sharing with your doctor": "உங்கள் மருத்துவருடன் பங்கிடுவது",
    "A summary of what you tell us today, and any records you upload.":
        "இன்று நீங்கள் சொல்வதின் சுருக்கம், மற்றும் நீங்கள் பதிவேற்றும் ஆவணங்கள்.",
    "Only clinicians involved in your care can see it.":
        "உங்கள் சிகிச்சையில் ஈடுபட்டுள்ள மருத்துவர்கள் மட்டுமே இதைப் பார்க்க முடியும்.",
    "Linking your health ID": "உங்கள் உடல்நல அடையாள எண்ணை இணைப்பது",
    "The health ID number you entered, linked to this patient record.":
        "நீங்கள் அளித்த உடல்நல அடையாள எண், இந்த நோயாளி பதிவுடன் இணைக்கப்பட்டது.",
    "So your records can follow you between visits instead of starting over.":
        "ஒவ்வொரு வருகையிலும் புதிதாகத் தொடங்காமல், உங்கள் பதிவுகள் உங்களுடன் வரும்.",
    "This is a prototype and is not connected to the national ABDM network.":
        "இது ஒரு முன்மாதிரி; தேசிய ABDM வலையமைப்புடன் இணைக்கப்படவில்லை.",
    "We will ask about your health so your doctor is prepared before you meet. "
    "You choose what to share, and you can withdraw your consent at any time.":
        "நீங்கள் சந்திப்பதற்கு முன் மருத்துவர் தயாராக இருக்க, உங்கள் உடல்நலம் பற்றிக் "
        "கேட்போம். எதைப் பங்கிடுவது என்பதை நீங்களே தீர்மானிக்கிறீர்கள், உங்கள் ஒப்புதலை "
        "எப்போது வேண்டுமானாலும் திரும்பப் பெறலாம்.",
    "You can withdraw consent later from your profile. Nothing is shared without your agreement.":
        "பிறகு உங்கள் சுயவிவரத்தில் இருந்து ஒப்புதலைத் திரும்பப் பெறலாம். உங்கள் "
        "சம்மதம் இல்லாமல் எதுவும் பங்கிடப்படுவதில்லை.",

    # --- Red flags / safety --------------------------------------------
    "Please speak to healthcare staff now":
        "இப்போதே மருத்துவப் பணியாளர்களுடன் பேசுங்கள்",
    "Some of the symptoms you described may require urgent medical attention.":
        "நீங்கள் சொன்ன சில அறிகுறிகளுக்கு அவசர மருத்துவக் கவனம் தேவைப்படலாம்.",
    "Please inform nearby healthcare staff immediately. Show them this screen.":
        "அருகில் உள்ள மருத்துவப் பணியாளர்களுக்கு உடனே தெரிவியுங்கள். இந்தத் திரையை "
        "அவர்களுக்குக் காட்டுங்கள்.",
    "This does not confirm a medical condition. It only means a health worker should "
    "look at you sooner rather than later.":
        "இது எந்த நோயையும் உறுதிப்படுத்தவில்லை. மருத்துவப் பணியாளர் உங்களை தாமதமாக "
        "அல்ல, விரைவாகப் பார்க்க வேண்டும் — அதுமட்டுமே இதன் பொருள்.",
    "Marked urgent — please stay near the staff desk.":
        "அவசரம் எனக் குறிக்கப்பட்டது — பணியாளர் மேசைக்கு அருகில் இருங்கள்.",
    "Continue answering while waiting": "காத்திருக்கும்போது பதிலளிப்பதைத் தொடருங்கள்",
    "I need immediate assistance": "எனக்கு உடனடி உதவி தேவை",

    # --- Medical profile sections --------------------------------------
    "Why you are here": "நீங்கள் வந்த காரணம்",
    "First, tell us what brings you in today.":
        "முதலில், இன்று நீங்கள் எதற்காக வந்தீர்கள் என்று சொல்லுங்கள்.",
    "What problem brings you in today?": "இன்று எந்தப் பிரச்சினைக்காக வந்தீர்கள்?",
    "Describe it in your own words. You can speak instead of typing.":
        "உங்கள் சொற்களில் சொல்லுங்கள். தட்டச்சு செய்வதற்குப் பதிலாகப் பேசலாம்.",
    "e.g. chest pain for three days": "எ.கா. மூன்று நாட்களாக மார்பு வலி",
    "About this problem": "இந்தப் பிரச்சினை பற்றி",
    "How long has it been there, and what makes it better or worse?":
        "இது எவ்வளவு காலமாக உள்ளது, எதனால் குறைகிறது அல்லது அதிகரிக்கிறது?",
    "How long have you had this?": "இது உங்களுக்கு எவ்வளவு காலமாக உள்ளது?",
    "A rough idea is fine.": "தோராயமாகச் சொன்னாலும் போதும்.",
    "Started today": "இன்று தொடங்கியது",
    "2–3 days": "2–3 நாட்கள்",
    "About a week": "சுமார் ஒரு வாரம்",
    "A few weeks": "சில வாரங்கள்",
    "More than a month": "ஒரு மாதத்திற்கு மேல்",
    "How much does it trouble you, from 1 to 10?":
        "1 முதல் 10 வரை, இது உங்களை எவ்வளவு தொந்தரவு செய்கிறது?",
    "1 is very mild, 10 is the worst.": "1 என்பது மிகக் குறைவு, 10 என்பது மிக அதிகம்.",
    "Is there anything that makes it better or worse?":
        "எதனால் இது குறைகிறது அல்லது அதிகரிக்கிறது என்று ஏதாவது உள்ளதா?",
    "For example rest, food, walking, or a medicine you took.":
        "எடுத்துக்காட்டாக ஓய்வு, உணவு, நடப்பது, அல்லது நீங்கள் எடுத்த மருந்து.",
    "Anything else you feel": "நீங்கள் உணரும் வேறு ஏதாவது",
    "A quick check for other symptoms.": "பிற அறிகுறிகளுக்கு ஒரு விரைவான சோதனை.",
    "Are you also feeling any of these?": "இவற்றில் ஏதாவது உங்களுக்கு உள்ளதா?",
    "Choose as many as you like.": "உங்களுக்கு வேண்டிய அளவு தேர்ந்தெடுங்கள்.",
    "Fever": "காய்ச்சல்",
    "Cough": "இருமல்",
    "Breathlessness": "மூச்சுத் திணறல்",
    "Short of breath": "மூச்சு வாங்குதல்",
    "Headache": "தலைவலி",
    "Dizziness": "தலைச்சுற்றல்",
    "Vomiting": "வாந்தி",
    "Loose motions": "வாய்க்கால் கழிச்சல்",
    "Swelling": "வீக்கம்",
    "Pain": "வலி",
    "Very tired": "மிகுந்த சோர்வு",
    "Losing weight": "எடை குறைதல்",
    "Not sleeping well": "தூக்கம் வராமை",
    "Stomach pain": "வயிற்று வலி",
    "Stomach problem": "வயிற்றுப் பிரச்சினை",
    "Chest pain": "மார்பு வலி",

    # --- Past illnesses -------------------------------------------------
    "Past illnesses": "முந்தைய நோய்கள்",
    "Now a few questions about long-term health conditions.":
        "இப்போது நீண்டகால நோய்கள் பற்றி சில கேள்விகள்.",
    "Has a doctor told you that you have a long-term illness?":
        "உங்களுக்கு நீண்டகால நோய் உள்ளது என்று மருத்துவர் சொன்னாரா?",
    "Such as diabetes, blood pressure or asthma.":
        "சர்க்கரை நோய், இரத்த அழுத்தம் அல்லது ஆஸ்துமா போன்றவை.",
    "Any long-term illness you have been told you have?":
        "உங்களுக்கு உள்ளது என்று சொல்லப்பட்ட நீண்டகால நோய் ஏதாவது?",
    "Which illness?": "எந்த நோய்?",
    "Any old illness?": "பழைய நோய் ஏதாவது?",
    "Ongoing conditions": "தொடர்கின்ற நோய்கள்",
    "Diabetes": "சர்க்கரை நோய்",
    "High blood pressure": "உயர் இரத்த அழுத்தம்",
    "Asthma": "ஆஸ்துமா",
    "Heart disease": "இதய நோய்",
    "Thyroid problem": "தைராய்டு பிரச்சினை",
    "Tuberculosis": "காசநோய்",
    "Cancer": "புற்றுநோய்",
    "Something else": "வேறு ஏதாவது",
    "Are you currently taking medicine for {item}?":
        "{item}-க்கு நீங்கள் தற்போது மருந்து எடுத்துக்கொள்கிறீர்களா?",
    "Do you remember the name of the medicine for {item}?":
        "{item}-க்கான மருந்தின் பெயர் உங்களுக்கு நினைவிருக்கிறதா?",
    "If you are not sure, you can skip this or upload the prescription later.":
        "உறுதியாகத் தெரியாவிட்டால், இதைத் தவிர்க்கலாம் அல்லது பிறகு மருந்துச் சீட்டைப் "
        "பதிவேற்றலாம்.",

    # --- Operations -----------------------------------------------------
    "Operations": "அறுவை சிகிச்சைகள்",
    "Have you ever had an operation?":
        "உங்களுக்கு எப்போதாவது அறுவை சிகிச்சை நடந்திருக்கிறதா?",
    "Have you had any operation?": "உங்களுக்கு ஏதாவது அறுவை சிகிச்சை நடந்திருக்கிறதா?",
    "Any operation, however long ago.":
        "எந்த அறுவை சிகிச்சையும், எவ்வளவு பழையதாக இருந்தாலும்.",
    "What operation, and roughly when?": "எந்த அறுவை சிகிச்சை, தோராயமாக எப்போது?",
    "For example: gallbladder removed, 2019.":
        "எடுத்துக்காட்டாக: பித்தப்பை நீக்கம், 2019.",
    "e.g. gallbladder removed, 2019": "எ.கா. பித்தப்பை நீக்கம், 2019",

    # --- Medicines ------------------------------------------------------
    "Medicines": "மருந்துகள்",
    "Medicines you take": "நீங்கள் எடுக்கும் மருந்துகள்",
    "Let us record the medicines you take.":
        "நீங்கள் எடுக்கும் மருந்துகளைப் பதிவு செய்வோம்.",
    "Which medicines do you take regularly?": "நீங்கள் தவறாமல் எந்த மருந்துகளை எடுக்கிறீர்கள்?",
    "Which medicines are you taking now?": "நீங்கள் இப்போது எந்த மருந்துகளை எடுக்கிறீர்கள்?",
    "Any daily medicine?": "தினசரி மருந்து ஏதாவது?",
    "Include tablets, insulin, inhalers and drops.":
        "மாத்திரைகள், இன்சுலின், இன்ஹேலர் மற்றும் சொட்டு மருந்துகளையும் சேர்க்கவும்.",
    "Add them one at a time. Tap a common answer or say it aloud.":
        "ஒரு நேரத்தில் ஒன்றாகச் சேர்க்கவும். வழக்கமான பதிலைத் தொடவும் அல்லது சத்தமாகச் சொல்லவும்.",
    "Add them one at a time.": "ஒரு நேரத்தில் ஒன்றாகச் சேர்க்கவும்.",
    "e.g. Metformin 500 mg twice a day":
        "எ.கா. மெட்ஃபார்மின் 500 மி.கி. நாளுக்கு இருமுறை",

    # --- Allergies ------------------------------------------------------
    "Allergies": "ஒவ்வாமைகள்",
    "Medicine problems": "மருந்தால் ஏற்பட்ட பிரச்சினைகள்",
    "This one matters a lot for your safety.":
        "உங்கள் பாதுகாப்புக்கு இது மிகவும் முக்கியம்.",
    "Are you allergic to any medicine or food?":
        "ஏதாவது மருந்து அல்லது உணவு உங்களுக்கு ஒவ்வாமை உண்டாக்குகிறதா?",
    "Any allergy?": "ஏதாவது ஒவ்வாமை?",
    "Has any medicine ever caused you a problem?":
        "ஏதாவது மருந்து உங்களுக்கு எப்போதாவது பிரச்சினை உண்டாக்கியதா?",
    "Tell us even if you are unsure — it keeps you safe.":
        "உறுதியாகத் தெரியாவிட்டாலும் சொல்லுங்கள் — அது உங்களைப் பாதுகாக்கும்.",
    "For example it upset your stomach, or you had to stop it.":
        "எடுத்துக்காட்டாக வயிற்றைக் கெடுத்தது, அல்லது அதை நிறுத்த வேண்டியிருந்தது.",
    "Which ones?": "எவை?",
    "Penicillin": "பென்சிலின்",
    "Aspirin": "ஆஸ்பிரின்",
    "Sulfa drugs": "சல்பா மருந்துகள்",
    "Dust": "தூசி",
    "No known allergies": "தெரிந்த ஒவ்வாமை இல்லை",
    "e.g. penicillin, peanuts": "எ.கா. பென்சிலின், நிலக்கடலை",
    "e.g. aspirin upset my stomach": "எ.கா. ஆஸ்பிரின் என் வயிற்றைக் கெடுத்தது",

    # --- Family and personal history ------------------------------------
    "Family health": "குடும்ப உடல்நலம்",
    "Some illnesses run in families.": "சில நோய்கள் குடும்பத்தில் தொடர்ந்து வருகின்றன.",
    "Does any illness run in your close family?":
        "உங்கள் நெருங்கிய குடும்பத்தில் ஏதாவது நோய் தொடர்ந்து வருகிறதா?",
    "Any illness that runs in your family?":
        "உங்கள் குடும்பத்தில் தொடர்ந்து வரும் நோய் ஏதாவது?",
    "Any illness in the family?": "குடும்பத்தில் ஏதாவது நோய்?",
    "Parents, brothers, sisters or children.":
        "பெற்றோர், சகோதரர்கள், சகோதரிகள் அல்லது பிள்ளைகள்.",
    "Family history": "குடும்ப வரலாறு",
    "e.g. mother has diabetes": "எ.கா. அம்மாவுக்குச் சர்க்கரை நோய்",
    "Daily habits": "அன்றாட பழக்கங்கள்",
    "Daily life": "அன்றாட வாழ்க்கை",
    "A few questions about your habits and routine.":
        "உங்கள் பழக்கங்கள் மற்றும் அன்றாட வழக்கம் பற்றி சில கேள்விகள்.",
    "Anything about your habits your doctor should know?":
        "உங்கள் பழக்கங்கள் பற்றி மருத்துவர் அறிய வேண்டியது ஏதாவது உள்ளதா?",
    "Which of these apply to you?": "இவற்றில் எது உங்களுக்குப் பொருந்தும்?",
    "I do not smoke": "நான் புகைபிடிப்பதில்லை",
    "I smoke": "நான் புகைபிடிக்கிறேன்",
    "I do not drink alcohol": "நான் மது அருந்துவதில்லை",
    "I drink alcohol": "நான் மது அருந்துகிறேன்",
    "I exercise regularly": "நான் தவறாமல் உடற்பயிற்சி செய்கிறேன்",
    "Vegetarian diet": "சைவ உணவு",
    "Non-smoker": "புகைபிடிக்காதவர்",
    "Smoker": "புகைபிடிப்பவர்",
    "No alcohol": "மது இல்லை",
    "What work do you do?": "நீங்கள் என்ன வேலை செய்கிறீர்கள்?",
    "Some jobs affect health, so this can be useful.":
        "சில வேலைகள் உடல்நலத்தைப் பாதிக்கும், எனவே இது பயனுள்ளதாக இருக்கும்.",
    "e.g. non-smoker, vegetarian diet": "எ.கா. புகைபிடிக்காதவர், சைவ உணவு",
    "e.g. diabetes, high blood pressure": "எ.கா. சர்க்கரை நோய், உயர் இரத்த அழுத்தம்",

    # --- Investigations --------------------------------------------------
    "Earlier tests": "முந்தைய பரிசோதனைகள்",
    "Earlier test results": "முந்தைய பரிசோதனை முடிவுகள்",
    "Any tests you have had done recently.":
        "சமீபத்தில் நீங்கள் செய்துகொண்ட ஏதாவது பரிசோதனைகள்.",
    "Have you had any blood test or scan recently?":
        "சமீபத்தில் உங்களுக்கு இரத்தப் பரிசோதனை அல்லது ஸ்கேன் நடந்ததா?",
    "Any recent test result you remember?":
        "சமீபத்திய பரிசோதனை முடிவு ஏதாவது உங்களுக்கு நினைவிருக்கிறதா?",
    "In the last year or so.": "கடந்த ஒரு வருடத்தில்.",
    "Which test, and what did it show?": "எந்தப் பரிசோதனை, அதில் என்ன தெரிந்தது?",
    "If you have the report, you can upload it in the next step instead.":
        "அறிக்கை இருந்தால், அடுத்த படியில் அதைப் பதிவேற்றலாம்.",
    "e.g. HbA1c 8.4% in March": "எ.கா. மார்ச்சில் HbA1c 8.4%",

    # --- Anything else ---------------------------------------------------
    "Anything else": "வேறு ஏதாவது",
    "Anything else you would like your doctor to know?":
        "உங்கள் மருத்துவர் அறிய வேண்டியது வேறு ஏதாவது உள்ளதா?",
    "Are you also feeling anything else?": "உங்களுக்கு வேறு ஏதாவது உணர்வும் உள்ளதா?",
    "Could you tell us a little more?": "இன்னும் சற்று விரிவாகச் சொல்ல முடியுமா?",
    "Yes or no is enough.": "ஆம் அல்லது இல்லை என்பதே போதும்.",
    "Choose as many as apply.": "பொருந்துகின்ற அனைத்தையும் தேர்ந்தெடுங்கள்.",
    "This question was suggested from what you just said. You can skip it.":
        "நீங்கள் இப்போது சொன்னதிலிருந்து இந்தக் கேள்வி பரிந்துரைக்கப்பட்டது. இதைத் "
        "தவிர்க்கலாம்.",
    "Optional questions used in Ayurvedic practice.":
        "ஆயுர்வேத மருத்துவ முறையில் பயன்படும் விருப்பக் கேள்விகள்.",

    # --- Encounter script (today's visit) -------------------------------
    "Type of treatment": "சிகிச்சை வகை",
    "First, tell us which kind of care you are here for.":
        "முதலில், எந்த வகைச் சிகிச்சைக்காக வந்தீர்கள் என்று சொல்லுங்கள்.",
    "Which kind of treatment are you here for?":
        "எந்த வகைச் சிகிச்சைக்காக வந்திருக்கிறீர்கள்?",
    "Which treatment?": "எந்தச் சிகிச்சை?",
    "This decides which questions we ask. You can pick a different one next time.":
        "எந்தக் கேள்விகளைக் கேட்பது என்பதை இது தீர்மானிக்கிறது. அடுத்த முறை வேறொன்றைத் "
        "தேர்ந்தெடுக்கலாம்.",
    "Modern medicine (Allopathy)": "நவீன மருத்துவம் (அலோபதி)",
    "Allopathy": "அலோபதி",
    "Ayurveda": "ஆயுர்வேதம்",
    "Homoeopathy": "ஹோமியோபதி",
    "Unani": "யுனானி",
    "Siddha": "சித்த மருத்துவம்",
    "Yoga & Naturopathy": "யோகா மற்றும் இயற்கை மருத்துவம்",
    "Yoga and Naturopathy": "யோகா மற்றும் இயற்கை மருத்துவம்",
    "I am not sure": "எனக்கு உறுதியாகத் தெரியவில்லை",
    "Today's concern": "இன்றைய குறை",
    "A few questions about this problem only.":
        "இந்தப் பிரச்சினை பற்றி மட்டும் சில கேள்விகள்.",
    "We already have your health history. Just tell us what is new.":
        "உங்கள் உடல்நல வரலாறு எங்களிடம் உள்ளது. புதிதாக என்ன என்பதை மட்டும் சொல்லுங்கள்.",
    "Tell us what is troubling you today.":
        "இன்று உங்களுக்கு என்ன தொந்தரவு என்று சொல்லுங்கள்.",
    "What is troubling you today?": "இன்று உங்களுக்கு என்ன தொந்தரவு?",
    "What is troubling you?": "உங்களுக்கு என்ன தொந்தரவு?",
    "What brings you here today?": "இன்று நீங்கள் எதற்காக வந்தீர்கள்?",
    "In your own words. You can speak instead of typing.":
        "உங்கள் சொற்களில். தட்டச்சு செய்வதற்குப் பதிலாகப் பேசலாம்.",
    "When did it start?": "இது எப்போது தொடங்கியது?",
    "Since when?": "எப்போதிலிருந்து?",
    "Today": "இன்று",
    "Yesterday": "நேற்று",
    "2–3 days ago": "2–3 நாட்களுக்கு முன்",
    "About a week ago": "சுமார் ஒரு வாரத்திற்கு முன்",
    "Longer than a week": "ஒரு வாரத்திற்கு மேல்",
    "A few details": "சில விவரங்கள்",
    "Can you describe it a little more?": "இதைப் பற்றி இன்னும் சற்று சொல்ல முடியுமா?",
    "For example where it is, what it feels like, or what makes it worse.":
        "எடுத்துக்காட்டாக அது எங்கே உள்ளது, எப்படி இருக்கிறது, அல்லது எதனால் அதிகரிக்கிறது.",
    "How bad is it?": "எவ்வளவு தொந்தரவு?",
    "How much is it troubling you, from 1 to 10?":
        "1 முதல் 10 வரை, இது உங்களை எவ்வளவு தொந்தரவு செய்கிறது?",
    "Is anything else happening as well?": "இதனுடன் வேறு ஏதாவது நடக்கிறதா?",
    "Only choose what you actually feel.":
        "உங்களுக்கு உண்மையில் உள்ளதை மட்டும் தேர்ந்தெடுங்கள்.",
    "Have you taken anything for it?": "இதற்காக நீங்கள் ஏதாவது எடுத்துக்கொண்டீர்களா?",
    "Any medicine or home remedy, even if it did not help.":
        "எந்த மருந்தும் அல்லது வீட்டு வைத்தியமும், பயன் தராவிட்டாலும்.",
    "Anything changed?": "ஏதாவது மாறியுள்ளதா?",
    "Have your regular medicines changed since your last visit?":
        "கடந்த வருகைக்குப் பிறகு உங்கள் வழக்கமான மருந்துகள் மாறியுள்ளதா?",
    "We already have your earlier list — only tell us what changed.":
        "உங்கள் முந்தைய பட்டியல் எங்களிடம் உள்ளது — என்ன மாறியது என்பதை மட்டும் சொல்லுங்கள்.",
    "What has changed?": "என்ன மாறியுள்ளது?",
    "A medicine you started, stopped, or now take differently.":
        "நீங்கள் தொடங்கிய, நிறுத்திய, அல்லது இப்போது வேறு விதமாக எடுக்கும் மருந்து.",
    "Has a doctor told you about any new condition since then?":
        "அதற்குப் பிறகு ஏதாவது புதிய நோய் பற்றி மருத்துவர் சொன்னாரா?",
    "Only something new.": "புதிதாக இருந்தால் மட்டும்.",
    "What was it?": "அது என்ன?",
    "This is your space.": "இது உங்கள் இடம்.",
    "Anything else you want the doctor to know today?":
        "இன்று மருத்துவர் அறிய வேண்டியது வேறு ஏதாவது உள்ளதா?",
    "Only here for a check-up": "பரிசோதனைக்காக மட்டும் வந்தேன்",
    "Hospital visit": "மருத்துவமனை வருகை",

    # --- AYUSH: Dashavidha ----------------------------------------------
    "Ten-fold examination": "தசவித பரீக்ஷை",
    "Dashavidha Pariksha — questions about your constitution.":
        "தசவித பரீக்ஷை — உங்கள் உடல் இயல்பு பற்றிய கேள்விகள்.",
    "Prakriti": "பிரகிருதி",
    "Which best describes your natural build and temperament?":
        "உங்கள் இயற்கையான உடலமைப்பையும் இயல்பையும் எது சிறப்பாக விவரிக்கிறது?",
    "Your lifelong tendency, not how you feel today.":
        "உங்கள் வாழ்நாள் இயல்பு, இன்றைய நிலை அல்ல.",
    "Vikriti": "விகிருதி",
    "How do you feel compared with your usual self?":
        "உங்கள் வழக்கமான நிலையுடன் ஒப்பிட்டால் இப்போது எப்படி உணர்கிறீர்கள்?",
    "Your current state, today.": "உங்கள் இன்றைய தற்போதைய நிலை.",
    "Sara": "சாரம்",
    "How would you describe your overall vitality?":
        "உங்கள் ஒட்டுமொத்த உடல் வலிமையை எப்படி விவரிப்பீர்கள்?",
    "How strong and resilient you generally feel.":
        "பொதுவாக நீங்கள் எவ்வளவு வலிமையாகவும் தாங்கும் திறனுடனும் உணர்கிறீர்கள்.",
    "Samhanana": "சம்ஹனனம்",
    "How is your body build?": "உங்கள் உடலமைப்பு எப்படி உள்ளது?",
    "Muscle and frame, in your own view.":
        "தசைகளும் உடற்கட்டும், உங்கள் பார்வையில்.",
    "Pramana": "பிரமாணம்",
    "How would you describe your height and weight together?":
        "உங்கள் உயரத்தையும் எடையையும் ஒன்றாகப் பார்த்தால் எப்படி விவரிப்பீர்கள்?",
    "Roughly proportionate, or not.": "தோராயமாகச் சமமாக, அல்லது இல்லை.",
    "Satmya": "சாத்மியம்",
    "Which foods or conditions suit you well?":
        "எந்த உணவுகள் அல்லது சூழல்கள் உங்களுக்கு நன்றாகப் பொருந்துகின்றன?",
    "What you tolerate easily.": "நீங்கள் எளிதாகத் தாங்கிக்கொள்வது.",
    "Sattva": "சத்வம்",
    "How do you usually handle stress?": "மன அழுத்தத்தை நீங்கள் பொதுவாக எப்படிச் சமாளிக்கிறீர்கள்?",
    "Your mental steadiness.": "உங்கள் மன உறுதி.",
    "Ahara Shakti": "ஆஹார சக்தி",
    "How is your appetite and digestion?": "உங்கள் பசியும் செரிமானமும் எப்படி உள்ளது?",
    "How much you can eat and digest comfortably.":
        "நீங்கள் எவ்வளவு எளிதாக உண்ணவும் செரிக்கவும் முடிகிறது.",
    "Vyayama Shakti": "வியாயாம சக்தி",
    "How much physical exertion can you manage?":
        "எவ்வளவு உடல் உழைப்பை நீங்கள் தாங்க முடியும்?",
    "Before you need to rest.": "ஓய்வு தேவைப்படுவதற்கு முன்.",
    "Vaya": "வயம்",
    "Which life stage are you in?": "நீங்கள் வாழ்க்கையின் எந்தப் பகுதியில் உள்ளீர்கள்?",

    # --- AYUSH: Ashtasthana ----------------------------------------------
    "Eight-fold examination": "அஷ்டஸ்தான பரீக்ஷை",
    "Ashtasthana Pariksha — your practitioner will confirm each of these.":
        "அஷ்டஸ்தான பரீக்ஷை — இவை ஒவ்வொன்றையும் உங்கள் மருத்துவர் உறுதிப்படுத்துவார்.",
    "Only what you notice yourself.": "நீங்களே உணர்வதை மட்டும்.",
    "Your own sense of it — a practitioner will check properly.":
        "இதைப் பற்றி உங்கள் சொந்த உணர்வு — மருத்துவர் முறையாகப் பரிசோதிப்பார்.",
    "Nadi": "நாடி",
    "How does your pulse or heartbeat usually feel?":
        "உங்கள் நாடி அல்லது இதயத் துடிப்பு பொதுவாக எப்படி உணரப்படுகிறது?",
    "Mutra": "மூத்திரம்",
    "How is your urine?": "உங்கள் சிறுநீர் எப்படி உள்ளது?",
    "Colour, quantity and how often.": "நிறம், அளவு மற்றும் எத்தனை முறை.",
    "Mala": "மலம்",
    "How are your bowel movements?": "உங்கள் மலம் கழிதல் எப்படி உள்ளது?",
    "Regularity and consistency.": "ஒழுங்கும் இறுக்கமும்.",
    "Jihva": "ஜிஹ்வை",
    "How does your tongue look and feel?":
        "உங்கள் நாக்கு எப்படித் தெரிகிறது, எப்படி உணரப்படுகிறது?",
    "Coating, dryness or taste in the mouth.":
        "நாக்கின் மேல் படலம், வறட்சி அல்லது வாயின் சுவை.",
    "Shabda": "சப்தம்",
    "How is your voice at present?": "உங்கள் குரல் இப்போது எப்படி உள்ளது?",
    "Strength and clarity when you speak.": "பேசும்போது வலிமையும் தெளிவும்.",
    "Sparsha": "ஸ்பர்சம்",
    "How does your skin feel to touch?": "உங்கள் தோல் தொடும்போது எப்படி உணரப்படுகிறது?",
    "Temperature, dryness or sweating.": "வெப்பம், வறட்சி அல்லது வியர்வை.",
    "Drik": "திருஷ்டி",
    "How are your eyes and vision?": "உங்கள் கண்களும் பார்வையும் எப்படி உள்ளது?",
    "Akriti": "ஆகிருதி",
    "How would you describe your overall appearance now?":
        "உங்கள் ஒட்டுமொத்தத் தோற்றத்தை இப்போது எப்படி விவரிப்பீர்கள்?",
    "How you look and feel compared with your usual self.":
        "உங்கள் வழக்கமான நிலையுடன் ஒப்பிட்டால் நீங்கள் எப்படித் தெரிகிறீர்கள், "
        "எப்படி உணர்கிறீர்கள்.",

    # --- AYUSH: lifestyle -------------------------------------------------
    "Digestion, sleep and routine": "செரிமானம், தூக்கம் மற்றும் அன்றாட வழக்கம்",
    "Agni, Nidra, Ahara and Vihara — how you eat, sleep and live.":
        "அக்னி, நித்திரை, ஆஹாரம் மற்றும் விஹாரம் — நீங்கள் எப்படி உண்கிறீர்கள், "
        "உறங்குகிறீர்கள், வாழ்கிறீர்கள்.",
    "Agni": "அக்னி",
    "How well do you digest your food?": "உங்கள் உணவு எவ்வளவு நன்றாகச் செரிக்கிறது?",
    "Whether food feels heavy, or digests comfortably.":
        "உணவு கனமாக இருக்கிறதா, அல்லது எளிதாகச் செரிக்கிறதா.",
    "Koshtha": "கோஷ்டம்",
    "How does your gut normally behave?": "உங்கள் வயிறு பொதுவாக எப்படி இருக்கிறது?",
    "Nidra": "நித்திரை",
    "How is your sleep?": "உங்கள் தூக்கம் எப்படி உள்ளது?",
    "Falling asleep, staying asleep, and feeling rested.":
        "தூக்கம் வருவது, நீடிப்பது, மற்றும் ஓய்வு கிடைத்ததாக உணர்வது.",
    "Manas": "மனஸ்",
    "How has your mind felt lately?": "சமீபத்தில் உங்கள் மனம் எப்படி இருந்தது?",
    "Only if you wish to say. This is recorded for your practitioner, not assessed here.":
        "நீங்கள் சொல்ல விரும்பினால் மட்டும். இது உங்கள் மருத்துவருக்காகப் "
        "பதிவு செய்யப்படுகிறது, இங்கே மதிப்பிடப்படுவதில்லை.",
    "And your daily routine?": "உங்கள் அன்றாட வழக்கம்?",
    "Which of these describe your diet?":
        "இவற்றில் எது உங்கள் உணவு முறையை விவரிக்கிறது?",
    "Ayurveda assessment": "ஆயுர்வேத மதிப்பீடு",
    "Your usual tendency, not just today.": "உங்கள் வழக்கமான இயல்பு, இன்று மட்டும் அல்ல.",
    "These optional questions are used in Ayurvedic practice. They describe your "
    "constitution and routine — they are not a diagnosis, and you can skip any of them.":
        "இந்த விருப்பக் கேள்விகள் ஆயுர்வேத மருத்துவ முறையில் பயன்படுகின்றன. இவை உங்கள் "
        "உடல் இயல்பையும் அன்றாட வழக்கத்தையும் விவரிக்கின்றன — இவை நோய் கண்டறிதல் அல்ல, "
        "இவற்றில் எதையும் நீங்கள் தவிர்க்கலாம்.",

    # --- Structured history section names --------------------------------
    "Chief complaint": "முதன்மைக் குறை",
    "History of present illness": "தற்போதைய நோயின் வரலாறு",
    "Past medical history": "முந்தைய மருத்துவ வரலாறு",
    "Past surgical history": "முந்தைய அறுவை சிகிச்சை வரலாறு",
    "Medications": "மருந்துகள்",
    "Current medications": "தற்போதைய மருந்துகள்",
    "Drug history": "மருந்து வரலாறு",
    "Personal history": "தனிப்பட்ட வரலாறு",
    "Previous investigations": "முந்தைய பரிசோதனைகள்",
    "Review of systems": "உடல் அமைப்புகளின் பரிசோதனை",
    "Additional information": "கூடுதல் தகவல்",
    "None reported": "எதுவும் தெரிவிக்கப்படவில்லை",
    "Regarding this problem": "இந்தப் பிரச்சினை பற்றி",
    "Also reports": "இதையும் தெரிவித்தார்",

    # --- Narratives -------------------------------------------------------
    "The patient": "நோயாளி",
    "{age}-year-old": "{age} வயது",
    "no specific complaint": "குறிப்பிட்ட குறை இல்லை",
    "an unspecified concern": "தெளிவற்ற குறை",
    "{subject} reports: {complaint}.": "{subject} தெரிவிக்கும் குறை: {complaint}.",
    "{subject} presents reporting: {complaint}.":
        "{subject} தெரிவிக்கும் குறை: {complaint}.",
    "{subject} returns reporting: {complaint}.":
        "{subject} மீண்டும் வந்துள்ளார், குறை: {complaint}.",
    "{lead}: {found}.": "{lead}: {found}.",
    "{lead}: none reported.": "{lead}: எதுவும் தெரிவிக்கப்படவில்லை.",
    "About this problem today: {items}.": "இன்று இந்தப் பிரச்சினை பற்றி: {items}.",
    "Severity reported by the patient: {value}.":
        "நோயாளி தெரிவித்த தீவிரம்: {value}.",
    "No further detail was given about the problem.":
        "பிரச்சினை பற்றி இதற்கு மேல் விவரம் தரப்படவில்லை.",
    "Also reported today: {items}.": "இன்று இதையும் தெரிவித்தார்: {items}.",
    "Known conditions from earlier visits: {items}.":
        "முந்தைய வருகைகளிலிருந்து அறியப்பட்ட நோய்கள்: {items}.",
    "Medications on record: {items}.": "பதிவில் உள்ள மருந்துகள்: {items}.",
    "Allergies on record: {items}.": "பதிவில் உள்ள ஒவ்வாமைகள்: {items}.",
    "No allergies recorded.": "எந்த ஒவ்வாமையும் பதிவு செய்யப்படவில்லை.",
    "Medication changes reported today: {items}.":
        "இன்று தெரிவிக்கப்பட்ட மருந்து மாற்றங்கள்: {items}.",
    "New conditions reported today: {items}.":
        "இன்று தெரிவிக்கப்பட்ட புதிய நோய்கள்: {items}.",
    "This visit has been marked urgent because some described symptoms may require "
    "prompt attention.":
        "தெரிவிக்கப்பட்ட சில அறிகுறிகளுக்கு விரைவான கவனம் தேவைப்படலாம் என்பதால், "
        "இந்த வருகை அவசரம் எனக் குறிக்கப்பட்டுள்ளது.",
    "Recorded from the patient's own account and their existing records. "
    "This is not a diagnosis.":
        "நோயாளி தானே தெரிவித்தபடியும், அவரது ஏற்கெனவே உள்ள பதிவுகளிலிருந்தும் "
        "பதிவு செய்யப்பட்டது. இது நோய் கண்டறிதல் அல்ல.",
    "This is a record of information provided by the patient and read from their "
    "documents. It is not a diagnosis.":
        "இது நோயாளி அளித்த, மற்றும் அவரது ஆவணங்களிலிருந்து படிக்கப்பட்ட தகவலின் "
        "பதிவு. இது நோய் கண்டறிதல் அல்ல.",
    "This records what you told us today alongside what we already knew. It is not a "
    "diagnosis, and a healthcare professional will review it with you.":
        "இன்று நீங்கள் சொன்னதையும், எங்களுக்கு ஏற்கெனவே தெரிந்திருந்ததையும் இது "
        "பதிவு செய்கிறது. இது நோய் கண்டறிதல் அல்ல; ஒரு மருத்துவப் பணியாளர் "
        "உங்களுடன் இதைப் பார்ப்பார்.",

    # --- Gender and care-system labels used in prose ----------------------
    "male": "ஆண்",
    "female": "பெண்",
    "other": "மற்றவை",
    "gender not stated": "பாலினம் தெரிவிக்கப்படவில்லை",
    "not decided yet": "இன்னும் தீர்மானிக்கப்படவில்லை",

    # --- Demo patients ----------------------------------------------------
    "Rajesh Kumar · 52": "ராஜேஷ் குமார் · 52",
    "Returning patient, comfortable with digital forms. Standard mode.":
        "மீண்டும் வரும் நோயாளி, டிஜிட்டல் படிவங்களில் வசதியாக உள்ளார். நிலையான முறை.",
    "Kamla Devi · 71": "கமலா தேவி · 71",
    "Prefers a simpler experience. Easy mode with audio guidance.":
        "எளிமையான முறையை விரும்புகிறார். ஒலி வழிகாட்டுதலுடன் எளிய முறை.",
    "Anil Sharma · 45": "அனில் ஷர்மா · 45",
    "Low vision. Extra-large text and high contrast.":
        "பார்வை குறைவு. மிகப் பெரிய எழுத்தும் அதிக நிற வேறுபாடும்.",
    "Sunita Devi · 34": "சுனிதா தேவி · 34",
    "First-time patient who stopped part-way through onboarding.":
        "முதல் முறை வரும் நோயாளி, பதிவை பாதியில் நிறுத்தியவர்.",
    "e.g. three days, worse on walking": "எ.கா. மூன்று நாட்கள், நடக்கும்போது அதிகம்",
    "e.g. very tired, losing weight": "எ.கா. மிகுந்த சோர்வு, எடை குறைதல்",
}
