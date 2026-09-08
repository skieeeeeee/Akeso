"""Gujarati translations, keyed by the English source string.

MACHINE-AUTHORED — pending review by a Gujarati speaker. Clinical phrasing in
particular should be checked: a question that reads oddly to a patient gets a
worse answer, and a worse answer reaches a doctor.

Add or correct an entry by editing this file; nothing else needs to change.
An inline `gu=` argument at a `t()` call site always overrides an entry here.

Terminology held consistent throughout: દર્દી (patient), બીમારી (illness),
દવા (medicine), તપાસ (test/examination), મુલાકાત (visit), ફરિયાદ (complaint),
નિદાન (diagnosis), સંમતિ (consent).
"""

from __future__ import annotations

GUJARATI: dict[str, str] = {
    # --- Onboarding steps, greetings and status messages ------------------
    "Health ID": "હેલ્થ આઈડી",
    "Your details": "તમારી માહિતી",
    "Comfort check": "સુવિધા તપાસ",
    "Your experience": "તમારો અનુભવ",
    "Consent": "સંમતિ",
    "Health history": "આરોગ્ય ઇતિહાસ",
    "Done": "પૂર્ણ",
    "Welcome": "સ્વાગત છે",
    "Welcome back": "તમારું ફરી સ્વાગત છે",
    "Sorry, I did not catch that. Please try again, or tap an option.":
        "માફ કરશો, મને સમજાયું નહીં. કૃપા કરીને ફરી કહો, કે કોઈ વિકલ્પ પસંદ કરો.",
    "Saved. Ready to be read.": "સાચવ્યું. વાંચવા માટે તૈયાર.",
    "Reading your document. This usually takes a few seconds.":
        "તમારો દસ્તાવેજ વંચાઈ રહ્યો છે. આમાં સામાન્યપણે થોડી સેકંડ લાગે છે.",
    "We found some information in this document. Please check it.":
        "આ દસ્તાવેજમાં અમને થોડી માહિતી મળી. કૃપા કરીને તે તપાસો.",
    "We read the text but could not pick out medical details. "
    "Your doctor can still read it.":
        "અમે લખાણ વાંચ્યું પણ તબીબી વિગત કાઢી ન શક્યા. "
        "તમારા ડૉક્ટર તે વાંચી શકે છે.",
    "We could not read this document. It is saved and you can try again.":
        "અમે આ દસ્તાવેજ વાંચી ન શક્યા. તે સાચવેલો છે અને તમે ફરી પ્રયાસ કરી શકો છો.",
    "This summarises what you told us and what your documents say. "
    "It is not a diagnosis, and your doctor will go through it with you.":
        "તમે જે કહ્યું અને તમારા દસ્તાવેજોમાં જે લખ્યું છે, તેનો આ સારાંશ છે. "
        "આ નિદાન નથી, અને તમારા ડૉક્ટર તે તમારી સાથે જોશે.",
    "Your visit details have been sent to the care team. Please wait to be called.":
        "તમારી મુલાકાતની માહિતી સંભાળ ટીમને મોકલી દેવાઈ છે. કૃપા કરીને બોલાવવામાં આવે ત્યાં સુધી રાહ જુઓ.",
    "Your visit has been sent and marked urgent. Please stay near the staff desk.":
        "તમારી માહિતી મોકલી દેવાઈ છે અને તાત્કાલિક તરીકે ચિહ્નિત કરાઈ છે. "
        "કૃપા કરીને સ્ટાફ ડેસ્ક પાસે રહો.",

    # --- Accessibility assessment -------------------------------------
    "How comfortable are you using smartphones or digital devices?":
        "સ્માર્ટફોન કે ડિજિટલ સાધનો વાપરવામાં તમને કેટલું અનુકૂળ લાગે છે?",
    "This helps us choose how much detail to show on each screen.":
        "આના પરથી અમે દરેક સ્ક્રીન પર કેટલી વિગત બતાવવી તે નક્કી કરીએ છીએ.",
    "Very comfortable": "ઘણું અનુકૂળ",
    "Somewhat comfortable": "થોડું અનુકૂળ",
    "I sometimes need help": "મને ક્યારેક મદદ જોઈએ છે",
    "I prefer a simpler experience": "મને સરળ અનુભવ ગમે છે",
    "How would you prefer to answer questions?": "તમે પ્રશ્નોના જવાબ કઈ રીતે આપવા ઇચ્છો છો?",
    "You can always switch between speaking and tapping later.":
        "બોલવા અને સ્પર્શ કરવા વચ્ચે તમે પછી પણ ક્યારેય બદલી શકો છો.",
    "By speaking": "બોલીને",
    "By touching options": "વિકલ્પોને સ્પર્શ કરીને",
    "Both": "બંને",
    "Do you have difficulty reading text on screens?":
        "સ્ક્રીન પરનું લખાણ વાંચવામાં તમને તકલીફ પડે છે?",
    "If reading is hard, we can make text larger and read questions aloud.":
        "વાંચવું અઘરું હોય, તો અમે લખાણ મોટું કરી શકીએ અને પ્રશ્નો મોટેથી વાંચી શકીએ.",
    "Do you have difficulty seeing content on screens?":
        "સ્ક્રીન પરનું જોવામાં તમને તકલીફ પડે છે?",
    "We can increase the text size and use stronger colour contrast.":
        "અમે લખાણનું માપ વધારી શકીએ અને રંગોનો ભેદ વધુ સ્પષ્ટ કરી શકીએ.",
    "Do you have difficulty hearing audio instructions?":
        "સંભળાવેલી સૂચનાઓ સાંભળવામાં તમને તકલીફ પડે છે?",
    "If hearing is hard, nothing in this app will depend on sound.":
        "સાંભળવું અઘરું હોય, તો આ ઍપમાં કંઈ પણ આવાજ પર આધારિત રહેશે નહીં.",
    "No difficulty": "કોઈ તકલીફ નથી",
    "Sometimes": "ક્યારેક",
    "Yes": "હા",
    "No": "ના",
    "Is there anything else that would make this easier for you?":
        "તમારા માટે આ વધુ સરળ બને એવું બીજું કંઈ છે?",
    "This is completely optional. Share only what you want to.":
        "આ સંપૂર્ણપણે મરજિયાત છે. તમે જે કહેવા ઇચ્છો તે જ કહો.",
    "I find reading and writing difficult": "મને વાંચવા-લખવામાં તકલીફ પડે છે",
    "I have low vision": "મને ઓછું દેખાય છે",
    "I am hard of hearing": "મને ઓછું સંભળાય છે",
    "Tapping the screen is tiring": "સ્ક્રીનને સ્પર્શ કરવું થકવનારું લાગે છે",
    "Someone is helping me today": "આજે કોઈ મારી મદદ કરે છે",
    "I use sign language": "હું સાંકેતિક ભાષા વાપરું છું",
    "Before we begin": "શરૂ કરતાં પહેલાં",
    "Speak your answers": "તમારા જવાબ બોલો",
    "Speak or tap, whichever suits": "બોલો કે સ્પર્શ કરો — જે અનુકૂળ હોય",
    "Tap to choose answers": "જવાબ પસંદ કરવા સ્પર્શ કરો",
    "One question at a time, large buttons": "એક સમયે એક પ્રશ્ન, મોટાં બટન",
    "All options on one screen": "બધા વિકલ્પો એક જ સ્ક્રીન પર",
    "Standard": "પ્રમાણભૂત",
    "Easy": "સરળ",
    "Normal": "સામાન્ય",
    "Large": "મોટું",
    "Extra large": "ઘણું મોટું",
    "Normal colours": "સામાન્ય રંગો",
    "High contrast": "વધુ સ્પષ્ટ રંગભેદ",
    "Voice": "આવાજ",
    "Touch": "સ્પર્શ",
    "Optional": "મરજિયાત",
    "Usually filled in from your date of birth.": "સામાન્યપણે તમારી જન્મતારીખ પરથી ભરાય છે.",
    "Your doctor needs this to understand your case before you walk in.":
        "તમે અંદર આવો તે પહેલાં તમારો કેસ સમજવા ડૉક્ટરને આ જરૂરી છે.",

    # --- Consent -------------------------------------------------------
    "Collecting your health information": "તમારી આરોગ્ય માહિતી એકઠી કરવી",
    "Your symptoms, past illnesses, surgeries, medicines, allergies and family history.":
        "તમારાં લક્ષણો, પહેલાંની બીમારીઓ, ઓપરેશન, દવાઓ, એલર્જી અને કૌટુંબિક ઇતિહાસ.",
    "So your doctor already knows your history and can spend the visit on your actual problem.":
        "જેથી તમારા ડૉક્ટરને તમારો ઇતિહાસ પહેલેથી ખબર હોય અને મુલાકાતનો સમય તમારી ખરી સમસ્યા પર વપરાય.",
    "It is stored against your patient record and shown to the clinician treating you.":
        "તે તમારા દર્દી રેકોર્ડ સાથે સાચવવામાં આવે છે અને તમારી સારવાર કરનાર ડૉક્ટરને બતાવવામાં આવે છે.",
    "Sharing with your doctor": "તમારા ડૉક્ટર સાથે વહેંચવું",
    "A summary of what you tell us today, and any records you upload.":
        "આજે તમે જે કહેશો તેનો સારાંશ, અને તમે અપલોડ કરેલા રેકોર્ડ.",
    "Only clinicians involved in your care can see it.":
        "ફક્ત તમારી સારવાર સાથે સંકળાયેલા ડૉક્ટરો જ તે જોઈ શકે છે.",
    "Linking your health ID": "તમારો હેલ્થ આઈડી જોડવો",
    "The health ID number you entered, linked to this patient record.":
        "તમે આપેલો હેલ્થ આઈડી નંબર, આ દર્દી રેકોર્ડ સાથે જોડાયેલો.",
    "So your records can follow you between visits instead of starting over.":
        "જેથી દરેક મુલાકાતે નવેસરથી શરૂ કરવાને બદલે તમારા રેકોર્ડ તમારી સાથે રહે.",
    "This is a prototype and is not connected to the national ABDM network.":
        "આ એક પ્રોટોટાઇપ છે અને રાષ્ટ્રીય ABDM નેટવર્ક સાથે જોડાયેલું નથી.",
    "We will ask about your health so your doctor is prepared before you meet. "
    "You choose what to share, and you can withdraw your consent at any time.":
        "તમારી મુલાકાત પહેલાં ડૉક્ટર તૈયાર હોય તે માટે અમે તમારા આરોગ્ય વિશે પૂછીશું. "
        "શું વહેંચવું તે તમે નક્કી કરો છો, અને તમારી સંમતિ તમે ક્યારેય પાછી ખેંચી શકો છો.",
    "You can withdraw consent later from your profile. Nothing is shared without your agreement.":
        "તમે પછી તમારી પ્રોફાઇલમાંથી સંમતિ પાછી ખેંચી શકો છો. તમારી સહમતિ વગર કંઈ પણ વહેંચાતું નથી.",

    # --- Red flags / safety --------------------------------------------
    "Please speak to healthcare staff now": "કૃપા કરીને હવે આરોગ્ય કર્મચારીઓ સાથે વાત કરો",
    "Some of the symptoms you described may require urgent medical attention.":
        "તમે જણાવેલાં કેટલાંક લક્ષણોને તાત્કાલિક તબીબી ધ્યાનની જરૂર પડી શકે છે.",
    "Please inform nearby healthcare staff immediately. Show them this screen.":
        "કૃપા કરીને નજીકના આરોગ્ય કર્મચારીઓને તરત જણાવો. તેમને આ સ્ક્રીન બતાવો.",
    "This does not confirm a medical condition. It only means a health worker should "
    "look at you sooner rather than later.":
        "આનાથી કોઈ બીમારી નક્કી થતી નથી. એનો અર્થ ફક્ત એટલો, કે આરોગ્ય કર્મચારીએ "
        "તમને મોડું નહીં, પણ વહેલું જોવું જોઈએ.",
    "Marked urgent — please stay near the staff desk.":
        "તાત્કાલિક તરીકે ચિહ્નિત — કૃપા કરીને સ્ટાફ ડેસ્ક પાસે રહો.",
    "Continue answering while waiting": "રાહ જોતાં જોતાં જવાબ આપતા રહો",
    "I need immediate assistance": "મને તાત્કાલિક મદદ જોઈએ છે",

    # --- Medical profile sections --------------------------------------
    "Why you are here": "તમે અહીં કેમ આવ્યા છો",
    "First, tell us what brings you in today.": "પહેલાં, આજે તમે શા માટે આવ્યા છો તે કહો.",
    "What problem brings you in today?": "આજે કઈ સમસ્યા માટે તમે આવ્યા છો?",
    "Describe it in your own words. You can speak instead of typing.":
        "તમારા શબ્દોમાં જણાવો. ટાઇપ કરવાને બદલે તમે બોલી શકો છો.",
    "e.g. chest pain for three days": "દા.ત. ત્રણ દિવસથી છાતીમાં દુખાવો",
    "About this problem": "આ સમસ્યા વિશે",
    "How long has it been there, and what makes it better or worse?":
        "આ કેટલા સમયથી છે, અને શાથી સારું કે વધારે લાગે છે?",
    "How long have you had this?": "આ તમને કેટલા સમયથી છે?",
    "A rough idea is fine.": "આશરે કહો તો પણ ચાલશે.",
    "Started today": "આજે શરૂ થયું",
    "2–3 days": "૨–૩ દિવસ",
    "About a week": "આશરે એક અઠવાડિયું",
    "A few weeks": "થોડાં અઠવાડિયાં",
    "More than a month": "એક મહિનાથી વધુ",
    "How much does it trouble you, from 1 to 10?": "આ તમને ૧ થી ૧૦ માં કેટલી તકલીફ આપે છે?",
    "1 is very mild, 10 is the worst.": "૧ એટલે ઘણું હળવું, ૧૦ એટલે સૌથી વધુ.",
    "Is there anything that makes it better or worse?":
        "શાથી તે સારું કે વધારે થાય એવું કંઈ છે?",
    "For example rest, food, walking, or a medicine you took.":
        "દાખલા તરીકે આરામ, ખોરાક, ચાલવું, કે તમે લીધેલી દવા.",
    "Anything else you feel": "તમને લાગતું બીજું કંઈ",
    "A quick check for other symptoms.": "બીજાં લક્ષણોની ઝડપી તપાસ.",
    "Are you also feeling any of these?": "તમને આમાંથી કંઈ લાગે છે?",
    "Choose as many as you like.": "તમને જોઈએ તેટલા વિકલ્પો પસંદ કરો.",
    "Fever": "તાવ",
    "Cough": "ખાંસી",
    "Breathlessness": "શ્વાસ ચઢવો",
    "Short of breath": "દમ ચઢવો",
    "Headache": "માથું દુખવું",
    "Dizziness": "ચક્કર",
    "Vomiting": "ઉલટી",
    "Loose motions": "ઝાડા",
    "Swelling": "સોજો",
    "Pain": "દુખાવો",
    "Very tired": "ઘણો થાક",
    "Losing weight": "વજન ઘટવું",
    "Not sleeping well": "ઊંઘ ન આવવી",
    "Stomach pain": "પેટમાં દુખાવો",
    "Stomach problem": "પેટની તકલીફ",
    "Chest pain": "છાતીમાં દુખાવો",

    # --- Past illnesses -------------------------------------------------
    "Past illnesses": "પહેલાંની બીમારીઓ",
    "Now a few questions about long-term health conditions.":
        "હવે લાંબા સમયની બીમારીઓ વિશે થોડા પ્રશ્નો.",
    "Has a doctor told you that you have a long-term illness?":
        "તમને લાંબા સમયની બીમારી છે એવું ડૉક્ટરે કહ્યું છે?",
    "Such as diabetes, blood pressure or asthma.": "જેમ કે ડાયાબિટીસ, બ્લડ પ્રેશર કે દમ.",
    "Any long-term illness you have been told you have?":
        "તમને છે એવું કહેવાયું હોય એવી કોઈ લાંબા સમયની બીમારી?",
    "Which illness?": "કઈ બીમારી?",
    "Any old illness?": "જૂની કોઈ બીમારી?",
    "Ongoing conditions": "ચાલુ બીમારીઓ",
    "Diabetes": "ડાયાબિટીસ",
    "High blood pressure": "ઊંચું બ્લડ પ્રેશર",
    "Asthma": "દમ",
    "Heart disease": "હૃદયરોગ",
    "Thyroid problem": "થાઇરોઇડની તકલીફ",
    "Tuberculosis": "ક્ષય રોગ",
    "Cancer": "કૅન્સર",
    "Something else": "બીજું કંઈ",
    "Are you currently taking medicine for {item}?":
        "{item} માટે તમે હાલમાં દવા લો છો?",
    "Do you remember the name of the medicine for {item}?":
        "{item} માટેની દવાનું નામ તમને યાદ છે?",
    "If you are not sure, you can skip this or upload the prescription later.":
        "ખાતરી ન હોય, તો આ છોડી દો કે પછી દવાની ચિઠ્ઠી અપલોડ કરો.",

    # --- Operations -----------------------------------------------------
    "Operations": "ઓપરેશન",
    "Have you ever had an operation?": "તમારું ક્યારેય ઓપરેશન થયું છે?",
    "Have you had any operation?": "તમારું કોઈ ઓપરેશન થયું છે?",
    "Any operation, however long ago.": "કોઈ પણ ઓપરેશન, ભલે કેટલું જૂનું હોય.",
    "What operation, and roughly when?": "કયું ઓપરેશન, અને આશરે ક્યારે?",
    "For example: gallbladder removed, 2019.": "દાખલા તરીકે: પિત્તાશય કઢાવ્યું, ૨૦૧૯.",
    "e.g. gallbladder removed, 2019": "દા.ત. પિત્તાશય કઢાવ્યું, ૨૦૧૯",

    # --- Medicines ------------------------------------------------------
    "Medicines": "દવાઓ",
    "Medicines you take": "તમે લેતી દવાઓ",
    "Let us record the medicines you take.": "તમે લેતી દવાઓ નોંધીએ.",
    "Which medicines do you take regularly?": "તમે નિયમિત કઈ દવાઓ લો છો?",
    "Which medicines are you taking now?": "તમે હાલમાં કઈ દવાઓ લો છો?",
    "Any daily medicine?": "રોજની કોઈ દવા?",
    "Include tablets, insulin, inhalers and drops.":
        "ગોળીઓ, ઇન્સ્યુલિન, ઇન્હેલર અને ટીપાં પણ જણાવો.",
    "Add them one at a time. Tap a common answer or say it aloud.":
        "એક સમયે એક ઉમેરો. સામાન્ય જવાબને સ્પર્શ કરો કે મોટેથી બોલો.",
    "Add them one at a time.": "એક સમયે એક ઉમેરો.",
    "e.g. Metformin 500 mg twice a day": "દા.ત. મેટફોર્મિન ૫૦૦ મિ.ગ્રા. દિવસમાં બે વાર",

    # --- Allergies ------------------------------------------------------
    "Allergies": "એલર્જી",
    "Medicine problems": "દવાની તકલીફ",
    "This one matters a lot for your safety.": "તમારી સલામતી માટે આ ઘણું મહત્ત્વનું છે.",
    "Are you allergic to any medicine or food?":
        "તમને કોઈ દવા કે ખોરાકની એલર્જી છે?",
    "Any allergy?": "કોઈ એલર્જી?",
    "Has any medicine ever caused you a problem?":
        "કોઈ દવાથી તમને ક્યારેય તકલીફ થઈ છે?",
    "Tell us even if you are unsure — it keeps you safe.":
        "ખાતરી ન હોય તો પણ કહો — તેથી તમે સલામત રહો છો.",
    "For example it upset your stomach, or you had to stop it.":
        "દાખલા તરીકે પેટ બગડ્યું, કે તે બંધ કરવી પડી.",
    "Which ones?": "કઈ કઈ?",
    "Penicillin": "પેનિસિલિન",
    "Aspirin": "એસ્પિરિન",
    "Sulfa drugs": "સલ્ફા દવાઓ",
    "Dust": "ધૂળ",
    "No known allergies": "જાણીતી કોઈ એલર્જી નથી",
    "e.g. penicillin, peanuts": "દા.ત. પેનિસિલિન, સિંગદાણા",
    "e.g. aspirin upset my stomach": "દા.ત. એસ્પિરિનથી મારું પેટ બગડ્યું",

    # --- Family and personal history ------------------------------------
    "Family health": "કૌટુંબિક આરોગ્ય",
    "Some illnesses run in families.": "કેટલીક બીમારીઓ કુટુંબમાં ચાલી આવે છે.",
    "Does any illness run in your close family?":
        "તમારા નજીકના કુટુંબમાં કોઈ બીમારી ચાલી આવે છે?",
    "Any illness that runs in your family?": "તમારા કુટુંબમાં ચાલી આવતી કોઈ બીમારી?",
    "Any illness in the family?": "કુટુંબમાં કોઈ બીમારી?",
    "Parents, brothers, sisters or children.": "માતા-પિતા, ભાઈ, બહેન કે સંતાનો.",
    "Family history": "કૌટુંબિક ઇતિહાસ",
    "e.g. mother has diabetes": "દા.ત. માતાને ડાયાબિટીસ છે",
    "Daily habits": "રોજની આદતો",
    "Daily life": "રોજનું જીવન",
    "A few questions about your habits and routine.":
        "તમારી આદતો અને દિનચર્યા વિશે થોડા પ્રશ્નો.",
    "Anything about your habits your doctor should know?":
        "તમારી આદતો વિશે ડૉક્ટરને ખબર હોવી જોઈએ એવું કંઈ છે?",
    "Which of these apply to you?": "આમાંથી કયું તમને લાગુ પડે છે?",
    "I do not smoke": "હું ધૂમ્રપાન કરતો/કરતી નથી",
    "I smoke": "હું ધૂમ્રપાન કરું છું",
    "I do not drink alcohol": "હું દારૂ પીતો/પીતી નથી",
    "I drink alcohol": "હું દારૂ પીઉં છું",
    "I exercise regularly": "હું નિયમિત કસરત કરું છું",
    "Vegetarian diet": "શાકાહારી આહાર",
    "Non-smoker": "ધૂમ્રપાન ન કરનાર",
    "Smoker": "ધૂમ્રપાન કરનાર",
    "No alcohol": "દારૂ નહીં",
    "What work do you do?": "તમે શું કામ કરો છો?",
    "Some jobs affect health, so this can be useful.":
        "કેટલાંક કામોની આરોગ્ય પર અસર થાય છે, તેથી આ ઉપયોગી થઈ શકે.",
    "e.g. non-smoker, vegetarian diet": "દા.ત. ધૂમ્રપાન ન કરનાર, શાકાહારી આહાર",
    "e.g. diabetes, high blood pressure": "દા.ત. ડાયાબિટીસ, ઊંચું બ્લડ પ્રેશર",

    # --- Investigations --------------------------------------------------
    "Earlier tests": "પહેલાંની તપાસ",
    "Earlier test results": "પહેલાંની તપાસનાં પરિણામ",
    "Any tests you have had done recently.": "તાજેતરમાં તમે કરાવેલી કોઈ તપાસ.",
    "Have you had any blood test or scan recently?":
        "તાજેતરમાં તમારી લોહીની તપાસ કે સ્કૅન થયું છે?",
    "Any recent test result you remember?":
        "તાજેતરનું કોઈ તપાસ પરિણામ તમને યાદ છે?",
    "In the last year or so.": "છેલ્લા એક વર્ષમાં.",
    "Which test, and what did it show?": "કઈ તપાસ, અને તેમાં શું આવ્યું?",
    "If you have the report, you can upload it in the next step instead.":
        "રિપોર્ટ હોય, તો પછીના પગલે તમે તે અપલોડ કરી શકો છો.",
    "e.g. HbA1c 8.4% in March": "દા.ત. માર્ચમાં HbA1c ૮.૪%",

    # --- Anything else ---------------------------------------------------
    "Anything else": "બીજું કંઈ",
    "Anything else you would like your doctor to know?":
        "તમારા ડૉક્ટરને ખબર હોવી જોઈએ એવું બીજું કંઈ છે?",
    "Are you also feeling anything else?": "તમને બીજું કંઈ પણ લાગે છે?",
    "Could you tell us a little more?": "તમે થોડું વધુ કહી શકશો?",
    "Yes or no is enough.": "હા કે ના એટલું બસ.",
    "Choose as many as apply.": "જે લાગુ પડે તે બધા પસંદ કરો.",
    "This question was suggested from what you just said. You can skip it.":
        "તમે હમણાં જે કહ્યું તેના પરથી આ પ્રશ્ન સૂચવાયો છે. તમે તે છોડી શકો છો.",
    "Optional questions used in Ayurvedic practice.":
        "આયુર્વેદિક પદ્ધતિમાં વપરાતા મરજિયાત પ્રશ્નો.",

    # --- Encounter script (today's visit) -------------------------------
    "Type of treatment": "સારવારનો પ્રકાર",
    "First, tell us which kind of care you are here for.":
        "પહેલાં, તમે કઈ પ્રકારની સારવાર માટે આવ્યા છો તે કહો.",
    "Which kind of treatment are you here for?":
        "તમે કઈ પ્રકારની સારવાર માટે આવ્યા છો?",
    "Which treatment?": "કઈ સારવાર?",
    "This decides which questions we ask. You can pick a different one next time.":
        "આના પરથી અમે કયા પ્રશ્નો પૂછીશું તે નક્કી થાય છે. આગલી વાર તમે બીજું પસંદ કરી શકો છો.",
    "Modern medicine (Allopathy)": "આધુનિક ચિકિત્સા (એલોપથી)",
    "Allopathy": "એલોપથી",
    "Ayurveda": "આયુર્વેદ",
    "Homoeopathy": "હોમિયોપથી",
    "Unani": "યુનાની",
    "Siddha": "સિદ્ધ",
    "Yoga & Naturopathy": "યોગ અને પ્રાકૃતિક ચિકિત્સા",
    "Yoga and Naturopathy": "યોગ અને પ્રાકૃતિક ચિકિત્સા",
    "I am not sure": "મને ખાતરી નથી",
    "Today's concern": "આજની ફરિયાદ",
    "A few questions about this problem only.": "ફક્ત આ સમસ્યા વિશે થોડા પ્રશ્નો.",
    "We already have your health history. Just tell us what is new.":
        "તમારો આરોગ્ય ઇતિહાસ અમારી પાસે છે. ફક્ત નવું શું છે તે કહો.",
    "Tell us what is troubling you today.": "આજે તમને શું તકલીફ છે તે કહો.",
    "What is troubling you today?": "આજે તમને શું તકલીફ છે?",
    "What is troubling you?": "તમને શું તકલીફ છે?",
    "What brings you here today?": "આજે તમે શા માટે આવ્યા છો?",
    "In your own words. You can speak instead of typing.":
        "તમારા શબ્દોમાં. ટાઇપ કરવાને બદલે તમે બોલી શકો છો.",
    "When did it start?": "આ ક્યારે શરૂ થયું?",
    "Since when?": "ક્યારથી?",
    "Today": "આજે",
    "Yesterday": "ગઈકાલે",
    "2–3 days ago": "૨–૩ દિવસ પહેલાં",
    "About a week ago": "આશરે એક અઠવાડિયા પહેલાં",
    "Longer than a week": "એક અઠવાડિયાથી વધુ",
    "A few details": "થોડી વિગત",
    "Can you describe it a little more?": "તમે આ વિશે થોડું વધુ કહી શકશો?",
    "For example where it is, what it feels like, or what makes it worse.":
        "દાખલા તરીકે તે ક્યાં છે, કેવું લાગે છે, કે શાથી વધે છે.",
    "How bad is it?": "કેટલી તકલીફ છે?",
    "How much is it troubling you, from 1 to 10?":
        "આ તમને ૧ થી ૧૦ માં કેટલી તકલીફ આપે છે?",
    "Is anything else happening as well?": "આ સાથે બીજું કંઈ થાય છે?",
    "Only choose what you actually feel.": "તમને ખરેખર લાગે તે જ પસંદ કરો.",
    "Have you taken anything for it?": "આ માટે તમે કંઈ લીધું છે?",
    "Any medicine or home remedy, even if it did not help.":
        "કોઈ પણ દવા કે ઘરગથ્થુ ઉપાય, ભલે તેનો ફાયદો ન થયો હોય.",
    "Anything changed?": "કંઈ બદલાયું છે?",
    "Have your regular medicines changed since your last visit?":
        "તમારી છેલ્લી મુલાકાત પછી તમારી નિયમિત દવાઓ બદલાઈ છે?",
    "We already have your earlier list — only tell us what changed.":
        "તમારી પહેલાંની યાદી અમારી પાસે છે — ફક્ત શું બદલાયું તે કહો.",
    "What has changed?": "શું બદલાયું છે?",
    "A medicine you started, stopped, or now take differently.":
        "તમે શરૂ કરેલી, બંધ કરેલી, કે હવે અલગ રીતે લેતી દવા.",
    "Has a doctor told you about any new condition since then?":
        "ત્યારથી ડૉક્ટરે તમને કોઈ નવી બીમારી વિશે કહ્યું છે?",
    "Only something new.": "ફક્ત નવું હોય તે.",
    "What was it?": "તે શું હતું?",
    "This is your space.": "આ તમારી જગ્યા છે.",
    "Anything else you want the doctor to know today?":
        "આજે ડૉક્ટરને ખબર હોવી જોઈએ એવું બીજું કંઈ છે?",
    "Only here for a check-up": "ફક્ત તપાસ માટે આવ્યો/આવી છું",
    "Hospital visit": "હૉસ્પિટલની મુલાકાત",

    # --- AYUSH: Dashavidha ----------------------------------------------
    "Ten-fold examination": "દશવિધ પરીક્ષા",
    "Dashavidha Pariksha — questions about your constitution.":
        "દશવિધ પરીક્ષા — તમારી પ્રકૃતિ વિશેના પ્રશ્નો.",
    "Prakriti": "પ્રકૃતિ",
    "Which best describes your natural build and temperament?":
        "તમારી કુદરતી બાંધો અને સ્વભાવ કયું સૌથી સારી રીતે વર્ણવે છે?",
    "Your lifelong tendency, not how you feel today.":
        "તમારી જીવનભરની પ્રકૃતિ, આજની સ્થિતિ નહીં.",
    "Vikriti": "વિકૃતિ",
    "How do you feel compared with your usual self?":
        "તમારી સામાન્ય સ્થિતિની સરખામણીમાં તમને કેવું લાગે છે?",
    "Your current state, today.": "તમારી આજની હાલની સ્થિતિ.",
    "Sara": "સાર",
    "How would you describe your overall vitality?":
        "તમારી એકંદર શક્તિનું વર્ણન તમે કેવી રીતે કરશો?",
    "How strong and resilient you generally feel.":
        "તમે સામાન્યપણે કેટલા મજબૂત અને સહનશીલ લાગો છો.",
    "Samhanana": "સંહનન",
    "How is your body build?": "તમારો શરીરનો બાંધો કેવો છે?",
    "Muscle and frame, in your own view.": "સ્નાયુ અને બાંધો, તમારા મતે.",
    "Pramana": "પ્રમાણ",
    "How would you describe your height and weight together?":
        "તમારી ઊંચાઈ અને વજન સાથે જોતાં તેનું વર્ણન કેવી રીતે કરશો?",
    "Roughly proportionate, or not.": "આશરે પ્રમાણસર, કે નહીં.",
    "Satmya": "સાત્મ્ય",
    "Which foods or conditions suit you well?":
        "કયા ખોરાક કે સ્થિતિ તમને સારી રીતે માફક આવે છે?",
    "What you tolerate easily.": "તમે સહેલાઈથી સહન કરી શકો તે.",
    "Sattva": "સત્ત્વ",
    "How do you usually handle stress?": "તણાવ તમે સામાન્યપણે કેવી રીતે સંભાળો છો?",
    "Your mental steadiness.": "તમારી માનસિક સ્થિરતા.",
    "Ahara Shakti": "આહાર શક્તિ",
    "How is your appetite and digestion?": "તમારી ભૂખ અને પાચન કેવું છે?",
    "How much you can eat and digest comfortably.":
        "તમે સહેલાઈથી કેટલું ખાઈ અને પચાવી શકો છો.",
    "Vyayama Shakti": "વ્યાયામ શક્તિ",
    "How much physical exertion can you manage?": "તમે કેટલો શારીરિક શ્રમ કરી શકો છો?",
    "Before you need to rest.": "આરામની જરૂર પડે તે પહેલાં.",
    "Vaya": "વય",
    "Which life stage are you in?": "તમે કઈ જીવન અવસ્થામાં છો?",

    # --- AYUSH: Ashtasthana ----------------------------------------------
    "Eight-fold examination": "અષ્ટસ્થાન પરીક્ષા",
    "Ashtasthana Pariksha — your practitioner will confirm each of these.":
        "અષ્ટસ્થાન પરીક્ષા — આમાંથી દરેકની તમારા વૈદ્ય ખાતરી કરશે.",
    "Only what you notice yourself.": "તમને પોતાને જે લાગે તે જ.",
    "Your own sense of it — a practitioner will check properly.":
        "આ વિશે તમારી પોતાની સમજ — વૈદ્ય યોગ્ય રીતે તપાસશે.",
    "Nadi": "નાડી",
    "How does your pulse or heartbeat usually feel?":
        "તમારી નાડી કે હૃદયના ધબકારા સામાન્યપણે કેવા લાગે છે?",
    "Mutra": "મૂત્ર",
    "How is your urine?": "તમારો પેશાબ કેવો છે?",
    "Colour, quantity and how often.": "રંગ, પ્રમાણ અને કેટલી વાર.",
    "Mala": "મળ",
    "How are your bowel movements?": "તમારી શૌચની ક્રિયા કેવી છે?",
    "Regularity and consistency.": "નિયમિતતા અને ઘનતા.",
    "Jihva": "જિહ્વા",
    "How does your tongue look and feel?": "તમારી જીભ કેવી દેખાય છે અને કેવી લાગે છે?",
    "Coating, dryness or taste in the mouth.": "જીભ પરનું આવરણ, સૂકાપણું કે મોંનો સ્વાદ.",
    "Shabda": "શબ્દ",
    "How is your voice at present?": "તમારો આવાજ હાલમાં કેવો છે?",
    "Strength and clarity when you speak.": "બોલતી વખતે જોર અને સ્પષ્ટતા.",
    "Sparsha": "સ્પર્શ",
    "How does your skin feel to touch?": "તમારી ત્વચા સ્પર્શમાં કેવી લાગે છે?",
    "Temperature, dryness or sweating.": "તાપમાન, સૂકાપણું કે પરસેવો.",
    "Drik": "દૃક્",
    "How are your eyes and vision?": "તમારી આંખો અને દૃષ્ટિ કેવી છે?",
    "Akriti": "આકૃતિ",
    "How would you describe your overall appearance now?":
        "તમારા એકંદર દેખાવનું વર્ણન હવે કેવી રીતે કરશો?",
    "How you look and feel compared with your usual self.":
        "તમારી સામાન્ય સ્થિતિની સરખામણીમાં તમે કેવા દેખાઓ છો અને કેવું લાગે છે.",

    # --- AYUSH: lifestyle -------------------------------------------------
    "Digestion, sleep and routine": "પાચન, ઊંઘ અને દિનચર્યા",
    "Agni, Nidra, Ahara and Vihara — how you eat, sleep and live.":
        "અગ્નિ, નિદ્રા, આહાર અને વિહાર — તમે કેવી રીતે ખાઓ, ઊંઘો અને જીવો છો.",
    "Agni": "અગ્નિ",
    "How well do you digest your food?": "તમારો ખોરાક કેટલો સારો પચે છે?",
    "Whether food feels heavy, or digests comfortably.":
        "ખોરાક ભારે લાગે છે, કે સહેલાઈથી પચે છે.",
    "Koshtha": "કોષ્ઠ",
    "How does your gut normally behave?": "તમારું પેટ સામાન્યપણે કેવું વર્તે છે?",
    "Nidra": "નિદ્રા",
    "How is your sleep?": "તમારી ઊંઘ કેવી છે?",
    "Falling asleep, staying asleep, and feeling rested.":
        "ઊંઘ આવવી, ટકવી, અને આરામ મળ્યાનું લાગવું.",
    "Manas": "મનસ્",
    "How has your mind felt lately?": "તાજેતરમાં તમારા મનને કેવું લાગ્યું છે?",
    "Only if you wish to say. This is recorded for your practitioner, not assessed here.":
        "તમે કહેવા ઇચ્છો તો જ. આ તમારા વૈદ્ય માટે નોંધાય છે, અહીં તેનું મૂલ્યાંકન થતું નથી.",
    "And your daily routine?": "અને તમારી દિનચર્યા?",
    "Which of these describe your diet?": "આમાંથી કયું તમારા આહારનું વર્ણન કરે છે?",
    "Ayurveda assessment": "આયુર્વેદ મૂલ્યાંકન",
    "Your usual tendency, not just today.": "તમારી સામાન્ય પ્રકૃતિ, ફક્ત આજની નહીં.",
    "These optional questions are used in Ayurvedic practice. They describe your "
    "constitution and routine — they are not a diagnosis, and you can skip any of them.":
        "આ મરજિયાત પ્રશ્નો આયુર્વેદિક પદ્ધતિમાં વપરાય છે. તે તમારી પ્રકૃતિ અને દિનચર્યા "
        "વર્ણવે છે — આ નિદાન નથી, અને તમે આમાંથી કોઈ પણ પ્રશ્ન છોડી શકો છો.",

    # --- Structured history section names --------------------------------
    "Chief complaint": "મુખ્ય ફરિયાદ",
    "History of present illness": "હાલની બીમારીનો ઇતિહાસ",
    "Past medical history": "પહેલાંનો તબીબી ઇતિહાસ",
    "Past surgical history": "પહેલાંનો ઓપરેશનનો ઇતિહાસ",
    "Medications": "દવાઓ",
    "Current medications": "હાલની દવાઓ",
    "Drug history": "દવાઓનો ઇતિહાસ",
    "Personal history": "વ્યક્તિગત ઇતિહાસ",
    "Previous investigations": "પહેલાંની તપાસ",
    "Review of systems": "તંત્રોની સમીક્ષા",
    "Additional information": "વધારાની માહિતી",
    "None reported": "કંઈ જણાવ્યું નથી",
    "Regarding this problem": "આ સમસ્યા વિશે",
    "Also reports": "આ પણ જણાવ્યું",

    # --- Narratives -------------------------------------------------------
    "The patient": "દર્દી",
    "{age}-year-old": "{age} વર્ષ",
    "no specific complaint": "કોઈ ખાસ ફરિયાદ નથી",
    "an unspecified concern": "અસ્પષ્ટ ફરિયાદ",
    "{subject} reports: {complaint}.": "{subject} ની ફરિયાદ: {complaint}.",
    "{subject} presents reporting: {complaint}.": "{subject} ની ફરિયાદ: {complaint}.",
    "{subject} returns reporting: {complaint}.":
        "{subject} ફરી આવ્યા છે, ફરિયાદ: {complaint}.",
    "{lead}: {found}.": "{lead}: {found}.",
    "{lead}: none reported.": "{lead}: કંઈ જણાવ્યું નથી.",
    "About this problem today: {items}.": "આજે આ સમસ્યા વિશે: {items}.",
    "Severity reported by the patient: {value}.": "દર્દીએ જણાવેલી તીવ્રતા: {value}.",
    "No further detail was given about the problem.":
        "સમસ્યા વિશે આનાથી વધુ વિગત આપવામાં આવી નથી.",
    "Also reported today: {items}.": "આજે આ પણ જણાવ્યું: {items}.",
    "Known conditions from earlier visits: {items}.":
        "પહેલાંની મુલાકાતોથી જાણીતી બીમારીઓ: {items}.",
    "Medications on record: {items}.": "રેકોર્ડમાંની દવાઓ: {items}.",
    "Allergies on record: {items}.": "રેકોર્ડમાંની એલર્જી: {items}.",
    "No allergies recorded.": "કોઈ એલર્જી નોંધાયેલી નથી.",
    "Medication changes reported today: {items}.": "આજે જણાવેલા દવાના ફેરફાર: {items}.",
    "New conditions reported today: {items}.": "આજે જણાવેલી નવી બીમારીઓ: {items}.",
    "This visit has been marked urgent because some described symptoms may require "
    "prompt attention.":
        "આ મુલાકાતને તાત્કાલિક તરીકે ચિહ્નિત કરવામાં આવી છે, કારણ કે જણાવેલાં કેટલાંક "
        "લક્ષણો પર જલદી ધ્યાન આપવાની જરૂર પડી શકે છે.",
    "Recorded from the patient's own account and their existing records. "
    "This is not a diagnosis.":
        "દર્દીએ પોતે જણાવ્યા મુજબ અને તેમના ઉપલબ્ધ રેકોર્ડ પરથી નોંધાયું છે. "
        "આ નિદાન નથી.",
    "This is a record of information provided by the patient and read from their "
    "documents. It is not a diagnosis.":
        "આ દર્દીએ આપેલી અને તેમના દસ્તાવેજોમાંથી વાંચેલી માહિતીની નોંધ છે. "
        "આ નિદાન નથી.",
    "This records what you told us today alongside what we already knew. It is not a "
    "diagnosis, and a healthcare professional will review it with you.":
        "આજે તમે જે કહ્યું અને અમને પહેલેથી જાણ હતી, એ બંનેની આ નોંધ છે. "
        "આ નિદાન નથી, અને એક આરોગ્ય વ્યાવસાયિક તમારી સાથે તે તપાસશે.",

    # --- Gender and care-system labels used in prose ----------------------
    "male": "પુરુષ",
    "female": "સ્ત્રી",
    "other": "અન્ય",
    "gender not stated": "લિંગ જણાવ્યું નથી",
    "not decided yet": "હજી નક્કી નથી",

    # --- Demo patients ----------------------------------------------------
    "Rajesh Kumar · 52": "રાજેશ કુમાર · ૫૨",
    "Returning patient, comfortable with digital forms. Standard mode.":
        "જૂના દર્દી, ડિજિટલ ફોર્મમાં સહજ. પ્રમાણભૂત પદ્ધતિ.",
    "Kamla Devi · 71": "કમલા દેવી · ૭૧",
    "Prefers a simpler experience. Easy mode with audio guidance.":
        "સરળ અનુભવ પસંદ કરે છે. આવાજ માર્ગદર્શન સાથે સરળ પદ્ધતિ.",
    "Anil Sharma · 45": "અનિલ શર્મા · ૪૫",
    "Low vision. Extra-large text and high contrast.":
        "ઓછી દૃષ્ટિ. ઘણું મોટું લખાણ અને વધુ સ્પષ્ટ રંગભેદ.",
    "Sunita Devi · 34": "સુનીતા દેવી · ૩૪",
    "First-time patient who stopped part-way through onboarding.":
        "પહેલી વાર આવેલાં દર્દી, જેમણે નોંધણી અધૂરી છોડી.",
    "e.g. three days, worse on walking": "દા.ત. ત્રણ દિવસ, ચાલવાથી વધારે",
    "e.g. very tired, losing weight": "દા.ત. ઘણો થાક, વજન ઘટવું",
}
