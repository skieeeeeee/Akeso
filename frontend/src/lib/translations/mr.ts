/**
 * Marathi translations, keyed by the English source string.
 *
 * MACHINE-AUTHORED — pending review by a Marathi speaker. Add or correct an
 * entry by editing this file; nothing else needs to change. An explicit `mr`
 * key in `STRINGS` always overrides an entry here.
 *
 * Terminology matches the server overlay (`backend/app/shared/translations/
 * mr.py`): रुग्ण (patient), आजार (illness), औषध (medicine), भेट (visit),
 * तक्रार (complaint), निदान (diagnosis), संमती (consent).
 */
export const MARATHI: Record<string, string> = {
  "about": "सुमारे",
  // --- Landing statistics --------------------------------------------------
  "minutes": "मिनिटे",
  "the average primary-care consultation in India":
    "भारतातील प्राथमिक आरोग्य सल्ल्याचा सरासरी कालावधी",
  "Among the shortest measured anywhere. Almost all of it goes on collecting a history the clinic could already have had.":
    "जगात मोजल्या गेलेल्यांपैकी सर्वात कमी. त्यातील जवळपास सर्व वेळ दवाखान्याकडे आधीच असू शकणारा इतिहास गोळा करण्यात जातो.",
  "million": "दशलक्ष",
  "people in India live with diabetes": "भारतात मधुमेह असलेले लोक",
  "A further 136 million are prediabetic — a group early detection actually changes.":
    "आणखी १३६ दशलक्ष लोक पूर्वमधुमेही आहेत — ज्यांच्यासाठी लवकर निदान खरोखर फरक घडवते.",
  "adults live with hypertension": "उच्च रक्तदाब असलेले प्रौढ",
  "Only a small fraction have it under control, and many do not know they have it.":
    "फार थोड्यांचाच रक्तदाब आटोक्यात आहे, आणि अनेकांना तो आहे हेच माहीत नाही.",
  "%": "%",
  "of deaths in India are from NCDs":
    "भारतातील मृत्यू असंसर्गजन्य आजारांमुळे",
  "Non-communicable disease — the category where a timely history and follow-up matter most.":
    "असंसर्गजन्य आजार — जिथे वेळेवर मिळालेला इतिहास आणि पाठपुरावा सर्वाधिक महत्त्वाचा ठरतो.",
  "of health spending is out of pocket": "आरोग्य खर्च जो स्वतःच्या खिशातून होतो",
  "Which is why a repeated test or a lost prescription is not a small inconvenience.":
    "म्हणूनच पुन्हा करावी लागणारी तपासणी किंवा हरवलेली औषधाची चिठ्ठी ही छोटी गैरसोय नसते.",

  // --- App identity and common actions ---------------------------------
  "MediKiosk": "मेडीकियोस्क",
  "Share your health information before your visit":
    "तुमच्या भेटीपूर्वी तुमची आरोग्य माहिती सामायिक करा",
  "Continue": "पुढे जा",
  "Back": "मागे",
  "Cancel": "रद्द करा",
  "Save": "सेव्ह करा",
  "Saving…": "सेव्ह होत आहे…",
  "Saved": "सेव्ह झाले",
  "Try again": "पुन्हा प्रयत्न करा",
  "Loading…": "लोड होत आहे…",
  "Skip for now": "आता वगळा",
  "Yes": "होय",
  "No": "नाही",
  "Optional": "ऐच्छिक",
  "Add": "जोडा",
  "Remove": "काढा",
  "Change": "बदला",
  "Done": "पूर्ण",
  "Close": "बंद करा",
  "Sign out": "साइन आउट",
  "Not provided": "दिलेले नाही",
  "Finish": "समाप्त करा",
  "Start": "सुरू करा",
  "Stop": "थांबा",
  "Preview": "पूर्वावलोकन",
  "Section": "विभाग",
  "Question": "प्रश्न",
  "of": "पैकी",
  "Part": "भाग",
  "About": "बद्दल",
  "Why": "का",
  "years": "वर्षे",
  "added": "जोडले",
  "Sent": "पाठवले",
  "Language": "भाषा",
  "Languages": "भाषा",
  "Settings": "सेटिंग",
  "Records": "नोंदी",
  "Visits": "भेटी",
  "Consent": "संमती",
  "Gender": "लिंग",
  "Age": "वय",
  "View all": "सर्व पहा",

  // --- Landing / welcome -----------------------------------------------
  "Tell us about your health before you see the doctor":
    "डॉक्टरांना भेटण्यापूर्वी तुमच्या आरोग्याबद्दल सांगा",
  "Answer a few simple questions here. Your doctor sees your history before you walk in, so your visit is about you — not about filling forms.":
    "येथे काही सोपे प्रश्न सोडवा. तुम्ही आत येण्यापूर्वीच डॉक्टरांना तुमचा इतिहास दिसतो, म्हणून तुमची भेट तुमच्याबद्दल असते — फॉर्म भरण्याबद्दल नाही.",
  "I have used MediKiosk before": "मी यापूर्वी मेडीकियोस्क वापरले आहे",
  "Choose your language": "तुमची भाषा निवडा",
  "Make text bigger": "मजकूर मोठा करा",
  "How it works": "हे कसे चालते",
  "Sign in with your mobile": "तुमच्या मोबाइलने साइन इन करा",
  "We send a one-time code. No password to remember.":
    "आम्ही एक-वेळ कोड पाठवतो. पासवर्ड लक्षात ठेवायची गरज नाही.",
  "Answer simple questions": "सोपे प्रश्न सोडवा",
  "Speak or tap — whichever is easier for you.":
    "बोला किंवा स्पर्श करा — तुम्हाला जे सोपे वाटेल.",
  "Your doctor is ready": "तुमचे डॉक्टर तयार आहेत",
  "Your history is waiting for them, so nothing gets repeated.":
    "तुमचा इतिहास त्यांच्यासाठी तयार असतो, म्हणून काहीही पुन्हा सांगावे लागत नाही.",
  "You choose what to share. You can withdraw your consent at any time.":
    "काय सामायिक करायचे ते तुम्ही ठरवता. तुमची संमती तुम्ही कधीही मागे घेऊ शकता.",

  // --- Sign in ----------------------------------------------------------
  "Sign in": "साइन इन",
  "Enter your mobile number and we will send a one-time code.":
    "तुमचा मोबाइल क्रमांक टाका आणि आम्ही एक-वेळ कोड पाठवू.",
  "Mobile number": "मोबाइल क्रमांक",
  "10-digit number, for example 98765 43210":
    "१० अंकी क्रमांक, उदाहरणार्थ ९८७६५ ४३२१०",
  "Send code": "कोड पाठवा",
  "Sending…": "पाठवत आहे…",
  "One-time code": "एक-वेळ कोड",
  "6 digits": "६ अंक",
  "Verify and continue": "पडताळा आणि पुढे जा",
  "Verifying…": "पडताळणी होत आहे…",
  "Send a new code": "नवीन कोड पाठवा",
  "Use a different number": "वेगळा क्रमांक वापरा",
  "Code sent to": "कोड पाठवला",
  "Prototype": "प्रारूप",
  "This demonstration does not send SMS. Use the code shown below.":
    "हे प्रात्यक्षिक एसएमएस पाठवत नाही. खाली दाखवलेला कोड वापरा.",
  "Or explore with a demo patient": "किंवा डेमो रुग्णासह पाहा",
  "Demo patient": "डेमो रुग्ण",
  "Fictional records for demonstration. No real patient data.":
    "प्रात्यक्षिकासाठी काल्पनिक नोंदी. खऱ्या रुग्णाची माहिती नाही.",
  "Demo patients are not loaded on this server yet.":
    "या सर्व्हरवर डेमो रुग्ण अजून लोड केलेले नाहीत.",
  "Log in": "लॉग इन",
  "Register": "नोंदणी करा",

  // --- ABHA / health ID -------------------------------------------------
  "Connect your health ID": "तुमचा हेल्थ आयडी जोडा",
  "If you have an ABHA number, connecting it keeps your records together between visits.":
    "तुमच्याकडे आभा क्रमांक असेल, तर तो जोडल्याने तुमच्या नोंदी भेटींदरम्यान एकत्र राहतात.",
  "ABHA number or address": "आभा क्रमांक किंवा पत्ता",
  "14 digits, or an address like name@abdm": "१४ अंक, किंवा name@abdm सारखा पत्ता",
  "Connect": "जोडा",
  "Checking…": "तपासत आहे…",
  "I do not have one": "माझ्याकडे नाही",
  "Prototype: this checks the number's format locally. It is not connected to the national ABDM network.":
    "प्रारूप: हे क्रमांकाचे स्वरूप स्थानिक पातळीवर तपासते. ते राष्ट्रीय ABDM नेटवर्कशी जोडलेले नाही.",
  "Health ID connected": "हेल्थ आयडी जोडला",
  "Why connect it?": "तो का जोडावा?",
  "Your history follows you, so you never start from scratch at your next visit. You can also continue without it.":
    "तुमचा इतिहास तुमच्यासोबत राहतो, म्हणून पुढच्या भेटीत नव्याने सुरुवात करावी लागत नाही. तुम्ही याशिवायही पुढे जाऊ शकता.",
  "Health ID": "हेल्थ आयडी",

  // --- Personal details -------------------------------------------------
  "Your details": "तुमची माहिती",
  "This helps the hospital identify you correctly.":
    "यामुळे रुग्णालयाला तुमची ओळख बरोबर पटते.",
  "Full name": "पूर्ण नाव",
  "As written on your ID": "तुमच्या ओळखपत्रावर लिहिल्याप्रमाणे",
  "Date of birth": "जन्मतारीख",
  "We use this to work out your age": "यावरून आम्ही तुमचे वय काढतो",
  "Male": "पुरुष",
  "Female": "स्त्री",
  "Other": "इतर",
  "Prefer not to say": "सांगायचे नाही",
  "Preferred language": "पसंतीची भाषा",
  "Emergency contact": "आपत्कालीन संपर्क",
  "Someone the hospital can call if needed.":
    "गरज पडल्यास रुग्णालय ज्यांना फोन करू शकेल अशी व्यक्ती.",
  "Their name": "त्यांचे नाव",
  "Their mobile number": "त्यांचा मोबाइल क्रमांक",
  "Relationship to you": "तुमच्याशी नाते",
  "For example: spouse, son, neighbour": "उदाहरणार्थ: जोडीदार, मुलगा, शेजारी",

  // --- Accessibility assessment ----------------------------------------
  "Let us set this up for you": "तुमच्यासाठी हे सेट करू या",
  "A few quick questions so the screens suit you. There are no wrong answers, and you can change everything later.":
    "स्क्रीन तुम्हाला सोयीच्या होण्यासाठी काही झटपट प्रश्न. कोणतेही उत्तर चुकीचे नाही, आणि तुम्ही नंतर सर्व बदलू शकता.",
  "Why we ask": "आम्ही का विचारतो",
  "Your answers only change how this app looks and sounds. They are not medical questions and are never shared as a diagnosis.":
    "तुमची उत्तरे केवळ हे ॲप कसे दिसते आणि कसे ऐकू येते तेच बदलतात. हे वैद्यकीय प्रश्न नाहीत आणि निदान म्हणून कधीही सामायिक केले जात नाहीत.",
  "Choose an option to continue": "पुढे जाण्यासाठी एक पर्याय निवडा",
  "We have set this up for you": "आम्ही तुमच्यासाठी हे सेट केले आहे",
  "Based on your answers. Change anything you like — now or later.":
    "तुमच्या उत्तरांवर आधारित. तुम्हाला हवे ते बदला — आता किंवा नंतर.",
  "This looks good": "हे ठीक वाटते",
  "Change these settings": "ही सेटिंग बदला",
  "Applying…": "लागू करत आहे…",
  "Your experience": "तुमचा अनुभव",
  "Screen style": "स्क्रीनची शैली",
  "Text size": "मजकुराचा आकार",
  "Colours": "रंग",
  "Read questions aloud": "प्रश्न मोठ्याने वाचा",
  "We will speak each question. You can turn this off any time.":
    "आम्ही प्रत्येक प्रश्न बोलून सांगू. तुम्ही हे कधीही बंद करू शकता.",
  "How you answer": "तुम्ही उत्तर कसे देता",
  "This is how text will look on your screens.":
    "तुमच्या स्क्रीनवर मजकूर असा दिसेल.",
  "You are never locked into a setting. Change it from your profile whenever you want.":
    "कोणतीही सेटिंग कायमची नसते. तुम्हाला हवे तेव्हा प्रोफाइलमधून बदला.",
  "Retake the comfort check": "सुविधा तपासणी पुन्हा करा",
  "Optional. We will suggest settings again based on your answers.":
    "ऐच्छिक. तुमच्या उत्तरांवरून आम्ही पुन्हा सेटिंग सुचवू.",
  "Change how MediKiosk looks and sounds. Your answers are not affected.":
    "मेडीकियोस्क कसे दिसते आणि कसे ऐकू येते ते बदला. तुमच्या उत्तरांवर परिणाम होत नाही.",
  "Settings saved": "सेटिंग सेव्ह झाली",

  // --- Consent ----------------------------------------------------------
  "Your consent": "तुमची संमती",
  "I agree": "मी सहमत आहे",
  "I do not agree": "मी सहमत नाही",
  "Needed to continue": "पुढे जाण्यासाठी आवश्यक",
  "Your choice": "तुमची निवड",
  "What we collect": "आम्ही काय गोळा करतो",
  "How it is used": "ते कसे वापरले जाते",
  "Without this we cannot collect your health information. You can still see your doctor as usual — you would just fill the form there instead.":
    "याशिवाय आम्ही तुमची आरोग्य माहिती गोळा करू शकत नाही. तुम्ही नेहमीप्रमाणे डॉक्टरांना भेटू शकता — फक्त फॉर्म तिथे भरावा लागेल.",
  "Listen to this": "हे ऐका",

  // --- Medical history form ---------------------------------------------
  "Your health history": "तुमचा आरोग्य इतिहास",
  "Tell us once. Next time you only describe what is new.":
    "एकदा सांगा. पुढच्या वेळी फक्त नवीन काय आहे तेच सांगा.",
  "Type here and press Add": "येथे लिहा आणि जोडा दाबा",
  "Nothing to add": "जोडण्यासारखे काही नाही",
  "Common answers": "सामान्य उत्तरे",
  "Health history": "आरोग्य इतिहास",

  // --- Documents ---------------------------------------------------------
  "Previous medical records": "पूर्वीच्या वैद्यकीय नोंदी",
  "Add a photo of a prescription, lab report or discharge summary. This is optional.":
    "औषधाची चिठ्ठी, तपासणी अहवाल किंवा डिस्चार्ज सारांशाचा फोटो जोडा. हे ऐच्छिक आहे.",
  "Choose a photo or PDF": "फोटो किंवा पीडीएफ निवडा",
  "Uploading…": "अपलोड होत आहे…",
  "What is this?": "हे काय आहे?",
  "Short description": "थोडक्यात वर्णन",
  "For example: Dr Mehta, March 2026": "उदाहरणार्थ: डॉ. मेहता, मार्च २०२६",
  "No records added": "कोणतीही नोंद जोडलेली नाही",
  "You can add records now or later from your profile. Your doctor can see them either way.":
    "तुम्ही नोंदी आता किंवा नंतर प्रोफाइलमधून जोडू शकता. दोन्ही प्रकारे तुमच्या डॉक्टरांना ते दिसते.",
  "Your records are saved and shown to your doctor as you uploaded them.":
    "तुमच्या नोंदी सेव्ह होतात आणि तुम्ही अपलोड केल्याप्रमाणेच डॉक्टरांना दाखवल्या जातात.",
  "Prescription": "औषधाची चिठ्ठी",
  "Lab report": "तपासणी अहवाल",
  "Discharge summary": "डिस्चार्ज सारांश",
  "Something else": "इतर काही",
  "Reading your document…": "तुमचे कागदपत्र वाचत आहे…",
  "Read this document": "हे कागदपत्र वाचा",
  "Try reading again": "पुन्हा वाचण्याचा प्रयत्न करा",
  "Information found in this document": "या कागदपत्रात मिळालेली माहिती",
  "This is what the document appears to say. It is not a diagnosis — please check it and tell us if anything looks wrong.":
    "कागदपत्रात असे लिहिलेले दिसते. हे निदान नाही — कृपया ते तपासा आणि काही चुकीचे वाटले तर सांगा.",
  "That is correct": "ते बरोबर आहे",
  "That is not right": "ते बरोबर नाही",
  "Confirmed by you": "तुम्ही पुष्टी केली",
  "You marked this wrong": "तुम्ही हे चुकीचे म्हणून खुणावले",
  "Show the text we read": "आम्ही वाचलेला मजकूर दाखवा",
  "We read the text but did not recognise any medical details. Your doctor can still read the document.":
    "आम्ही मजकूर वाचला पण वैद्यकीय तपशील ओळखू शकलो नाही. तुमचे डॉक्टर हे कागदपत्र वाचू शकतात.",
  "Within the printed range": "छापील मर्यादेच्या आत",
  "Below the printed range": "छापील मर्यादेपेक्षा कमी",
  "Above the printed range": "छापील मर्यादेपेक्षा जास्त",
  "Could not be compared": "तुलना करता आली नाही",
  "Values are compared only against the range printed on your report. A healthcare professional should review them.":
    "मूल्यांची तुलना केवळ तुमच्या अहवालावर छापलेल्या मर्यादेशी केली जाते. आरोग्य व्यावसायिकाने ती तपासावी.",

  // --- Timeline ----------------------------------------------------------
  "Your medical timeline": "तुमचा वैद्यकीय कालपट",
  "Everything we know about, newest first.":
    "आम्हाला माहीत असलेले सर्व, नवीनतम प्रथम.",
  "Nothing here yet": "येथे अजून काही नाही",
  "Once you answer questions or add a record, it will appear here.":
    "तुम्ही प्रश्नांची उत्तरे दिली किंवा नोंद जोडली, की ते येथे दिसेल.",
  "Everything": "सर्व",
  "Needs your check": "तुमच्या तपासणीची गरज",
  "No date on record": "नोंदीत तारीख नाही",

  // --- Review ------------------------------------------------------------
  "Check your information": "तुमची माहिती तपासा",
  "Please look through this before we finish. You can change anything.":
    "आपण संपवण्यापूर्वी कृपया हे पाहा. तुम्ही काहीही बदलू शकता.",
  "You told us": "तुम्ही सांगितले",
  "From your documents": "तुमच्या कागदपत्रांतून",
  "Still missing": "अजून बाकी",
  "These are usually useful for your doctor. You can add them now or later.":
    "हे सामान्यतः तुमच्या डॉक्टरांसाठी उपयुक्त असते. तुम्ही ते आता किंवा नंतर जोडू शकता.",
  "Summary for your doctor": "तुमच्या डॉक्टरांसाठी सारांश",
  "This is correct — finish": "हे बरोबर आहे — समाप्त करा",
  "Change this": "हे बदला",
  "You said this": "तुम्ही हे सांगितले",
  "Found in a document": "कागदपत्रात मिळाले",
  "Nothing recorded": "काही नोंदवलेले नाही",

  // --- Profile / completion ---------------------------------------------
  "You are all set": "सर्व तयार आहे",
  "Your health profile is saved. Show this screen at the reception desk.":
    "तुमची आरोग्य प्रोफाइल सेव्ह झाली. ही स्क्रीन स्वागत कक्षात दाखवा.",
  "View my profile": "माझी प्रोफाइल पहा",
  "Your health profile": "तुमची आरोग्य प्रोफाइल",
  "No visits recorded yet": "अजून कोणतीही भेट नोंदवलेली नाही",
  "Finish setting up": "सेट करणे पूर्ण करा",
  "Your profile is not finished yet. Complete it so your doctor has your full history.":
    "तुमची प्रोफाइल अजून पूर्ण झालेली नाही. डॉक्टरांकडे तुमचा संपूर्ण इतिहास असावा म्हणून ती पूर्ण करा.",
  "items recorded": "नोंदी दाखल",
  "At your next visit you will only be asked what has changed.":
    "पुढच्या भेटीत तुम्हाला फक्त काय बदलले तेच विचारले जाईल.",

  // --- Voice --------------------------------------------------------------
  "Tap to speak": "बोलण्यासाठी स्पर्श करा",
  "Listening…": "ऐकत आहे…",
  "Working out what you said…": "तुम्ही काय सांगितले ते समजून घेत आहे…",
  "We heard": "आम्ही ऐकले",
  "That is right": "ते बरोबर आहे",
  "Say it again": "पुन्हा सांगा",
  "Type instead": "त्याऐवजी लिहा",
  "Recording…": "रेकॉर्ड होत आहे…",
  "Voice input problem": "आवाजाच्या इनपुटमध्ये अडचण",
  "This device has no voice for the selected language, so questions cannot be read aloud. All text stays on screen.":
    "या उपकरणावर निवडलेल्या भाषेसाठी आवाज उपलब्ध नाही, म्हणून प्रश्न मोठ्याने वाचता येत नाहीत. सर्व मजकूर स्क्रीनवर राहतो.",
  "Voice input is not available in this browser, so please type or tap your answers.":
    "या ब्राउझरमध्ये आवाजाचे इनपुट उपलब्ध नाही, म्हणून कृपया तुमची उत्तरे लिहा किंवा स्पर्श करून द्या.",

  // --- Interview ----------------------------------------------------------
  "We will ask a few questions, one at a time. Speak or tap — whichever is easier.":
    "आम्ही एका वेळी एक असे काही प्रश्न विचारू. बोला किंवा स्पर्श करा — जे सोपे असेल.",
  "Continue where you left off": "जिथे थांबले तिथून पुढे जा",
  "Follow-up question": "पुढील प्रश्न",
  "Smart assistance is unavailable right now, so we are using our standard questions. Nothing you have answered is lost.":
    "स्मार्ट सहाय्य सध्या उपलब्ध नाही, म्हणून आम्ही आमचे नेहमीचे प्रश्न वापरत आहोत. तुम्ही दिलेले कोणतेही उत्तर हरवलेले नाही.",
  "That is everything we need": "आम्हाला आवश्यक असलेले सर्व झाले",
  "Next you can add old medical records, or go straight to reviewing what you told us.":
    "पुढे तुम्ही जुन्या वैद्यकीय नोंदी जोडू शकता, किंवा तुम्ही सांगितलेले थेट तपासू शकता.",

  // --- AYUSH ---------------------------------------------------------------
  "Include Ayurveda questions": "आयुर्वेदाचे प्रश्न समाविष्ट करा",
  "Optional. Used at AYUSH facilities to record your constitution and routine.":
    "ऐच्छिक. आयुष केंद्रांमध्ये तुमची प्रकृती आणि दिनचर्या नोंदवण्यासाठी वापरले जाते.",
  "Ayurveda assessment": "आयुर्वेद मूल्यांकन",
  "Skip these questions": "हे प्रश्न वगळा",
  "Include them": "ते समाविष्ट करा",
  "Ten-fold examination": "दशविध परीक्षा",
  "Dashavidha Pariksha — your constitution and current state.":
    "दशविध परीक्षा — तुमची प्रकृती आणि सध्याची स्थिती.",
  "Eight-fold examination": "अष्टस्थान परीक्षा",
  "Ashtasthana Pariksha. You describe what you notice; your practitioner examines and confirms each of these.":
    "अष्टस्थान परीक्षा. तुम्हाला जे जाणवते ते तुम्ही सांगता; तुमचे वैद्य तपासून यांपैकी प्रत्येकाची खात्री करतात.",
  "Digestion, sleep and routine": "पचन, झोप आणि दिनचर्या",
  "Agni, Koshtha, Nidra and Manas.": "अग्नी, कोष्ठ, निद्रा आणि मनस्.",
  "factors recorded": "कारक नोंदवले",
  "Record your constitution, examination findings and routine for an Ayurvedic consultation.":
    "आयुर्वेदिक सल्ल्यासाठी तुमची प्रकृती, परीक्षेचे निष्कर्ष आणि दिनचर्या नोंदवा.",
  "Open assessment": "मूल्यांकन उघडा",
  "These answers are recorded for your practitioner. Nothing here is assessed or interpreted by the app.":
    "ही उत्तरे तुमच्या वैद्यांसाठी नोंदवली जातात. यातील काहीही ॲपकडून तपासले किंवा अर्थ लावले जात नाही.",
  "Type of treatment": "उपचाराचा प्रकार",
  "Modern medicine": "आधुनिक वैद्यकशास्त्र",
  "Ayurveda": "आयुर्वेद",
  "We record which system you chose and ask about your diet and routine. Examination questions specific to this system are not built yet.":
    "तुम्ही कोणती पद्धत निवडली ते आम्ही नोंदवतो आणि तुमच्या आहार व दिनचर्येबद्दल विचारतो. या पद्धतीसाठी खास परीक्षेचे प्रश्न अजून तयार केलेले नाहीत.",
  "Your diet (Ahara)": "तुमचा आहार",
  "Your routine (Vihara)": "तुमचा विहार",
  "Ayurvedic examination you answered": "तुम्ही दिलेली आयुर्वेदिक परीक्षा",
  "{count} of {total} factors recorded": "{total} पैकी {count} कारक नोंदवले",
  "Ayurveda details saved": "आयुर्वेद माहिती सेव्ह झाली",

  // --- Landing page: problem, flow, features -----------------------------
  "Features": "वैशिष्ट्ये",
  "For clinics": "दवाखान्यांसाठी",
  "Kiosk mode": "कियोस्क मोड",
  "Your doctor should already know your history when you walk in":
    "तुम्ही आत येताच तुमच्या डॉक्टरांना तुमचा इतिहास माहीत असावा",
  "MediKiosk collects a patient's medical history before the consultation — by voice, in their own language — so the few minutes with the doctor are spent on the problem, not on paperwork.":
    "मेडीकियोस्क सल्ल्यापूर्वीच रुग्णाचा वैद्यकीय इतिहास गोळा करते — आवाजाने, त्यांच्याच भाषेत — जेणेकरून डॉक्टरांसोबतची थोडी मिनिटे कागदपत्रांवर नाही, तर समस्येवर खर्च होतील.",
  "Try the patient flow": "रुग्णाचा प्रवाह पाहा",
  "See a demo patient": "डेमो रुग्ण पहा",
  "The problem is time": "समस्या वेळेची आहे",
  "A patient repeats their history at every visit. The clinician spends most of a very short consultation writing it down. Both lose, and the record still ends up thin.":
    "रुग्ण प्रत्येक भेटीत आपला इतिहास पुन्हा सांगतो. डॉक्टर अत्यंत थोड्या सल्ला-वेळेचा बहुतांश भाग तो लिहून घेण्यात घालवतात. दोघांचेच नुकसान होते, आणि नोंद तरीही अपुरीच राहते.",
  "Why it matters here": "हे येथे का महत्त्वाचे आहे",
  "Figures are published estimates, shown with their source and year. Please re-check them against the latest release before citing.":
    "आकडे हे प्रकाशित अंदाज आहेत, स्रोत आणि वर्षासह दिलेले. उद्धृत करण्यापूर्वी कृपया ते ताज्या प्रकाशनाशी पुन्हा तपासा.",
  "Illustrative arithmetic": "उदाहरणादाखल गणित",
  "In the": "या",
  "you have spent on this page, a doctor working at India's average pace would have seen about":
    "वेळेत तुम्ही या पानावर घालवला, त्यात भारताच्या सरासरी गतीने काम करणाऱ्या डॉक्टरने सुमारे इतके रुग्ण पाहिले असते",
  "patients.": "रुग्ण.",
  "Derived from the average consultation length, not a live measurement":
    "सरासरी सल्ला-कालावधीवरून काढलेले, प्रत्यक्ष मोजमाप नाही",
  "Before the visit": "भेटीपूर्वी",
  "The patient answers simple questions at a kiosk or on their phone — speaking or tapping, in English or an Indian language.":
    "रुग्ण कियोस्कवर किंवा आपल्या फोनवर सोपे प्रश्न सोडवतो — बोलून किंवा स्पर्श करून, इंग्रजीत किंवा भारतीय भाषेत.",
  "Old records are read": "जुन्या नोंदी वाचल्या जातात",
  "A photo of a prescription or lab report is scanned, and the medicines, diagnoses and test values found in it are listed for the patient to confirm.":
    "औषधाच्या चिठ्ठीचा किंवा तपासणी अहवालाचा फोटो स्कॅन केला जातो, आणि त्यात मिळालेली औषधे, निदाने व तपासणी मूल्ये रुग्णाच्या पुष्टीसाठी दाखवली जातात.",
  "The clinician gets a history": "डॉक्टरांना इतिहास मिळतो",
  "A structured summary, with each fact labelled as reported by the patient, read from a document, or already on record.":
    "एक सुसंगत सारांश, ज्यात प्रत्येक बाब रुग्णाने सांगितलेली, कागदपत्रातून वाचलेली, की आधीच नोंदीत असलेली — असे स्पष्ट लिहिलेले असते.",
  "The second visit is the point": "खरा मुद्दा दुसऱ्या भेटीचा आहे",
  "A returning patient does not repeat anything. They describe what is wrong today, and the questions adapt around what is already known.":
    "जुना रुग्ण काहीही पुन्हा सांगत नाही. आज काय त्रास आहे तेच सांगतो, आणि आधीच माहीत असलेल्यानुसार प्रश्न बदलतात.",
  "What it does": "हे काय करते",
  "Voice, in your language": "आवाज, तुमच्या भाषेत",
  "Speak your answers and correct the transcription before it is saved. Typing and tapping are always available — voice is never required.":
    "तुमची उत्तरे बोला आणि सेव्ह होण्यापूर्वी लिप्यंतर दुरुस्त करा. लिहिणे आणि स्पर्श करणे नेहमी उपलब्ध असते — आवाज कधीही सक्तीचा नाही.",
  "Built for every patient": "प्रत्येक रुग्णासाठी बनवलेले",
  "A short comfort check suggests text size, contrast, audio and a simpler screen layout. Age alone never decides it, and the patient can override anything.":
    "एक छोटी सुविधा तपासणी मजकुराचा आकार, रंगफरक, आवाज आणि सोपी स्क्रीन मांडणी सुचवते. केवळ वयावरून हे कधीच ठरत नाही, आणि रुग्ण काहीही बदलू शकतो.",
  "Reads old records": "जुन्या नोंदी वाचते",
  "Prescriptions and lab reports are scanned on the server. Lab values are compared only against the range printed on the report — never guessed.":
    "औषधांच्या चिठ्ठ्या आणि तपासणी अहवाल सर्व्हरवर स्कॅन केले जातात. तपासणी मूल्यांची तुलना केवळ अहवालावर छापलेल्या मर्यादेशी केली जाते — अंदाज कधीच बांधला जात नाही.",
  "Flags what should not wait": "जे थांबू शकत नाही ते चिन्हांकित करते",
  "Answers are screened for presentations that need prompt attention. The patient is told to speak to staff, and the flag cannot be switched off from the kiosk.":
    "लवकर लक्ष देण्याची गरज असलेल्या लक्षणांसाठी उत्तरे तपासली जातात. रुग्णाला कर्मचाऱ्यांशी बोलण्यास सांगितले जाते, आणि हे चिन्ह कियोस्कवरून बंद करता येत नाही.",
  "Allopathy and AYUSH": "ॲलोपॅथी आणि आयुष",
  "The patient chooses which system of medicine they are here for. An Ayurvedic visit adds the Dashavidha and Ashtasthana examination; an allopathic visit stays short.":
    "रुग्ण कोणत्या वैद्यक पद्धतीसाठी आला आहे ते निवडतो. आयुर्वेदिक भेटीत दशविध आणि अष्टस्थान परीक्षा जोडली जाते; ॲलोपॅथिक भेट थोडक्यात राहते.",
  "Consent, and nothing implied": "संमती, आणि गृहीत काहीही नाही",
  "Health information is collected only after the patient agrees, per purpose, and consent can be withdrawn. Health-ID linkage is prepared for ABDM but not connected.":
    "आरोग्य माहिती रुग्णाच्या सहमतीनंतरच, प्रत्येक उद्देशासाठी वेगळी गोळा केली जाते, आणि संमती मागे घेता येते. हेल्थ आयडी जोडणी ABDM साठी तयार आहे पण जोडलेली नाही.",
  "What it does not do": "हे काय करत नाही",
  "MediKiosk does not diagnose, does not prescribe, and does not replace a clinician. It organises what the patient tells us and what their documents say, and labels which is which.":
    "मेडीकियोस्क निदान करत नाही, औषध सुचवत नाही, आणि डॉक्टरांची जागा घेत नाही. रुग्ण जे सांगतो आणि त्यांच्या कागदपत्रांत जे लिहिले आहे ते नीट मांडते, आणि कोणते कोणते हे स्पष्ट करते.",
  "Specifications": "तपशील",
  "Stack": "तंत्रज्ञान",
  "React and TypeScript on the front, FastAPI and PostgreSQL behind, as a modular monolith. Alembic migrations, Docker images for both halves.":
    "पुढे React आणि TypeScript, मागे FastAPI आणि PostgreSQL, एक मॉड्युलर मोनोलिथ म्हणून. Alembic स्थलांतरे, दोन्ही भागांसाठी Docker प्रतिमा.",
  "Clinical data": "वैद्यकीय माहिती",
  "Every fact carries its source, confidence and whether a person has verified it. A new visit never overwrites the historical record.":
    "प्रत्येक बाबीसोबत तिचा स्रोत, विश्वासार्हता आणि एखाद्या व्यक्तीने ती पडताळली आहे का, हे असते. नवीन भेट जुनी नोंद कधीही खोडत नाही.",
  "AI": "एआय",
  "The interview is a deterministic state machine. A model may help read an answer or a document, but its output is schema-validated and every path works with AI switched off.":
    "मुलाखत ही एक निश्चित स्थिती-यंत्रणा आहे. उत्तर किंवा कागदपत्र वाचण्यात मॉडेल मदत करू शकते, पण त्याचे उत्तर स्कीमानुसार पडताळले जाते आणि एआय बंद असतानाही प्रत्येक मार्ग चालतो.",
  "All six languages are complete: English, Hindi, Marathi, Tamil, Gujarati and Punjabi. The four regional translations are machine-authored and marked for review by a speaker of each; anything still untranslated falls back rather than breaking.":
    "सर्व सहा भाषा पूर्ण आहेत: इंग्रजी, हिंदी, मराठी, तमिळ, गुजराती आणि पंजाबी. चारही प्रादेशिक अनुवाद यंत्राने केलेले आहेत आणि त्या भाषांच्या भाषकांच्या पुनरावलोकनासाठी चिन्हांकित आहेत; जे अजून अनुवादित नाही ते तुटण्याऐवजी पर्यायी भाषेत दिसते.",
  "Failure behaviour": "बिघाडाच्या वेळचे वर्तन",
  "No workflow depends on one external service. If AI, voice, scanning or the health-ID service is unavailable, the patient keeps going and nothing already entered is lost.":
    "कोणतीही प्रक्रिया एकाच बाह्य सेवेवर अवलंबून नाही. एआय, आवाज, स्कॅनिंग किंवा हेल्थ आयडी सेवा उपलब्ध नसेल, तरी रुग्ण पुढे जात राहतो आणि आधी भरलेले काहीही हरवत नाही.",
  "Accessibility": "सुलभता",
  "Keyboard navigable, visible focus, semantic landmarks, large touch targets, and status never conveyed by colour alone.":
    "कीबोर्डने वापरण्यायोग्य, दिसणारा फोकस, अर्थपूर्ण खुणा, मोठी स्पर्श-क्षेत्रे, आणि स्थिती केवळ रंगाने कधीही दर्शवली जात नाही.",
  "Runs on a tablet at reception or on the patient's own phone. Records live in your PostgreSQL database, and the schema is shaped for the clinician view that comes next.":
    "स्वागत कक्षातील टॅबलेटवर किंवा रुग्णाच्या स्वतःच्या फोनवर चालते. नोंदी तुमच्या PostgreSQL डेटाबेसमध्ये राहतात, आणि स्कीमा पुढे येणाऱ्या डॉक्टर-दृश्यासाठी घडवलेली आहे.",
  "See it work": "हे चालताना पहा",
  "Sign in with a mobile number, or open a demo patient with a full history already on file.":
    "मोबाइल क्रमांकाने साइन इन करा, किंवा संपूर्ण इतिहास असलेला डेमो रुग्ण उघडा.",
  "Prototype. All demo patients and medical records are fictional. Health-ID verification is simulated and not connected to ABDM.":
    "प्रारूप. सर्व डेमो रुग्ण आणि वैद्यकीय नोंदी काल्पनिक आहेत. हेल्थ आयडी पडताळणी कृत्रिम आहे आणि ABDM शी जोडलेली नाही.",

  // --- Returning-patient home ---------------------------------------------
  "Start a new health visit": "नवीन आरोग्य भेट सुरू करा",
  "Tell us what is troubling you today. We already have your history.":
    "आज तुम्हाला काय त्रास होत आहे ते सांगा. तुमचा इतिहास आमच्याकडे आहे.",
  "Continue your visit": "तुमची भेट पुढे चालू ठेवा",
  "Your health summary": "तुमचा आरोग्य सारांश",
  "Ongoing conditions": "सुरू असलेले आजार",
  "Your medicines": "तुमची औषधे",
  "Allergies": "ॲलर्जी",
  "Recent records": "अलीकडच्या नोंदी",
  "Recent activity": "अलीकडची हालचाल",
  "Last visit": "शेवटची भेट",
  "visits recorded": "भेटी नोंदवल्या",
  "Finish setting up your profile": "तुमची प्रोफाइल पूर्ण करा",
  "Nothing recorded yet": "अजून काही नोंदवलेले नाही",
  "You have not added any medical records yet":
    "तुम्ही अजून कोणतीही वैद्यकीय नोंद जोडलेली नाही",
  "A photo of a prescription or lab report helps your doctor see your history.":
    "औषधाच्या चिठ्ठीचा किंवा तपासणी अहवालाचा फोटो तुमच्या डॉक्टरांना तुमचा इतिहास पाहण्यास मदत करतो.",
  "No allergies recorded": "कोणतीही ॲलर्जी नोंदवलेली नाही",
  "Update my health history": "माझा आरोग्य इतिहास अद्ययावत करा",

  // --- Encounter (today's visit) -------------------------------------------
  "What brings you here today?": "आज तुम्ही कशासाठी आले आहात?",
  "Describe it in your own words — speak, type, or tap a common answer.":
    "तुमच्या शब्दांत सांगा — बोला, लिहा, किंवा सामान्य उत्तरावर स्पर्श करा.",
  "We already know about": "आम्हाला आधीच माहीत आहे",
  "You will not be asked about these again. You can update them from your profile.":
    "याबद्दल तुम्हाला पुन्हा विचारले जाणार नाही. तुम्ही ते प्रोफाइलमधून अद्ययावत करू शकता.",
  "About today only": "फक्त आजबद्दल",
  "New today": "आज नवीन",
  "Already on record": "आधीच नोंदीत",
  "That is everything for today": "आजसाठी इतकेच",
  "Please check what you told us before we send it to the care team.":
    "देखभाल पथकाला पाठवण्यापूर्वी तुम्ही सांगितलेले कृपया तपासा.",
  "Check and submit": "तपासा आणि पाठवा",
  "Marked urgent": "तातडीचे म्हणून चिन्हांकित",
  "Marked urgent — please stay near the staff desk.":
    "तातडीचे म्हणून चिन्हांकित — कृपया कर्मचारी कक्षाजवळ राहा.",
  "What you told us": "तुम्ही आम्हाला काय सांगितले",
  "A member of staff will review this with you. This cannot be turned off from here.":
    "एक कर्मचारी हे तुमच्यासोबत तपासेल. हे येथून बंद करता येत नाही.",
  "Staff have been notified. Please stay where you are.":
    "कर्मचाऱ्यांना कळवले आहे. कृपया तुम्ही आहात तिथेच राहा.",
  "Check today's visit": "आजची भेट तपासा",
  "Please make sure this is right. You can change today's answers.":
    "कृपया हे बरोबर आहे याची खात्री करा. तुम्ही आजची उत्तरे बदलू शकता.",
  "Today's concern": "आजची तक्रार",
  "What you told us today": "आज तुम्ही काय सांगितले",
  "questions you chose to skip": "तुम्ही वगळलेले प्रश्न",
  "How much it troubles you": "हे तुम्हाला किती त्रास देते",
  "out of 10": "१० पैकी",
  "This rating is not what made your visit urgent — that came from the symptoms you described.":
    "या गुणांकामुळे तुमची भेट तातडीची झाली नाही — ते तुम्ही सांगितलेल्या लक्षणांमुळे झाले.",
  "Relevant existing history": "संबंधित उपलब्ध इतिहास",
  "From your earlier visits. Editing this happens in your health history, not here.":
    "तुमच्या पूर्वीच्या भेटींतून. यात बदल तुमच्या आरोग्य इतिहासात होतो, येथे नाही.",
  "Records added today": "आज जोडलेल्या नोंदी",
  "Change today's answers": "आजची उत्तरे बदला",
  "Summary for the care team": "देखभाल पथकासाठी सारांश",
  "Still needed": "अजून आवश्यक",
  "Before you send this": "हे पाठवण्यापूर्वी",
  "My current symptoms were recorded correctly":
    "माझी सध्याची लक्षणे बरोबर नोंदवली गेली आहेत",
  "I have reviewed the information above": "मी वरील माहिती तपासली आहे",
  "I understand this will be used to support my healthcare visit":
    "हे माझ्या आरोग्य भेटीस मदत करण्यासाठी वापरले जाईल हे मला समजते",
  "Send to the care team": "देखभाल पथकाला पाठवा",
  "Your visit has been sent": "तुमची भेट पाठवली गेली आहे",
  "Back to home": "मुख्य पानावर परत",
  "This visit has already been sent. Start a new visit if something has changed.":
    "ही भेट आधीच पाठवली गेली आहे. काही बदलले असेल तर नवीन भेट सुरू करा.",

  // --- Errors and chrome ---------------------------------------------------
  "Something went wrong. Please try again.":
    "काहीतरी चुकले. कृपया पुन्हा प्रयत्न करा.",
  "We could not reach the server. Check the connection and try again.":
    "आम्ही सर्व्हरपर्यंत पोहोचू शकलो नाही. जोडणी तपासा आणि पुन्हा प्रयत्न करा.",
  "Your session has ended. Please sign in again.":
    "तुमचे सत्र संपले आहे. कृपया पुन्हा साइन इन करा.",
  "This is needed to continue": "पुढे जाण्यासाठी हे आवश्यक आहे",
  "Skip to main content": "मुख्य मजकुरावर जा",
  "Found in {name}": "{name} मध्ये मिळाले",
  "Your answers are saved as you go — you can stop and come back.":
    "तुमची उत्तरे सोबतच सेव्ह होतात — तुम्ही थांबून पुन्हा येऊ शकता.",

  // --- Enum labels -----------------------------------------------------------
  "Pending": "प्रतीक्षेत",
  "Processing": "प्रक्रियेत",
  "Completed": "पूर्ण",
  "Could not be read": "वाचता आले नाही",
  "Needs your review": "तुमच्या तपासणीची गरज",
  "Not verified": "पडताळलेले नाही",
  "Verified": "पडताळले",
  "Skipped": "वगळले",
  "Given": "दिली",
  "Declined": "नाकारली",
  "Withdrawn": "मागे घेतली",
  "Collecting your health information": "तुमची आरोग्यविषयक माहिती गोळा करणे",
  "Sharing with the doctor treating you":
    "तुमचे उपचार करणाऱ्या डॉक्टरांसोबत सामायिक करणे",
  "Linking your ABHA number": "तुमचा आभा क्रमांक जोडणे",
  "Standard": "मानक",
  "Easy Mode": "सोपा मोड",
  "Normal": "सामान्य",
  "Large": "मोठा",
  "Extra large": "खूप मोठा",
  "High": "उच्च",
  "Voice": "आवाज",
  "Touch": "स्पर्श",
  "Voice and touch": "आवाज आणि स्पर्श",
  "Typing": "लिहून",
  "Recommended for you": "तुमच्यासाठी सुचवलेले",
  "Chosen by you": "तुम्ही निवडलेले",
  "Not started": "सुरू झालेले नाही",
  "In progress": "सुरू आहे",
  "Awaiting your review": "तुमच्या तपासणीच्या प्रतीक्षेत",
  "Cancelled": "रद्द",
  "Confirmed": "पुष्ट",
  "Routine": "सामान्य",
  "Priority": "प्राधान्य",
  "Urgent": "तातडीचे",
  "First visit": "पहिली भेट",
  "Follow-up visit": "पुढील भेट",
  "From a document": "कागदपत्रातून",
  "From an earlier visit": "पूर्वीच्या भेटीतून",
  "From a clinician": "डॉक्टरांकडून",
  "Condition": "स्थिती",
  "Medicine": "औषध",
  "Test": "तपासणी",
  "Procedure": "प्रक्रिया",
  "Surgery": "शस्त्रक्रिया",
  "Allergy": "ॲलर्जी",
  "Vital sign": "जीवनचिन्ह",
  "Note": "टिप्पणी",
  "Visit": "भेट",
  "Low": "कमी",
  "Unclear": "अस्पष्ट",
  "Not reviewed": "तपासलेले नाही",
  "Kept": "ठेवले",
  "Removed": "काढले",
  "Allopathy": "ॲलोपॅथी",
  "Homoeopathy": "होमिओपॅथी",
  "Unani": "युनानी",
  "Siddha": "सिद्ध",
  "Yoga and Naturopathy": "योग व निसर्गोपचार",
  "Not sure yet": "अजून खात्री नाही",
  "Document you uploaded": "तुम्ही अपलोड केलेले कागदपत्र",
  "Visit record": "भेटीची नोंद",
  "Understood from what you said": "तुम्ही जे सांगितले त्यावरून समजले",
};
