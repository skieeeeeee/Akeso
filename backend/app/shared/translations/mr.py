"""Marathi translations, keyed by the English source string.

MACHINE-AUTHORED — pending review by a Marathi speaker. Clinical phrasing in
particular should be checked: a question that reads oddly to a patient gets a
worse answer, and a worse answer reaches a doctor.

Add or correct an entry by editing this file; nothing else needs to change.
An inline `mr=` argument at a `t()` call site always overrides an entry here.

Terminology held consistent throughout: रुग्ण (patient), आजार (illness),
औषध (medicine), तपासणी (test/examination), भेट (visit), तक्रार (complaint),
निदान (diagnosis), संमती (consent).
"""

from __future__ import annotations

MARATHI: dict[str, str] = {
    # --- Onboarding steps, greetings and status messages ------------------
    "Health ID": "हेल्थ आयडी",
    "Your details": "तुमची माहिती",
    "Comfort check": "सुविधा तपासणी",
    "Your experience": "तुमचा अनुभव",
    "Consent": "संमती",
    "Health history": "आरोग्य इतिहास",
    "Done": "पूर्ण",
    "Welcome": "स्वागत आहे",
    "Welcome back": "तुमचे पुन्हा स्वागत आहे",
    "Sorry, I did not catch that. Please try again, or tap an option.":
        "क्षमस्व, मला समजले नाही. कृपया पुन्हा सांगा, किंवा एखादा पर्याय निवडा.",
    "Saved. Ready to be read.": "सहेजले. वाचण्यासाठी तयार.",
    "Reading your document. This usually takes a few seconds.":
        "तुमचे कागदपत्र वाचले जात आहे. यास सामान्यतः काही सेकंद लागतात.",
    "We found some information in this document. Please check it.":
        "या कागदपत्रात आम्हाला काही माहिती मिळाली. कृपया ती तपासा.",
    "We read the text but could not pick out medical details. "
    "Your doctor can still read it.":
        "आम्ही मजकूर वाचला पण वैद्यकीय तपशील काढू शकलो नाही. "
        "तुमचे डॉक्टर ते वाचू शकतात.",
    "We could not read this document. It is saved and you can try again.":
        "आम्ही हे कागदपत्र वाचू शकलो नाही. ते सहेजले आहे आणि तुम्ही पुन्हा प्रयत्न करू शकता.",
    "This summarises what you told us and what your documents say. "
    "It is not a diagnosis, and your doctor will go through it with you.":
        "तुम्ही जे सांगितले आणि तुमच्या कागदपत्रांत जे लिहिले आहे, त्याचा हा सारांश आहे. "
        "हे निदान नाही, आणि तुमचे डॉक्टर ते तुमच्यासोबत पाहतील.",
    "Your visit details have been sent to the care team. Please wait to be called.":
        "तुमच्या भेटीची माहिती देखभाल पथकाला पाठवली आहे. कृपया बोलावले जाईपर्यंत थांबा.",
    "Your visit has been sent and marked urgent. Please stay near the staff desk.":
        "तुमची माहिती पाठवली आहे आणि तातडीचे म्हणून चिन्हांकित केली आहे. "
        "कृपया कर्मचारी कक्षाजवळ राहा.",

    # --- Accessibility assessment -------------------------------------
    "How comfortable are you using smartphones or digital devices?":
        "स्मार्टफोन किंवा डिजिटल उपकरणे वापरताना तुम्हाला कितपत सोयीचे वाटते?",
    "This helps us choose how much detail to show on each screen.":
        "यावरून आम्ही प्रत्येक स्क्रीनवर किती तपशील दाखवायचा ते ठरवतो.",
    "Very comfortable": "खूप सोयीचे",
    "Somewhat comfortable": "काहीसे सोयीचे",
    "I sometimes need help": "मला कधी कधी मदत लागते",
    "I prefer a simpler experience": "मला सोपा अनुभव आवडतो",
    "How would you prefer to answer questions?": "तुम्हाला प्रश्नांची उत्तरे कशी द्यायला आवडेल?",
    "You can always switch between speaking and tapping later.":
        "बोलणे आणि स्पर्श करणे यात तुम्ही नंतर कधीही बदल करू शकता.",
    "By speaking": "बोलून",
    "By touching options": "पर्यायांना स्पर्श करून",
    "Both": "दोन्ही",
    "Do you have difficulty reading text on screens?":
        "स्क्रीनवरील मजकूर वाचताना तुम्हाला अडचण येते का?",
    "If reading is hard, we can make text larger and read questions aloud.":
        "वाचणे कठीण असेल, तर आम्ही मजकूर मोठा करू शकतो आणि प्रश्न मोठ्याने वाचू शकतो.",
    "Do you have difficulty seeing content on screens?":
        "स्क्रीनवरील मजकूर पाहताना तुम्हाला अडचण येते का?",
    "We can increase the text size and use stronger colour contrast.":
        "आम्ही मजकुराचा आकार वाढवू शकतो आणि रंगांचा फरक अधिक स्पष्ट करू शकतो.",
    "Do you have difficulty hearing audio instructions?":
        "ऐकवलेल्या सूचना ऐकताना तुम्हाला अडचण येते का?",
    "If hearing is hard, nothing in this app will depend on sound.":
        "ऐकणे कठीण असेल, तर या ॲपमधील काहीही आवाजावर अवलंबून राहणार नाही.",
    "No difficulty": "काही अडचण नाही",
    "Sometimes": "कधी कधी",
    "Yes": "होय",
    "No": "नाही",
    "Is there anything else that would make this easier for you?":
        "हे तुमच्यासाठी अधिक सोपे होईल असे आणखी काही आहे का?",
    "This is completely optional. Share only what you want to.":
        "हे पूर्णपणे ऐच्छिक आहे. तुम्हाला जे सांगायचे आहे तेवढेच सांगा.",
    "I find reading and writing difficult": "मला वाचन-लेखन कठीण जाते",
    "I have low vision": "मला कमी दिसते",
    "I am hard of hearing": "मला ऐकायला कमी येते",
    "Tapping the screen is tiring": "स्क्रीनला स्पर्श करणे थकवणारे वाटते",
    "Someone is helping me today": "आज कोणी माझी मदत करत आहे",
    "I use sign language": "मी सांकेतिक भाषा वापरतो/वापरते",
    "Before we begin": "सुरुवात करण्यापूर्वी",
    "Speak your answers": "तुमची उत्तरे बोला",
    "Speak or tap, whichever suits": "बोला किंवा स्पर्श करा — जे सोयीचे असेल",
    "Tap to choose answers": "उत्तरे निवडण्यासाठी स्पर्श करा",
    "One question at a time, large buttons": "एका वेळी एक प्रश्न, मोठी बटणे",
    "All options on one screen": "सर्व पर्याय एकाच स्क्रीनवर",
    "Standard": "मानक",
    "Easy": "सोपा",
    "Normal": "सामान्य",
    "Large": "मोठा",
    "Extra large": "खूप मोठा",
    "Normal colours": "सामान्य रंग",
    "High contrast": "अधिक स्पष्ट रंगफरक",
    "Voice": "आवाज",
    "Touch": "स्पर्श",
    "Optional": "ऐच्छिक",
    "Usually filled in from your date of birth.": "सामान्यतः तुमच्या जन्मतारखेवरून भरले जाते.",
    "Your doctor needs this to understand your case before you walk in.":
        "तुम्ही आत येण्यापूर्वी तुमची केस समजून घेण्यासाठी डॉक्टरांना हे आवश्यक आहे.",

    # --- Consent -------------------------------------------------------
    "Collecting your health information": "तुमची आरोग्यविषयक माहिती गोळा करणे",
    "Your symptoms, past illnesses, surgeries, medicines, allergies and family history.":
        "तुमची लक्षणे, पूर्वीचे आजार, शस्त्रक्रिया, औषधे, ॲलर्जी आणि कौटुंबिक इतिहास.",
    "So your doctor already knows your history and can spend the visit on your actual problem.":
        "जेणेकरून तुमच्या डॉक्टरांना तुमचा इतिहास आधीच माहीत असेल आणि भेटीचा वेळ तुमच्या खऱ्या समस्येवर खर्च होईल.",
    "It is stored against your patient record and shown to the clinician treating you.":
        "ते तुमच्या रुग्ण नोंदीसोबत साठवले जाते आणि तुमचे उपचार करणाऱ्या डॉक्टरांना दाखवले जाते.",
    "Sharing with your doctor": "तुमच्या डॉक्टरांसोबत सामायिक करणे",
    "A summary of what you tell us today, and any records you upload.":
        "आज तुम्ही जे सांगाल त्याचा सारांश, आणि तुम्ही अपलोड केलेल्या नोंदी.",
    "Only clinicians involved in your care can see it.":
        "फक्त तुमच्या उपचारांशी संबंधित डॉक्टरच ते पाहू शकतात.",
    "Linking your health ID": "तुमचा हेल्थ आयडी जोडणे",
    "The health ID number you entered, linked to this patient record.":
        "तुम्ही दिलेला हेल्थ आयडी क्रमांक, या रुग्ण नोंदीशी जोडलेला.",
    "So your records can follow you between visits instead of starting over.":
        "जेणेकरून प्रत्येक भेटीत नव्याने सुरुवात न करता तुमच्या नोंदी तुमच्यासोबत राहतील.",
    "This is a prototype and is not connected to the national ABDM network.":
        "हे एक प्रारूप आहे आणि राष्ट्रीय ABDM नेटवर्कशी जोडलेले नाही.",
    "We will ask about your health so your doctor is prepared before you meet. "
    "You choose what to share, and you can withdraw your consent at any time.":
        "तुमची भेट होण्यापूर्वी डॉक्टर तयार असावेत म्हणून आम्ही तुमच्या आरोग्याबद्दल विचारू. "
        "काय सामायिक करायचे ते तुम्ही ठरवता, आणि तुमची संमती तुम्ही कधीही मागे घेऊ शकता.",
    "You can withdraw consent later from your profile. Nothing is shared without your agreement.":
        "तुम्ही नंतर तुमच्या प्रोफाइलमधून संमती मागे घेऊ शकता. तुमच्या सहमतीशिवाय काहीही सामायिक केले जात नाही.",

    # --- Red flags / safety --------------------------------------------
    "Please speak to healthcare staff now": "कृपया आता आरोग्य कर्मचाऱ्यांशी बोला",
    "Some of the symptoms you described may require urgent medical attention.":
        "तुम्ही सांगितलेल्या काही लक्षणांना तातडीच्या वैद्यकीय लक्षाची आवश्यकता असू शकते.",
    "Please inform nearby healthcare staff immediately. Show them this screen.":
        "कृपया जवळच्या आरोग्य कर्मचाऱ्यांना लगेच कळवा. त्यांना ही स्क्रीन दाखवा.",
    "This does not confirm a medical condition. It only means a health worker should "
    "look at you sooner rather than later.":
        "यावरून कोणताही आजार निश्चित होत नाही. याचा अर्थ फक्त इतका, की आरोग्य कर्मचाऱ्याने "
        "तुम्हाला उशिरा नाही, तर लवकर पाहावे.",
    "Marked urgent — please stay near the staff desk.":
        "तातडीचे म्हणून चिन्हांकित — कृपया कर्मचारी कक्षाजवळ राहा.",
    "Continue answering while waiting": "प्रतीक्षा करताना उत्तरे देत राहा",
    "I need immediate assistance": "मला तातडीने मदत हवी आहे",

    # --- Medical profile sections --------------------------------------
    "Why you are here": "तुम्ही येथे का आले आहात",
    "First, tell us what brings you in today.": "प्रथम, आज तुम्ही कशासाठी आले आहात ते सांगा.",
    "What problem brings you in today?": "आज कोणत्या समस्येसाठी तुम्ही आले आहात?",
    "Describe it in your own words. You can speak instead of typing.":
        "तुमच्या शब्दांत सांगा. टाइप करण्याऐवजी तुम्ही बोलू शकता.",
    "e.g. chest pain for three days": "उदा. तीन दिवसांपासून छातीत दुखणे",
    "About this problem": "या समस्येबद्दल",
    "How long has it been there, and what makes it better or worse?":
        "हे किती काळापासून आहे, आणि कशाने बरे किंवा जास्त वाटते?",
    "How long have you had this?": "हे तुम्हाला किती काळापासून आहे?",
    "A rough idea is fine.": "अंदाजे सांगितले तरी चालेल.",
    "Started today": "आज सुरू झाले",
    "2–3 days": "२–३ दिवस",
    "About a week": "सुमारे एक आठवडा",
    "A few weeks": "काही आठवडे",
    "More than a month": "एक महिन्यापेक्षा जास्त",
    "How much does it trouble you, from 1 to 10?": "हे तुम्हाला १ ते १० मध्ये किती त्रास देते?",
    "1 is very mild, 10 is the worst.": "१ म्हणजे खूप सौम्य, १० म्हणजे सर्वात जास्त.",
    "Is there anything that makes it better or worse?":
        "कशाने ते बरे किंवा जास्त होते असे काही आहे का?",
    "For example rest, food, walking, or a medicine you took.":
        "उदाहरणार्थ विश्रांती, जेवण, चालणे, किंवा तुम्ही घेतलेले औषध.",
    "Anything else you feel": "तुम्हाला जाणवणारे इतर काही",
    "A quick check for other symptoms.": "इतर लक्षणांची झटपट तपासणी.",
    "Are you also feeling any of these?": "तुम्हाला यांपैकी काही जाणवत आहे का?",
    "Choose as many as you like.": "तुम्हाला हवे तितके पर्याय निवडा.",
    "Fever": "ताप",
    "Cough": "खोकला",
    "Breathlessness": "श्वास लागणे",
    "Short of breath": "दम लागणे",
    "Headache": "डोकेदुखी",
    "Dizziness": "चक्कर",
    "Vomiting": "उलटी",
    "Loose motions": "जुलाब",
    "Swelling": "सूज",
    "Pain": "दुखणे",
    "Very tired": "खूप थकवा",
    "Losing weight": "वजन कमी होणे",
    "Not sleeping well": "झोप न लागणे",
    "Stomach pain": "पोटदुखी",
    "Stomach problem": "पोटाची तक्रार",
    "Chest pain": "छातीत दुखणे",

    # --- Past illnesses -------------------------------------------------
    "Past illnesses": "पूर्वीचे आजार",
    "Now a few questions about long-term health conditions.":
        "आता दीर्घकालीन आजारांबद्दल काही प्रश्न.",
    "Has a doctor told you that you have a long-term illness?":
        "तुम्हाला दीर्घकालीन आजार आहे असे डॉक्टरांनी सांगितले आहे का?",
    "Such as diabetes, blood pressure or asthma.":
        "जसे मधुमेह, रक्तदाब किंवा दमा.",
    "Any long-term illness you have been told you have?":
        "तुम्हाला आहे असे सांगितले गेलेले कोणतेही दीर्घकालीन आजार?",
    "Which illness?": "कोणता आजार?",
    "Any old illness?": "जुना कोणता आजार?",
    "Ongoing conditions": "सुरू असलेले आजार",
    "Diabetes": "मधुमेह",
    "High blood pressure": "उच्च रक्तदाब",
    "Asthma": "दमा",
    "Heart disease": "हृदयविकार",
    "Thyroid problem": "थायरॉइडची तक्रार",
    "Tuberculosis": "क्षयरोग",
    "Cancer": "कर्करोग",
    "Something else": "इतर काही",
    "Are you currently taking medicine for {item}?":
        "{item} साठी तुम्ही सध्या औषध घेत आहात का?",
    "Do you remember the name of the medicine for {item}?":
        "{item} साठीच्या औषधाचे नाव तुम्हाला आठवते का?",
    "If you are not sure, you can skip this or upload the prescription later.":
        "खात्री नसेल, तर हे वगळा किंवा नंतर औषधाची चिठ्ठी अपलोड करा.",

    # --- Operations -----------------------------------------------------
    "Operations": "शस्त्रक्रिया",
    "Have you ever had an operation?": "तुमची कधी शस्त्रक्रिया झाली आहे का?",
    "Have you had any operation?": "तुमची कोणती शस्त्रक्रिया झाली आहे का?",
    "Any operation, however long ago.": "कोणतीही शस्त्रक्रिया, कितीही जुनी असली तरी.",
    "What operation, and roughly when?": "कोणती शस्त्रक्रिया, आणि अंदाजे कधी?",
    "For example: gallbladder removed, 2019.": "उदाहरणार्थ: पित्ताशय काढले, २०१९.",
    "e.g. gallbladder removed, 2019": "उदा. पित्ताशय काढले, २०१९",

    # --- Medicines ------------------------------------------------------
    "Medicines": "औषधे",
    "Medicines you take": "तुम्ही घेत असलेली औषधे",
    "Let us record the medicines you take.": "तुम्ही घेत असलेली औषधे नोंदवू या.",
    "Which medicines do you take regularly?": "तुम्ही नियमित कोणती औषधे घेता?",
    "Which medicines are you taking now?": "तुम्ही सध्या कोणती औषधे घेत आहात?",
    "Any daily medicine?": "रोजचे कोणते औषध?",
    "Include tablets, insulin, inhalers and drops.":
        "गोळ्या, इन्सुलिन, इनहेलर आणि थेंब यांचा समावेश करा.",
    "Add them one at a time. Tap a common answer or say it aloud.":
        "एका वेळी एक जोडा. सामान्य उत्तरावर स्पर्श करा किंवा मोठ्याने सांगा.",
    "Add them one at a time.": "एका वेळी एक जोडा.",
    "e.g. Metformin 500 mg twice a day": "उदा. मेटफॉर्मिन ५०० मिग्रॅ दिवसातून दोन वेळा",

    # --- Allergies ------------------------------------------------------
    "Allergies": "ॲलर्जी",
    "Medicine problems": "औषधांचा त्रास",
    "This one matters a lot for your safety.": "तुमच्या सुरक्षिततेसाठी हे खूप महत्त्वाचे आहे.",
    "Are you allergic to any medicine or food?":
        "तुम्हाला कोणत्या औषधाची किंवा अन्नाची ॲलर्जी आहे का?",
    "Any allergy?": "कोणती ॲलर्जी?",
    "Has any medicine ever caused you a problem?":
        "कोणत्या औषधाने तुम्हाला कधी त्रास झाला आहे का?",
    "Tell us even if you are unsure — it keeps you safe.":
        "खात्री नसली तरी सांगा — त्यामुळे तुम्ही सुरक्षित राहता.",
    "For example it upset your stomach, or you had to stop it.":
        "उदाहरणार्थ पोट बिघडले, किंवा ते थांबवावे लागले.",
    "Which ones?": "कोणती?",
    "Penicillin": "पेनिसिलिन",
    "Aspirin": "ॲस्पिरिन",
    "Sulfa drugs": "सल्फा औषधे",
    "Dust": "धूळ",
    "No known allergies": "ज्ञात ॲलर्जी नाही",
    "e.g. penicillin, peanuts": "उदा. पेनिसिलिन, शेंगदाणे",
    "e.g. aspirin upset my stomach": "उदा. ॲस्पिरिनने माझे पोट बिघडले",

    # --- Family and personal history ------------------------------------
    "Family health": "कौटुंबिक आरोग्य",
    "Some illnesses run in families.": "काही आजार कुटुंबात चालत आलेले असतात.",
    "Does any illness run in your close family?":
        "तुमच्या जवळच्या कुटुंबात कोणता आजार चालत आलेला आहे का?",
    "Any illness that runs in your family?": "तुमच्या कुटुंबात चालत आलेला कोणता आजार?",
    "Any illness in the family?": "कुटुंबात कोणता आजार?",
    "Parents, brothers, sisters or children.": "आई-वडील, भाऊ, बहिणी किंवा मुले.",
    "Family history": "कौटुंबिक इतिहास",
    "e.g. mother has diabetes": "उदा. आईला मधुमेह आहे",
    "Daily habits": "रोजच्या सवयी",
    "Daily life": "रोजचे जीवन",
    "Anything about your habits your doctor should know?":
        "तुमच्या सवयींबद्दल डॉक्टरांना माहीत असावे असे काही आहे का?",
    "Which of these apply to you?": "यांपैकी कोणते तुम्हाला लागू होते?",
    "I do not smoke": "मी धूम्रपान करत नाही",
    "I smoke": "मी धूम्रपान करतो/करते",
    "I do not drink alcohol": "मी मद्यपान करत नाही",
    "I drink alcohol": "मी मद्यपान करतो/करते",
    "I exercise regularly": "मी नियमित व्यायाम करतो/करते",
    "Vegetarian diet": "शाकाहारी आहार",
    "Non-smoker": "धूम्रपान न करणारे",
    "Smoker": "धूम्रपान करणारे",
    "No alcohol": "मद्यपान नाही",
    "What work do you do?": "तुम्ही काय काम करता?",
    "Some jobs affect health, so this can be useful.":
        "काही कामांचा आरोग्यावर परिणाम होतो, म्हणून हे उपयुक्त ठरू शकते.",
    "e.g. non-smoker, vegetarian diet": "उदा. धूम्रपान न करणारे, शाकाहारी आहार",
    "e.g. diabetes, high blood pressure": "उदा. मधुमेह, उच्च रक्तदाब",

    # --- Investigations --------------------------------------------------
    "Earlier tests": "पूर्वीच्या तपासण्या",
    "Earlier test results": "पूर्वीच्या तपासण्यांचे निकाल",
    "Any tests you have had done recently.": "अलीकडे तुम्ही केलेल्या कोणत्याही तपासण्या.",
    "Have you had any blood test or scan recently?":
        "अलीकडे तुमची रक्ततपासणी किंवा स्कॅन झाले आहे का?",
    "Any recent test result you remember?":
        "अलीकडचा कोणता तपासणी निकाल तुम्हाला आठवतो का?",
    "In the last year or so.": "गेल्या वर्षभरात.",
    "Which test, and what did it show?": "कोणती तपासणी, आणि त्यात काय आले?",
    "If you have the report, you can upload it in the next step instead.":
        "अहवाल असेल, तर पुढच्या टप्प्यात तुम्ही तो अपलोड करू शकता.",
    "e.g. HbA1c 8.4% in March": "उदा. मार्चमध्ये HbA1c ८.४%",

    # --- Anything else ---------------------------------------------------
    "Anything else": "इतर काही",
    "A few questions about your habits and routine.":
        "तुमच्या सवयी आणि दिनचर्येबद्दल काही प्रश्न.",
    "Your usual tendency, not just today.": "तुमची नेहमीची प्रवृत्ती, फक्त आजची नाही.",
    "e.g. three days, worse on walking": "उदा. तीन दिवस, चालल्यावर जास्त",
    "e.g. very tired, losing weight": "उदा. खूप थकवा, वजन कमी होणे",
    "Anything else you would like your doctor to know?":
        "तुमच्या डॉक्टरांना माहीत असावे असे आणखी काही आहे का?",
    "Are you also feeling anything else?": "तुम्हाला आणखी काही जाणवत आहे का?",
    "Could you tell us a little more?": "तुम्ही थोडे अधिक सांगू शकाल का?",
    "Yes or no is enough.": "होय किंवा नाही एवढे पुरे.",
    "Choose as many as apply.": "जे लागू होतील ते सर्व निवडा.",
    "This question was suggested from what you just said. You can skip it.":
        "तुम्ही आता जे सांगितले त्यावरून हा प्रश्न सुचवला आहे. तुम्ही तो वगळू शकता.",
    "Optional questions used in Ayurvedic practice.":
        "आयुर्वेदिक उपचारपद्धतीत वापरले जाणारे ऐच्छिक प्रश्न.",

    # --- Encounter script (today's visit) -------------------------------
    "Type of treatment": "उपचाराचा प्रकार",
    "First, tell us which kind of care you are here for.":
        "प्रथम, तुम्ही कोणत्या प्रकारच्या उपचारासाठी आले आहात ते सांगा.",
    "Which kind of treatment are you here for?":
        "तुम्ही कोणत्या प्रकारच्या उपचारासाठी आले आहात?",
    "Which treatment?": "कोणता उपचार?",
    "This decides which questions we ask. You can pick a different one next time.":
        "यावरून आम्ही कोणते प्रश्न विचारायचे ते ठरते. पुढच्या वेळी तुम्ही वेगळा निवडू शकता.",
    "Modern medicine (Allopathy)": "आधुनिक वैद्यकशास्त्र (ॲलोपॅथी)",
    "Allopathy": "ॲलोपॅथी",
    "Ayurveda": "आयुर्वेद",
    "Homoeopathy": "होमिओपॅथी",
    "Unani": "युनानी",
    "Siddha": "सिद्ध",
    "Yoga & Naturopathy": "योग व निसर्गोपचार",
    "Yoga and Naturopathy": "योग व निसर्गोपचार",
    "I am not sure": "मला खात्री नाही",
    "Today's concern": "आजची तक्रार",
    "A few questions about this problem only.": "फक्त या समस्येबद्दल काही प्रश्न.",
    "We already have your health history. Just tell us what is new.":
        "तुमचा आरोग्य इतिहास आमच्याकडे आहे. फक्त नवीन काय आहे ते सांगा.",
    "Tell us what is troubling you today.": "आज तुम्हाला काय त्रास होत आहे ते सांगा.",
    "What is troubling you today?": "आज तुम्हाला काय त्रास होत आहे?",
    "What is troubling you?": "तुम्हाला काय त्रास होत आहे?",
    "What brings you here today?": "आज तुम्ही कशासाठी आले आहात?",
    "In your own words. You can speak instead of typing.":
        "तुमच्या शब्दांत. टाइप करण्याऐवजी तुम्ही बोलू शकता.",
    "When did it start?": "हे कधी सुरू झाले?",
    "Since when?": "कधीपासून?",
    "Today": "आज",
    "Yesterday": "काल",
    "2–3 days ago": "२–३ दिवसांपूर्वी",
    "About a week ago": "सुमारे एक आठवड्यापूर्वी",
    "Longer than a week": "एक आठवड्यापेक्षा जास्त",
    "A few details": "थोडे तपशील",
    "Can you describe it a little more?": "तुम्ही याबद्दल थोडे अधिक सांगू शकाल का?",
    "For example where it is, what it feels like, or what makes it worse.":
        "उदाहरणार्थ ते कुठे आहे, कसे वाटते, किंवा कशाने वाढते.",
    "How bad is it?": "किती त्रास होतो?",
    "How much is it troubling you, from 1 to 10?":
        "हे तुम्हाला १ ते १० मध्ये किती त्रास देत आहे?",
    "Is anything else happening as well?": "यासोबत आणखी काही होत आहे का?",
    "Only choose what you actually feel.": "तुम्हाला खरोखर जाणवते तेवढेच निवडा.",
    "Have you taken anything for it?": "यासाठी तुम्ही काही घेतले आहे का?",
    "Any medicine or home remedy, even if it did not help.":
        "कोणतेही औषध किंवा घरगुती उपाय, त्याचा उपयोग झाला नसला तरी.",
    "Anything changed?": "काही बदलले आहे का?",
    "Have your regular medicines changed since your last visit?":
        "मागच्या भेटीनंतर तुमची नियमित औषधे बदलली आहेत का?",
    "We already have your earlier list — only tell us what changed.":
        "तुमची आधीची यादी आमच्याकडे आहे — फक्त काय बदलले ते सांगा.",
    "What has changed?": "काय बदलले आहे?",
    "A medicine you started, stopped, or now take differently.":
        "तुम्ही सुरू केलेले, थांबवलेले, किंवा वेगळ्या पद्धतीने घेत असलेले औषध.",
    "Has a doctor told you about any new condition since then?":
        "तेव्हापासून डॉक्टरांनी तुम्हाला कोणत्या नवीन आजाराबद्दल सांगितले आहे का?",
    "Only something new.": "फक्त नवीन असलेले.",
    "What was it?": "ते काय होते?",
    "This is your space.": "ही तुमची जागा आहे.",
    "Anything else you want the doctor to know today?":
        "आज डॉक्टरांना माहीत असावे असे आणखी काही आहे का?",
    "Only here for a check-up": "फक्त तपासणीसाठी आलो/आले आहे",
    "Hospital visit": "रुग्णालय भेट",

    # --- AYUSH: Dashavidha ----------------------------------------------
    "Ten-fold examination": "दशविध परीक्षा",
    "Dashavidha Pariksha — questions about your constitution.":
        "दशविध परीक्षा — तुमच्या प्रकृतीबद्दलचे प्रश्न.",
    "Prakriti": "प्रकृती",
    "Which best describes your natural build and temperament?":
        "तुमची स्वाभाविक ठेवण आणि स्वभाव कोणते सर्वात योग्य वर्णन करते?",
    "Your lifelong tendency, not how you feel today.":
        "तुमची आयुष्यभराची प्रवृत्ती, आजची स्थिती नाही.",
    "Vikriti": "विकृती",
    "How do you feel compared with your usual self?":
        "तुमच्या नेहमीच्या स्थितीच्या तुलनेत तुम्हाला कसे वाटते?",
    "Your current state, today.": "तुमची आजची सध्याची स्थिती.",
    "Sara": "सार",
    "How would you describe your overall vitality?":
        "तुमच्या एकूण चैतन्याचे वर्णन तुम्ही कसे कराल?",
    "How strong and resilient you generally feel.":
        "तुम्ही सामान्यतः कितपत सशक्त आणि सहनशील वाटता.",
    "Samhanana": "संहनन",
    "How is your body build?": "तुमची शरीरयष्टी कशी आहे?",
    "Muscle and frame, in your own view.": "स्नायू आणि बांधा, तुमच्या मते.",
    "Pramana": "प्रमाण",
    "How would you describe your height and weight together?":
        "तुमची उंची आणि वजन एकत्र पाहता त्याचे वर्णन कसे कराल?",
    "Roughly proportionate, or not.": "अंदाजे प्रमाणबद्ध, की नाही.",
    "Satmya": "सात्म्य",
    "Which foods or conditions suit you well?":
        "कोणते पदार्थ किंवा परिस्थिती तुम्हाला चांगल्या मानवतात?",
    "What you tolerate easily.": "तुम्ही सहज सहन करू शकता ते.",
    "Sattva": "सत्त्व",
    "How do you usually handle stress?": "तणाव तुम्ही सामान्यतः कसा हाताळता?",
    "Your mental steadiness.": "तुमची मानसिक स्थिरता.",
    "Ahara Shakti": "आहार शक्ती",
    "How is your appetite and digestion?": "तुमची भूक आणि पचन कसे आहे?",
    "How much you can eat and digest comfortably.":
        "तुम्ही सहजपणे किती खाऊ आणि पचवू शकता.",
    "Vyayama Shakti": "व्यायाम शक्ती",
    "How much physical exertion can you manage?": "तुम्ही किती शारीरिक श्रम करू शकता?",
    "Before you need to rest.": "विश्रांतीची गरज भासण्यापूर्वी.",
    "Vaya": "वय",
    "Which life stage are you in?": "तुम्ही कोणत्या जीवनावस्थेत आहात?",

    # --- AYUSH: Ashtasthana ----------------------------------------------
    "Eight-fold examination": "अष्टस्थान परीक्षा",
    "Ashtasthana Pariksha — your practitioner will confirm each of these.":
        "अष्टस्थान परीक्षा — यांपैकी प्रत्येकाची तुमचे वैद्य खात्री करतील.",
    "Only what you notice yourself.": "तुम्हाला स्वतःला जे जाणवते तेवढेच.",
    "Your own sense of it — a practitioner will check properly.":
        "याबद्दल तुमची स्वतःची जाणीव — वैद्य योग्य प्रकारे तपासतील.",
    "Nadi": "नाडी",
    "How does your pulse or heartbeat usually feel?":
        "तुमची नाडी किंवा हृदयाची धडधड सामान्यतः कशी जाणवते?",
    "Mutra": "मूत्र",
    "How is your urine?": "तुमची लघवी कशी आहे?",
    "Colour, quantity and how often.": "रंग, प्रमाण आणि किती वेळा.",
    "Mala": "मल",
    "How are your bowel movements?": "तुमची शौचाची प्रवृत्ती कशी आहे?",
    "Regularity and consistency.": "नियमितपणा आणि घट्टपणा.",
    "Jihva": "जिव्हा",
    "How does your tongue look and feel?": "तुमची जीभ कशी दिसते आणि कशी जाणवते?",
    "Coating, dryness or taste in the mouth.": "जिभेवरचा थर, कोरडेपणा किंवा तोंडाची चव.",
    "Shabda": "शब्द",
    "How is your voice at present?": "तुमचा आवाज सध्या कसा आहे?",
    "Strength and clarity when you speak.": "बोलताना जोर आणि स्पष्टता.",
    "Sparsha": "स्पर्श",
    "How does your skin feel to touch?": "तुमची त्वचा स्पर्शाला कशी जाणवते?",
    "Temperature, dryness or sweating.": "तापमान, कोरडेपणा किंवा घाम.",
    "Drik": "दृक्",
    "How are your eyes and vision?": "तुमचे डोळे आणि दृष्टी कशी आहे?",
    "Akriti": "आकृती",
    "How would you describe your overall appearance now?":
        "तुमच्या एकूण दिसण्याचे वर्णन आता कसे कराल?",
    "How you look and feel compared with your usual self.":
        "तुमच्या नेहमीच्या स्थितीच्या तुलनेत तुम्ही कसे दिसता आणि कसे वाटता.",

    # --- AYUSH: lifestyle -------------------------------------------------
    "Digestion, sleep and routine": "पचन, झोप आणि दिनचर्या",
    "Agni, Nidra, Ahara and Vihara — how you eat, sleep and live.":
        "अग्नी, निद्रा, आहार आणि विहार — तुम्ही कसे खाता, झोपता आणि जगता.",
    "Agni": "अग्नी",
    "How well do you digest your food?": "तुमचे अन्न कितपत चांगले पचते?",
    "Whether food feels heavy, or digests comfortably.":
        "अन्न जड वाटते, की सहज पचते.",
    "Koshtha": "कोष्ठ",
    "How does your gut normally behave?": "तुमचे पोट सामान्यतः कसे वागते?",
    "Nidra": "निद्रा",
    "How is your sleep?": "तुमची झोप कशी आहे?",
    "Falling asleep, staying asleep, and feeling rested.":
        "झोप लागणे, टिकणे, आणि विश्रांती मिळाल्यासारखे वाटणे.",
    "Manas": "मनस्",
    "How has your mind felt lately?": "अलीकडे तुमच्या मनाला कसे वाटले आहे?",
    "Only if you wish to say. This is recorded for your practitioner, not assessed here.":
        "तुम्हाला सांगायचे असेल तरच. हे तुमच्या वैद्यांसाठी नोंदवले जाते, येथे त्याचे मूल्यांकन होत नाही.",
    "And your daily routine?": "आणि तुमची दिनचर्या?",
    "Which of these describe your diet?": "यांपैकी कोणते तुमच्या आहाराचे वर्णन करते?",
    "Ayurveda assessment": "आयुर्वेद मूल्यांकन",
    "These optional questions are used in Ayurvedic practice. They describe your "
    "constitution and routine — they are not a diagnosis, and you can skip any of them.":
        "हे ऐच्छिक प्रश्न आयुर्वेदिक उपचारपद्धतीत वापरले जातात. ते तुमची प्रकृती आणि "
        "दिनचर्या सांगतात — हे निदान नाही, आणि तुम्ही यांपैकी कोणताही प्रश्न वगळू शकता.",

    # --- Structured history section names --------------------------------
    "Chief complaint": "मुख्य तक्रार",
    "History of present illness": "सध्याच्या आजाराचा इतिहास",
    "Past medical history": "पूर्वीचा वैद्यकीय इतिहास",
    "Past surgical history": "पूर्वीचा शस्त्रक्रिया इतिहास",
    "Medications": "औषधे",
    "Current medications": "सध्याची औषधे",
    "Drug history": "औषधांचा इतिहास",
    "Personal history": "वैयक्तिक इतिहास",
    "Previous investigations": "पूर्वीच्या तपासण्या",
    "Review of systems": "प्रणालींची समीक्षा",
    "Additional information": "अतिरिक्त माहिती",
    "None reported": "काही सांगितले नाही",
    "Regarding this problem": "या समस्येबद्दल",
    "Also reports": "हेही सांगितले",

    # --- Narratives -------------------------------------------------------
    "The patient": "रुग्ण",
    "{age}-year-old": "{age} वर्षे",
    "no specific complaint": "विशेष तक्रार नाही",
    "an unspecified concern": "अस्पष्ट तक्रार",
    "{subject} reports: {complaint}.": "{subject} यांची तक्रार: {complaint}.",
    "{subject} presents reporting: {complaint}.": "{subject} यांची तक्रार: {complaint}.",
    "{subject} returns reporting: {complaint}.":
        "{subject} पुन्हा आले आहेत, तक्रार: {complaint}.",
    "{lead}: {found}.": "{lead}: {found}.",
    "{lead}: none reported.": "{lead}: काही सांगितले नाही.",
    "About this problem today: {items}.": "आज या समस्येबद्दल: {items}.",
    "Severity reported by the patient: {value}.": "रुग्णाने सांगितलेली तीव्रता: {value}.",
    "No further detail was given about the problem.":
        "समस्येबद्दल यापेक्षा अधिक तपशील दिला गेला नाही.",
    "Also reported today: {items}.": "आज हेही सांगितले: {items}.",
    "Known conditions from earlier visits: {items}.":
        "पूर्वीच्या भेटींवरून ज्ञात आजार: {items}.",
    "Medications on record: {items}.": "नोंदीतील औषधे: {items}.",
    "Allergies on record: {items}.": "नोंदीतील ॲलर्जी: {items}.",
    "No allergies recorded.": "कोणतीही ॲलर्जी नोंदवलेली नाही.",
    "Medication changes reported today: {items}.": "आज सांगितलेले औषधांतील बदल: {items}.",
    "New conditions reported today: {items}.": "आज सांगितलेले नवीन आजार: {items}.",
    "This visit has been marked urgent because some described symptoms may require "
    "prompt attention.":
        "या भेटीला तातडीचे म्हणून चिन्हांकित केले आहे, कारण सांगितलेल्या काही लक्षणांकडे "
        "लवकर लक्ष देणे आवश्यक असू शकते.",
    "Recorded from the patient's own account and their existing records. "
    "This is not a diagnosis.":
        "रुग्णाने स्वतः सांगितल्यानुसार आणि त्यांच्या उपलब्ध नोंदींवरून नोंदवले आहे. "
        "हे निदान नाही.",
    "This is a record of information provided by the patient and read from their "
    "documents. It is not a diagnosis.":
        "ही रुग्णाने दिलेली आणि त्यांच्या कागदपत्रांतून वाचलेली माहितीची नोंद आहे. "
        "हे निदान नाही.",
    "This records what you told us today alongside what we already knew. It is not a "
    "diagnosis, and a healthcare professional will review it with you.":
        "आज तुम्ही जे सांगितले आणि आम्हाला आधीच माहीत असलेले, या दोन्हींची ही नोंद आहे. "
        "हे निदान नाही, आणि एक आरोग्य व्यावसायिक तुमच्यासोबत ते तपासेल.",

    # --- Gender and care-system labels used in prose ----------------------
    "male": "पुरुष",
    "female": "स्त्री",
    "other": "इतर",
    "gender not stated": "लिंग सांगितले नाही",
    "not decided yet": "अजून ठरलेले नाही",

    # --- Demo patients ----------------------------------------------------
    "Rajesh Kumar · 52": "राजेश कुमार · ५२",
    "Returning patient, comfortable with digital forms. Standard mode.":
        "जुने रुग्ण, डिजिटल फॉर्ममध्ये सहज. मानक पद्धत.",
    "Kamla Devi · 71": "कमला देवी · ७१",
    "Prefers a simpler experience. Easy mode with audio guidance.":
        "सोपा अनुभव पसंत करतात. आवाज मार्गदर्शनासह सोपी पद्धत.",
    "Anil Sharma · 45": "अनिल शर्मा · ४५",
    "Low vision. Extra-large text and high contrast.":
        "कमी दृष्टी. खूप मोठा मजकूर आणि अधिक स्पष्ट रंगफरक.",
    "Sunita Devi · 34": "सुनीता देवी · ३४",
    "First-time patient who stopped part-way through onboarding.":
        "पहिल्यांदा आलेल्या रुग्ण, ज्यांनी नोंदणी अर्धवट सोडली.",
}
