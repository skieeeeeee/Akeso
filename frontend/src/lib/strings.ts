/**
 * Static UI copy.
 *
 * Only chrome lives here — questions, consent text and medical-section
 * prompts are served by the API so the two clients can never disagree about
 * clinical wording. Adding a language means adding one key per entry and
 * extending the `Language` union.
 */
import { localised } from "@/services/apiClient";
import { overlay } from "@/lib/translations";
import type { Language } from "@/types/api";

export const STRINGS = {
  // --- App identity ------------------------------------------------------
  appName: { en: "MediKiosk", hi: "मेडीकियोस्क" },
  appTagline: {
    en: "Share your health information before your visit",
    hi: "अपनी मुलाक़ात से पहले अपनी स्वास्थ्य जानकारी साझा करें",
  },

  // --- Common actions ----------------------------------------------------
  continue: { en: "Continue", hi: "आगे बढ़ें" },
  back: { en: "Back", hi: "पीछे" },
  cancel: { en: "Cancel", hi: "रद्द करें" },
  save: { en: "Save", hi: "सहेजें" },
  saving: { en: "Saving…", hi: "सहेजा जा रहा है…" },
  saved: { en: "Saved", hi: "सहेजा गया" },
  retry: { en: "Try again", hi: "फिर कोशिश करें" },
  loading: { en: "Loading…", hi: "लोड हो रहा है…" },
  skip: { en: "Skip for now", hi: "अभी छोड़ें" },
  yes: { en: "Yes", hi: "हाँ" },
  no: { en: "No", hi: "नहीं" },
  optional: { en: "Optional", hi: "वैकल्पिक" },
  add: { en: "Add", hi: "जोड़ें" },
  remove: { en: "Remove", hi: "हटाएँ" },
  edit: { en: "Change", hi: "बदलें" },
  done: { en: "Done", hi: "पूर्ण" },
  close: { en: "Close", hi: "बंद करें" },
  signOut: { en: "Sign out", hi: "साइन आउट" },
  notProvided: { en: "Not provided", hi: "नहीं दिया गया" },

  // --- Welcome -----------------------------------------------------------
  welcomeHeading: {
    en: "Tell us about your health before you see the doctor",
    hi: "डॉक्टर से मिलने से पहले हमें अपने स्वास्थ्य के बारे में बताएं",
  },
  welcomeBody: {
    en: "Answer a few simple questions here. Your doctor sees your history before you walk in, so your visit is about you — not about filling forms.",
    hi: "यहाँ कुछ आसान सवालों के जवाब दें। आपके डॉक्टर आपके आने से पहले आपका इतिहास देख लेंगे, जिससे मुलाक़ात फ़ॉर्म भरने में नहीं, आप पर केंद्रित रहे।",
  },
  welcomeStart: { en: "Start", hi: "शुरू करें" },
  welcomeReturning: { en: "I have used MediKiosk before", hi: "मैंने पहले मेडीकियोस्क उपयोग किया है" },
  chooseLanguage: { en: "Choose your language", hi: "अपनी भाषा चुनें" },
  accessibilityShortcut: { en: "Make text bigger", hi: "टेक्स्ट बड़ा करें" },
  howItWorks: { en: "How it works", hi: "यह कैसे काम करता है" },
  step1Title: { en: "Sign in with your mobile", hi: "अपने मोबाइल से साइन इन करें" },
  step1Body: {
    en: "We send a one-time code. No password to remember.",
    hi: "हम एक बार का कोड भेजते हैं। कोई पासवर्ड याद रखने की ज़रूरत नहीं।",
  },
  step2Title: { en: "Answer simple questions", hi: "आसान सवालों के जवाब दें" },
  step2Body: {
    en: "Speak or tap — whichever is easier for you.",
    hi: "बोलें या छुएं — जो आपके लिए आसान हो।",
  },
  step3Title: { en: "Your doctor is ready", hi: "आपके डॉक्टर तैयार हैं" },
  step3Body: {
    en: "Your history is waiting for them, so nothing gets repeated.",
    hi: "आपका इतिहास उनके पास पहले से होगा, कुछ दोहराना नहीं पड़ेगा।",
  },
  welcomeConsent: {
    en: "Nothing is shared until you agree to it, and only with the clinician treating you.",
    hi: "जब तक आप सहमत न हों, कुछ भी साझा नहीं किया जाता — और केवल आपका इलाज करने वाले डॉक्टर के साथ।",
    mr: "तुम्ही संमती देईपर्यंत काहीही सामायिक केले जात नाही — आणि केवळ तुमचे उपचार करणाऱ्या डॉक्टरांसोबत.",
    ta: "நீங்கள் ஒப்புக்கொள்ளும் வரை எதுவும் பங்கிடப்படுவதில்லை — உங்களுக்குச் சிகிச்சை அளிக்கும் மருத்துவருடன் மட்டுமே.",
    gu: "તમે સંમતિ ન આપો ત્યાં સુધી કંઈ વહેંચાતું નથી — અને ફક્ત તમારી સારવાર કરનાર ડૉક્ટર સાથે.",
    pa: "ਜਦੋਂ ਤੱਕ ਤੁਸੀਂ ਸਹਿਮਤ ਨਹੀਂ ਹੁੰਦੇ, ਕੁਝ ਵੀ ਸਾਂਝਾ ਨਹੀਂ ਕੀਤਾ ਜਾਂਦਾ — ਅਤੇ ਸਿਰਫ਼ ਤੁਹਾਡਾ ਇਲਾਜ ਕਰਨ ਵਾਲੇ ਡਾਕਟਰ ਨਾਲ।",
  },
  privacyNote: {
    en: "You choose what to share. You can withdraw your consent at any time.",
    hi: "आप तय करते हैं कि क्या साझा करना है। आप सहमति कभी भी वापस ले सकते हैं।",
  },

  // --- Login -------------------------------------------------------------
  loginHeading: { en: "Sign in", hi: "साइन इन करें" },
  loginBody: {
    en: "Enter your mobile number and we will send a one-time code.",
    hi: "अपना मोबाइल नंबर दर्ज करें, हम एक बार का कोड भेजेंगे।",
  },
  mobileLabel: { en: "Mobile number", hi: "मोबाइल नंबर" },
  mobileHint: { en: "10-digit number, for example 98765 43210", hi: "10 अंकों का नंबर, जैसे 98765 43210" },
  sendCode: { en: "Send code", hi: "कोड भेजें" },
  sendingCode: { en: "Sending…", hi: "भेजा जा रहा है…" },
  codeLabel: { en: "One-time code", hi: "एक बार का कोड" },
  codeHint: { en: "6 digits", hi: "6 अंक" },
  verifyAndContinue: { en: "Verify and continue", hi: "सत्यापित करें और आगे बढ़ें" },
  verifying: { en: "Verifying…", hi: "सत्यापित हो रहा है…" },
  resendCode: { en: "Send a new code", hi: "नया कोड भेजें" },
  changeNumber: { en: "Use a different number", hi: "दूसरा नंबर उपयोग करें" },
  codeSentTo: { en: "Code sent to", hi: "कोड भेजा गया" },
  prototypeNoticeTitle: { en: "Prototype", hi: "प्रोटोटाइप" },
  prototypeNoticeBody: {
    en: "This demonstration does not send SMS. Use the code shown below.",
    hi: "यह प्रदर्शन SMS नहीं भेजता। नीचे दिखाया गया कोड उपयोग करें।",
  },
  demoHeading: { en: "Or explore with a demo patient", hi: "या डेमो रोगी के साथ देखें" },
  demoPatientBadge: { en: "Demo patient", hi: "डेमो रोगी" },
  demoBody: {
    en: "Fictional records for demonstration. No real patient data.",
    hi: "प्रदर्शन के लिए काल्पनिक रिकॉर्ड। कोई वास्तविक रोगी जानकारी नहीं।",
  },
  demoUnavailable: {
    en: "Demo patients are not loaded on this server yet.",
    hi: "इस सर्वर पर डेमो रोगी अभी लोड नहीं हैं।",
  },

  // --- ABHA --------------------------------------------------------------
  abhaHeading: { en: "Connect your health ID", hi: "अपनी हेल्थ आईडी जोड़ें" },
  abhaBody: {
    en: "If you have an ABHA number, connecting it keeps your records together between visits.",
    hi: "यदि आपके पास ABHA नंबर है, तो उसे जोड़ने से आपके रिकॉर्ड हर मुलाक़ात में एक साथ रहते हैं।",
  },
  abhaLabel: { en: "ABHA number or address", hi: "ABHA नंबर या पता" },
  abhaHint: {
    en: "14 digits, or an address like name@abdm",
    hi: "14 अंक, या name@abdm जैसा पता",
  },
  abhaConnect: { en: "Connect", hi: "जोड़ें" },
  abhaConnecting: { en: "Checking…", hi: "जाँच हो रही है…" },
  abhaSkip: { en: "I do not have one", hi: "मेरे पास नहीं है" },
  abhaMockNotice: {
    en: "Prototype: this checks the number's format locally. It is not connected to the national ABDM network.",
    hi: "प्रोटोटाइप: यह नंबर का प्रारूप स्थानीय रूप से जाँचता है। यह राष्ट्रीय ABDM नेटवर्क से जुड़ा नहीं है।",
  },
  abhaConnected: { en: "Health ID connected", hi: "हेल्थ आईडी जुड़ गई" },
  abhaWhyTitle: { en: "Why connect it?", hi: "इसे क्यों जोड़ें?" },
  abhaWhyBody: {
    en: "Your history follows you, so you never start from scratch at your next visit. You can also continue without it.",
    hi: "आपका इतिहास आपके साथ चलता है, अगली मुलाक़ात में नए सिरे से शुरू नहीं करना पड़ता। आप इसके बिना भी आगे बढ़ सकते हैं।",
  },

  // --- Personal information ---------------------------------------------
  personalHeading: { en: "Your details", hi: "आपकी जानकारी" },
  personalBody: {
    en: "This helps the hospital identify you correctly.",
    hi: "इससे अस्पताल आपकी सही पहचान कर पाता है।",
  },
  fullNameLabel: { en: "Full name", hi: "पूरा नाम" },
  fullNameHint: { en: "As written on your ID", hi: "जैसा आपकी आईडी पर लिखा है" },
  dobLabel: { en: "Date of birth", hi: "जन्म तिथि" },
  dobHint: { en: "We use this to work out your age", hi: "इससे हम आपकी उम्र निकालते हैं" },
  genderLabel: { en: "Gender", hi: "लिंग" },
  genderMale: { en: "Male", hi: "पुरुष" },
  genderFemale: { en: "Female", hi: "महिला" },
  genderOther: { en: "Other", hi: "अन्य" },
  genderUndisclosed: { en: "Prefer not to say", hi: "बताना नहीं चाहते" },
  languageLabel: { en: "Preferred language", hi: "पसंदीदा भाषा" },
  emergencyHeading: { en: "Emergency contact", hi: "आपातकालीन संपर्क" },
  emergencyBody: {
    en: "Someone the hospital can call if needed.",
    hi: "कोई व्यक्ति जिसे ज़रूरत पड़ने पर अस्पताल कॉल कर सके।",
  },
  emergencyNameLabel: { en: "Their name", hi: "उनका नाम" },
  emergencyNumberLabel: { en: "Their mobile number", hi: "उनका मोबाइल नंबर" },
  emergencyRelationLabel: { en: "Relationship to you", hi: "आपसे संबंध" },
  emergencyRelationHint: { en: "For example: spouse, son, neighbour", hi: "जैसे: पति/पत्नी, बेटा, पड़ोसी" },
  ageIs: { en: "Age", hi: "उम्र" },
  years: { en: "years", hi: "वर्ष" },

  // --- Assessment --------------------------------------------------------
  assessmentHeading: { en: "Let us set this up for you", hi: "इसे आपके लिए तैयार करें" },
  assessmentBody: {
    en: "A few quick questions so the screens suit you. There are no wrong answers, and you can change everything later.",
    hi: "कुछ छोटे सवाल जिससे स्क्रीन आपके अनुकूल हो। कोई जवाब गलत नहीं है, और आप सब कुछ बाद में बदल सकते हैं।",
  },
  assessmentQuestionOf: { en: "Question", hi: "सवाल" },
  assessmentOf: { en: "of", hi: "में से" },
  assessmentWhyTitle: { en: "Why we ask", hi: "हम क्यों पूछते हैं" },
  assessmentWhyBody: {
    en: "Your answers only change how this app looks and sounds. They are not medical questions and are never shared as a diagnosis.",
    hi: "आपके जवाब केवल यह बदलते हैं कि यह ऐप कैसा दिखता और सुनाई देता है। ये चिकित्सीय सवाल नहीं हैं और कभी निदान के रूप में साझा नहीं होते।",
  },
  assessmentSelectToContinue: { en: "Choose an option to continue", hi: "आगे बढ़ने के लिए विकल्प चुनें" },

  // --- Recommendation / preferences -------------------------------------
  recommendationHeading: { en: "We have set this up for you", hi: "हमने यह आपके लिए तैयार किया है" },
  recommendationBody: {
    en: "Based on your answers. Change anything you like — now or later.",
    hi: "आपके जवाबों के आधार पर। जो चाहें बदलें — अभी या बाद में।",
  },
  recommendationAccept: { en: "This looks good", hi: "यह ठीक है" },
  recommendationCustomise: { en: "Change these settings", hi: "ये सेटिंग बदलें" },
  recommendationApplying: { en: "Applying…", hi: "लागू हो रहा है…" },
  preferencesHeading: { en: "Your experience", hi: "आपका अनुभव" },
  interfaceModeLabel: { en: "Screen style", hi: "स्क्रीन शैली" },
  fontSizeLabel: { en: "Text size", hi: "टेक्स्ट का आकार" },
  contrastLabel: { en: "Colours", hi: "रंग" },
  audioGuidanceLabel: { en: "Read questions aloud", hi: "सवाल बोलकर सुनाएँ" },
  audioGuidanceHelp: {
    en: "We will speak each question. You can turn this off any time.",
    hi: "हम हर सवाल बोलकर सुनाएंगे। आप इसे कभी भी बंद कर सकते हैं।",
  },
  interactionLabel: { en: "How you answer", hi: "आप कैसे जवाब देंगे" },
  previewLabel: { en: "Preview", hi: "पूर्वावलोकन" },
  previewSample: {
    en: "This is how text will look on your screens.",
    hi: "आपकी स्क्रीन पर टेक्स्ट ऐसा दिखेगा।",
  },
  neverLockedNote: {
    en: "You are never locked into a setting. Change it from your profile whenever you want.",
    hi: "आप किसी सेटिंग में बंधे नहीं हैं। जब चाहें अपनी प्रोफ़ाइल से बदलें।",
  },

  // --- Consent -----------------------------------------------------------
  consentHeading: { en: "Your consent", hi: "आपकी सहमति" },
  consentAcceptAll: { en: "I agree", hi: "मैं सहमत हूँ" },
  consentDecline: { en: "I do not agree", hi: "मैं सहमत नहीं हूँ" },
  consentSubmitting: { en: "Recording…", hi: "दर्ज हो रहा है…" },
  consentRequiredTag: { en: "Needed to continue", hi: "आगे बढ़ने के लिए आवश्यक" },
  consentOptionalTag: { en: "Your choice", hi: "आपकी मर्ज़ी" },
  consentWhatLabel: { en: "What we collect", hi: "हम क्या एकत्र करते हैं" },
  consentWhyLabel: { en: "Why", hi: "क्यों" },
  consentHowLabel: { en: "How it is used", hi: "इसका उपयोग कैसे होता है" },
  consentDeclinedNotice: {
    en: "Without this we cannot collect your health information. You can still see your doctor as usual — you would just fill the form there instead.",
    hi: "इसके बिना हम आपकी स्वास्थ्य जानकारी एकत्र नहीं कर सकते। आप डॉक्टर से पहले की तरह मिल सकते हैं — फ़ॉर्म वहीं भरना होगा।",
  },
  consentListen: { en: "Listen to this", hi: "इसे सुनें" },
  consentStopListening: { en: "Stop", hi: "रोकें" },

  // --- Medical profile ---------------------------------------------------
  medicalHeading: { en: "Your health history", hi: "आपका स्वास्थ्य इतिहास" },
  medicalBody: {
    en: "Tell us once. Next time you only describe what is new.",
    hi: "एक बार बताएं। अगली बार आप केवल नई बात बताएंगे।",
  },
  medicalAddPlaceholder: { en: "Type here and press Add", hi: "यहाँ लिखें और जोड़ें दबाएँ" },
  medicalNothingToAdd: { en: "Nothing to add", hi: "कुछ जोड़ना नहीं है" },
  medicalQuickAdd: { en: "Common answers", hi: "सामान्य जवाब" },
  medicalItemsAdded: { en: "added", hi: "जोड़े गए" },
  medicalFinish: { en: "Finish", hi: "समाप्त करें" },
  medicalSectionOf: { en: "Section", hi: "भाग" },

  // --- Records / documents -----------------------------------------------
  recordsHeading: { en: "Previous medical records", hi: "पिछले चिकित्सा रिकॉर्ड" },
  recordsBody: {
    en: "Add a photo of a prescription, lab report or discharge summary. This is optional.",
    hi: "किसी पर्चे, लैब रिपोर्ट या डिस्चार्ज सारांश की फ़ोटो जोड़ें। यह वैकल्पिक है।",
  },
  recordsChooseFile: { en: "Choose a photo or PDF", hi: "फ़ोटो या PDF चुनें" },
  recordsUploading: { en: "Uploading…", hi: "अपलोड हो रहा है…" },
  recordsTypeLabel: { en: "What is this?", hi: "यह क्या है?" },
  recordsTitleLabel: { en: "Short description", hi: "संक्षिप्त विवरण" },
  recordsTitleHint: { en: "For example: Dr Mehta, March 2026", hi: "जैसे: डॉ. मेहता, मार्च 2026" },
  recordsEmptyTitle: { en: "No records added", hi: "कोई रिकॉर्ड नहीं जोड़ा" },
  recordsEmptyBody: {
    en: "You can add records now or later from your profile. Your doctor can see them either way.",
    hi: "आप रिकॉर्ड अभी या बाद में अपनी प्रोफ़ाइल से जोड़ सकते हैं। दोनों स्थिति में आपके डॉक्टर उन्हें देख सकते हैं।",
  },
  recordsStoredNote: {
    en: "Your records are saved and shown to your doctor as you uploaded them.",
    hi: "आपके रिकॉर्ड सहेजे गए हैं और आपके डॉक्टर को वैसे ही दिखाए जाएंगे जैसे आपने अपलोड किए।",
  },
  documentTypePrescription: { en: "Prescription", hi: "पर्चा" },
  documentTypeLabReport: { en: "Lab report", hi: "लैब रिपोर्ट" },
  documentTypeDischarge: { en: "Discharge summary", hi: "डिस्चार्ज सारांश" },
  documentTypeOther: { en: "Something else", hi: "कुछ और" },

  // --- Completion / profile ---------------------------------------------
  completeHeading: { en: "You are all set", hi: "आप तैयार हैं" },
  completeBody: {
    en: "Your health profile is saved. Show this screen at the reception desk.",
    hi: "आपकी स्वास्थ्य प्रोफ़ाइल सहेज दी गई है। इस स्क्रीन को रिसेप्शन पर दिखाएँ।",
  },
  completeViewProfile: { en: "View my profile", hi: "मेरी प्रोफ़ाइल देखें" },
  profileHeading: { en: "Your health profile", hi: "आपकी स्वास्थ्य प्रोफ़ाइल" },
  profileIdentity: { en: "Your details", hi: "आपकी जानकारी" },
  profileHealthId: { en: "Health ID", hi: "हेल्थ आईडी" },
  profileExperience: { en: "Your experience", hi: "आपका अनुभव" },
  profileHistory: { en: "Health history", hi: "स्वास्थ्य इतिहास" },
  profileRecords: { en: "Records", hi: "रिकॉर्ड" },
  profileConsents: { en: "Consent", hi: "सहमति" },
  profileVisits: { en: "Visits", hi: "मुलाक़ातें" },
  profileNoVisits: { en: "No visits recorded yet", hi: "अभी कोई मुलाक़ात दर्ज नहीं" },
  profileFinishOnboarding: { en: "Finish setting up", hi: "सेटअप पूरा करें" },
  profileIncompleteNotice: {
    en: "Your profile is not finished yet. Complete it so your doctor has your full history.",
    hi: "आपकी प्रोफ़ाइल अभी पूरी नहीं है। इसे पूरा करें जिससे आपके डॉक्टर के पास आपका पूरा इतिहास हो।",
  },
  profileItemsRecorded: { en: "items recorded", hi: "प्रविष्टियाँ दर्ज" },
  profileNextVisitNote: {
    en: "At your next visit you will only be asked what has changed.",
    hi: "अगली मुलाक़ात में आपसे केवल यह पूछा जाएगा कि क्या बदला है।",
  },

  // --- Voice -------------------------------------------------------------
  voiceTapToSpeak: { en: "Tap to speak", hi: "बोलने के लिए छुएं" },
  voiceListening: { en: "Listening…", hi: "सुन रहे हैं…" },
  voiceStop: { en: "Stop", hi: "रोकें" },
  voiceProcessing: { en: "Working out what you said…", hi: "आपकी बात समझ रहे हैं…" },
  voiceHeard: { en: "We heard", hi: "हमने सुना" },
  voiceConfirm: { en: "That is right", hi: "यह सही है" },
  voiceAgain: { en: "Say it again", hi: "फिर बोलें" },
  voiceTypeInstead: { en: "Type instead", hi: "टाइप करें" },
  voiceProblem: { en: "Voice input problem", hi: "आवाज़ इनपुट में दिक्कत" },
  ttsNoVoice: {
    en: "This device has no voice for the selected language, so questions cannot be read aloud. All text stays on screen.",
    hi: "इस डिवाइस में चुनी गई भाषा के लिए आवाज़ उपलब्ध नहीं है, इसलिए सवाल बोलकर नहीं सुनाए जा सकते। सारा टेक्स्ट स्क्रीन पर रहेगा।",
  },
  voiceUnavailable: {
    en: "Voice input is not available in this browser, so please type or tap your answers.",
    hi: "इस ब्राउज़र में आवाज़ इनपुट उपलब्ध नहीं है, कृपया टाइप करें या छूकर जवाब दें।",
  },

  // --- Interview ---------------------------------------------------------
  interviewHeading: { en: "Your health history", hi: "आपका स्वास्थ्य इतिहास" },
  interviewIntro: {
    en: "We will ask a few questions, one at a time. Speak or tap — whichever is easier.",
    hi: "हम एक-एक कर कुछ सवाल पूछेंगे। बोलें या छुएं — जो आसान हो।",
  },
  interviewStart: { en: "Start", hi: "शुरू करें" },
  interviewResume: { en: "Continue where you left off", hi: "जहाँ छोड़ा था वहाँ से जारी रखें" },
  interviewAboutThis: { en: "About", hi: "के बारे में" },
  interviewAiSuggested: { en: "Follow-up question", hi: "अनुवर्ती सवाल" },
  interviewAiFallback: {
    en: "Smart assistance is unavailable right now, so we are using our standard questions. Nothing you have answered is lost.",
    hi: "स्मार्ट सहायता अभी उपलब्ध नहीं है, इसलिए हम सामान्य सवाल पूछ रहे हैं। आपके दिए जवाब सुरक्षित हैं।",
  },
  interviewDone: { en: "That is everything we need", hi: "हमें इतनी ही जानकारी चाहिए थी" },
  interviewDoneBody: {
    en: "Next you can add old medical records, or go straight to reviewing what you told us.",
    hi: "अगले चरण में आप पुराने मेडिकल रिकॉर्ड जोड़ सकते हैं, या सीधे अपनी दी गई जानकारी देख सकते हैं।",
  },
  interviewAyushOffer: { en: "Include Ayurveda questions", hi: "आयुर्वेद के सवाल शामिल करें" },
  interviewAyushHelp: {
    en: "Optional. Used at AYUSH facilities to record your constitution and routine.",
    hi: "वैकल्पिक। आयुष केंद्रों में आपकी प्रकृति और दिनचर्या दर्ज करने के लिए।",
  },
  sectionOf: { en: "Part", hi: "भाग" },

  // --- Document intelligence --------------------------------------------
  docProcessing: { en: "Reading your document…", hi: "आपका दस्तावेज़ पढ़ा जा रहा है…" },
  docRead: { en: "Read this document", hi: "इस दस्तावेज़ को पढ़ें" },
  docRetry: { en: "Try reading again", hi: "फिर पढ़ने की कोशिश करें" },
  docFindings: { en: "Information found in this document", hi: "इस दस्तावेज़ में मिली जानकारी" },
  docFindingsNote: {
    en: "This is what the document appears to say. It is not a diagnosis — please check it and tell us if anything looks wrong.",
    hi: "दस्तावेज़ में यही लिखा प्रतीत होता है। यह निदान नहीं है — कृपया जाँचें और कुछ गलत लगे तो बताएं।",
  },
  docAccept: { en: "That is correct", hi: "यह सही है" },
  docReject: { en: "That is not right", hi: "यह सही नहीं है" },
  docAccepted: { en: "Confirmed by you", hi: "आपने पुष्टि की" },
  docRejected: { en: "You marked this wrong", hi: "आपने इसे गलत बताया" },
  docRawText: { en: "Show the text we read", hi: "पढ़ा गया टेक्स्ट दिखाएँ" },
  docDetailsHeading: {
    en: "Document details",
    hi: "दस्तावेज़ का विवरण",
    mr: "कागदपत्राचा तपशील",
    ta: "ஆவண விவரங்கள்",
    gu: "દસ્તાવેજની વિગત",
    pa: "ਕਾਗਜ਼ ਦਾ ਵੇਰਵਾ",
  },
  docDetailsNote: {
    en: "Read from the printed part of the document. Please check it.",
    hi: "दस्तावेज़ के छपे हिस्से से पढ़ा गया। कृपया इसे जाँच लें।",
    mr: "कागदपत्राच्या छापील भागातून वाचले. कृपया तपासा.",
    ta: "ஆவணத்தின் அச்சிடப்பட்ட பகுதியிலிருந்து படிக்கப்பட்டது. சரிபார்க்கவும்.",
    gu: "દસ્તાવેજના છાપેલા ભાગમાંથી વાંચ્યું. કૃપા કરીને તપાસો.",
    pa: "ਕਾਗਜ਼ ਦੇ ਛਪੇ ਹਿੱਸੇ ਤੋਂ ਪੜ੍ਹਿਆ। ਕਿਰਪਾ ਕਰਕੇ ਜਾਂਚੋ।",
  },
  docFacility: {
    en: "Hospital or clinic", hi: "अस्पताल या क्लिनिक", mr: "रुग्णालय किंवा दवाखाना",
    ta: "மருத்துவமனை அல்லது கிளினிக்", gu: "હૉસ્પિટલ કે ક્લિનિક", pa: "ਹਸਪਤਾਲ ਜਾਂ ਕਲੀਨਿਕ",
  },
  docClinician: {
    en: "Doctor", hi: "डॉक्टर", mr: "डॉक्टर", ta: "மருத்துவர்", gu: "ડૉક્ટર", pa: "ਡਾਕਟਰ",
  },
  docDepartment: {
    en: "Department", hi: "विभाग", mr: "विभाग", ta: "பிரிவு", gu: "વિભાગ", pa: "ਵਿਭਾਗ",
  },
  docPatientName: {
    en: "Patient name", hi: "मरीज़ का नाम", mr: "रुग्णाचे नाव",
    ta: "நோயாளியின் பெயர்", gu: "દર્દીનું નામ", pa: "ਮਰੀਜ਼ ਦਾ ਨਾਂ",
  },
  docPhone: {
    en: "Phone", hi: "फ़ोन", mr: "फोन", ta: "தொலைபேசி", gu: "ફોન", pa: "ਫ਼ੋਨ",
  },
  docDate: {
    en: "Date on document", hi: "दस्तावेज़ पर तारीख़", mr: "कागदपत्रावरील तारीख",
    ta: "ஆவணத்தில் உள்ள தேதி", gu: "દસ્તાવેજ પરની તારીખ", pa: "ਕਾਗਜ਼ ਉੱਤੇ ਤਾਰੀਖ਼",
  },
  docNoFindings: {
    en: "We could not pick out medicines or test values from this document. Handwritten notes are often not readable by scanning. Your document is saved and your doctor will read it themselves.",
    hi: "इस दस्तावेज़ से हम दवाइयाँ या जाँच के मान नहीं निकाल सके। हाथ से लिखे पर्चे स्कैन से अक्सर नहीं पढ़े जा सकते। आपका दस्तावेज़ सहेजा गया है और आपके डॉक्टर इसे स्वयं पढ़ेंगे।",
    mr: "या कागदपत्रातून आम्हाला औषधे किंवा तपासणीचे मूल्य काढता आले नाही. हाताने लिहिलेले पर्चे स्कॅनने बरेचदा वाचता येत नाहीत. तुमचे कागदपत्र सहेजले आहे आणि तुमचे डॉक्टर ते स्वतः वाचतील.",
    ta: "இந்த ஆவணத்திலிருந்து மருந்துகளையோ பரிசோதனை மதிப்புகளையோ பிரித்தெடுக்க முடியவில்லை. கையால் எழுதிய குறிப்புகளை வருடி படிக்க முடியாமல் போவது வழக்கம். உங்கள் ஆவணம் சேமிக்கப்பட்டுள்ளது, உங்கள் மருத்துவரே அதைப் படிப்பார்.",
    gu: "આ દસ્તાવેજમાંથી અમે દવાઓ કે તપાસના મૂલ્યો કાઢી ન શક્યા. હાથે લખેલી ચિઠ્ઠીઓ સ્કૅનથી ઘણીવાર વાંચી શકાતી નથી. તમારો દસ્તાવેજ સાચવેલો છે અને તમારા ડૉક્ટર તે પોતે વાંચશે.",
    pa: "ਇਸ ਕਾਗਜ਼ ਤੋਂ ਅਸੀਂ ਦਵਾਈਆਂ ਜਾਂ ਜਾਂਚ ਦੇ ਮੁੱਲ ਨਹੀਂ ਕੱਢ ਸਕੇ। ਹੱਥ ਨਾਲ ਲਿਖੀਆਂ ਪਰਚੀਆਂ ਸਕੈਨ ਨਾਲ ਕਈ ਵਾਰ ਪੜ੍ਹੀਆਂ ਨਹੀਂ ਜਾਂਦੀਆਂ। ਤੁਹਾਡਾ ਕਾਗਜ਼ ਸੰਭਾਲਿਆ ਗਿਆ ਹੈ ਅਤੇ ਤੁਹਾਡੇ ਡਾਕਟਰ ਇਸ ਨੂੰ ਆਪ ਪੜ੍ਹਨਗੇ।",
  },
  recordsScanNote: {
    en: "Printed prescriptions and lab reports scan best. Handwritten notes are often unreadable — upload them anyway, your doctor will read them.",
    hi: "छपे पर्चे और जाँच रिपोर्ट सबसे अच्छे स्कैन होते हैं। हाथ से लिखे पर्चे अक्सर नहीं पढ़े जाते — फिर भी अपलोड करें, आपके डॉक्टर उन्हें पढ़ लेंगे।",
    mr: "छापील पर्चे आणि तपासणी अहवाल सर्वोत्तम स्कॅन होतात. हाताने लिहिलेले बरेचदा वाचले जात नाहीत — तरीही अपलोड करा, तुमचे डॉक्टर ते वाचतील.",
    ta: "அச்சிடப்பட்ட மருந்துச் சீட்டுகளும் பரிசோதனை அறிக்கைகளும் நன்றாக வருடப்படும். கையெழுத்துக் குறிப்புகள் பெரும்பாலும் படிக்க முடியாதவை — இருப்பினும் பதிவேற்றுங்கள், உங்கள் மருத்துவர் படிப்பார்.",
    gu: "છાપેલી ચિઠ્ઠીઓ અને તપાસ રિપોર્ટ સૌથી સારી રીતે સ્કૅન થાય છે. હાથે લખેલી ઘણીવાર વંચાતી નથી — તો પણ અપલોડ કરો, તમારા ડૉક્ટર વાંચી લેશે.",
    pa: "ਛਪੀਆਂ ਪਰਚੀਆਂ ਅਤੇ ਜਾਂਚ ਰਿਪੋਰਟਾਂ ਸਭ ਤੋਂ ਵਧੀਆ ਸਕੈਨ ਹੁੰਦੀਆਂ ਹਨ। ਹੱਥ ਨਾਲ ਲਿਖੀਆਂ ਕਈ ਵਾਰ ਨਹੀਂ ਪੜ੍ਹੀਆਂ ਜਾਂਦੀਆਂ — ਫਿਰ ਵੀ ਅਪਲੋਡ ਕਰੋ, ਤੁਹਾਡੇ ਡਾਕਟਰ ਪੜ੍ਹ ਲੈਣਗੇ।",
  },
  labNormal: { en: "Within the printed range", hi: "छपी सीमा के भीतर" },
  labLow: { en: "Below the printed range", hi: "छपी सीमा से कम" },
  labHigh: { en: "Above the printed range", hi: "छपी सीमा से अधिक" },
  labUnclear: { en: "Could not be compared", hi: "तुलना नहीं हो सकी" },
  labDisclaimer: {
    en: "Values are compared only against the range printed on your report. A healthcare professional should review them.",
    hi: "मान केवल आपकी रिपोर्ट पर छपी सीमा से तुलना किए गए हैं। इन्हें किसी स्वास्थ्य पेशेवर को देखना चाहिए।",
  },

  // --- Timeline ----------------------------------------------------------
  timelineHeading: { en: "Your medical timeline", hi: "आपकी चिकित्सा समयरेखा" },
  timelineBody: {
    en: "Everything we know about, newest first.",
    hi: "हमें ज्ञात सब कुछ, नया पहले।",
  },
  timelineEmptyTitle: { en: "Nothing here yet", hi: "अभी कुछ नहीं" },
  timelineEmptyBody: {
    en: "Once you answer questions or add a record, it will appear here.",
    hi: "जब आप सवालों के जवाब देंगे या रिकॉर्ड जोड़ेंगे, यह यहाँ दिखेगा।",
  },
  timelineAll: { en: "Everything", hi: "सब कुछ" },
  timelineNeedsCheck: { en: "Needs your check", hi: "आपकी जाँच चाहिए" },
  timelineNoDate: { en: "No date on record", hi: "रिकॉर्ड पर तिथि नहीं" },

  // --- Review ------------------------------------------------------------
  reviewHeading: { en: "Check your information", hi: "अपनी जानकारी जाँचें" },
  reviewBody: {
    en: "Please look through this before we finish. You can change anything.",
    hi: "समाप्त करने से पहले कृपया इसे देख लें। आप कुछ भी बदल सकते हैं।",
  },
  reviewYouTold: { en: "You told us", hi: "आपने बताया" },
  reviewFromDocuments: { en: "From your documents", hi: "आपके दस्तावेज़ों से" },
  reviewMissing: { en: "Still missing", hi: "अभी बाकी" },
  reviewMissingBody: {
    en: "These are usually useful for your doctor. You can add them now or later.",
    hi: "ये आमतौर पर आपके डॉक्टर के लिए उपयोगी हैं। आप इन्हें अभी या बाद में जोड़ सकते हैं।",
  },
  reviewSummary: { en: "Summary for your doctor", hi: "आपके डॉक्टर के लिए सारांश" },
  reviewConfirm: { en: "This is correct — finish", hi: "यह सही है — समाप्त करें" },
  reviewEditSection: { en: "Change this", hi: "इसे बदलें" },
  reviewSourcePatient: { en: "You said this", hi: "आपने यह बताया" },
  reviewSourceDocument: { en: "Found in a document", hi: "एक दस्तावेज़ में मिला" },
  reviewNothingRecorded: { en: "Nothing recorded", hi: "कुछ दर्ज नहीं" },

  // --- AYUSH -------------------------------------------------------------
  ayushHeading: { en: "Ayurveda assessment", hi: "आयुर्वेद मूल्यांकन" },
  ayushSkip: { en: "Skip these questions", hi: "ये सवाल छोड़ें" },
  ayushInclude: { en: "Include them", hi: "इन्हें शामिल करें" },
  ayushDashavidha: { en: "Ten-fold examination", hi: "दशविध परीक्षा" },
  ayushDashavidhaHelp: {
    en: "Dashavidha Pariksha — your constitution and current state.",
    hi: "दशविध परीक्षा — आपकी प्रकृति और वर्तमान स्थिति।",
  },
  ayushAshtasthana: { en: "Eight-fold examination", hi: "अष्टस्थान परीक्षा" },
  ayushAshtasthanaHelp: {
    en: "Ashtasthana Pariksha. You describe what you notice; your practitioner examines and confirms each of these.",
    hi: "अष्टस्थान परीक्षा। आप जो महसूस करते हैं वह बताएं; आपके वैद्य इनमें से प्रत्येक की जाँच कर पुष्टि करेंगे।",
  },
  ayushLifestyle: { en: "Digestion, sleep and routine", hi: "पाचन, नींद और दिनचर्या" },
  ayushLifestyleHelp: {
    en: "Agni, Koshtha, Nidra and Manas.",
    hi: "अग्नि, कोष्ठ, निद्रा और मनस।",
  },
  ayushProgress: { en: "factors recorded", hi: "कारक दर्ज" },
  ayushOpenTitle: { en: "Ayurveda assessment", hi: "आयुर्वेद मूल्यांकन" },
  ayushOpenBody: {
    en: "Record your constitution, examination findings and routine for an Ayurvedic consultation.",
    hi: "आयुर्वेदिक परामर्श के लिए अपनी प्रकृति, परीक्षा निष्कर्ष और दिनचर्या दर्ज करें।",
  },
  ayushOpenAction: { en: "Open assessment", hi: "मूल्यांकन खोलें" },
  ayushNotDiagnostic: {
    en: "These answers are recorded for your practitioner. Nothing here is assessed or interpreted by the app.",
    hi: "ये जवाब आपके वैद्य के लिए दर्ज होते हैं। ऐप यहाँ कुछ भी आँकता या व्याख्या नहीं करता।",
  },
  careSystemLabel: { en: "Type of treatment", hi: "उपचार का प्रकार" },
  careSystemAllopathy: { en: "Modern medicine", hi: "आधुनिक चिकित्सा" },
  careSystemAyurveda: { en: "Ayurveda", hi: "आयुर्वेद" },
  careSystemPartialNote: {
    en: "We record which system you chose and ask about your diet and routine. Examination questions specific to this system are not built yet.",
    hi: "हम दर्ज करते हैं कि आपने कौन सी पद्धति चुनी और आपके आहार-विहार के बारे में पूछते हैं। इस पद्धति की विशिष्ट परीक्षा के सवाल अभी नहीं बने हैं।",
  },
  ayushAhara: { en: "Your diet (Ahara)", hi: "आपका आहार" },
  ayushVihara: { en: "Your routine (Vihara)", hi: "आपका विहार" },
  ayushRecordedHeading: {
    en: "Ayurvedic examination you answered",
    hi: "आपने जो आयुर्वेदिक परीक्षा दी",
  },
  ayushRecordedCount: {
    en: "{count} of {total} factors recorded",
    hi: "{total} में से {count} कारक दर्ज",
  },
  ayushSaved: { en: "Ayurveda details saved", hi: "आयुर्वेद जानकारी सहेजी गई" },

  // --- Landing page ------------------------------------------------------
  navHowItWorks: { en: "How it works", hi: "यह कैसे काम करता है" },
  navFeatures: { en: "Features", hi: "विशेषताएँ" },
  navForClinics: { en: "For clinics", hi: "क्लिनिक के लिए" },
  navLogIn: { en: "Log in", hi: "लॉग इन" },
  navRegister: { en: "Register", hi: "रजिस्टर करें" },
  navKiosk: { en: "Kiosk mode", hi: "कियोस्क मोड" },

  landingHeadline: {
    en: "Your doctor should already know your story before you walk in",
    hi: "जब आप अंदर आएँ, आपके डॉक्टर को आपकी कहानी पहले से पता होनी चाहिए",
    mr: "तुम्ही आत जाताच तुमच्या डॉक्टरांना तुमची गोष्ट आधीच माहीत असावी",
    ta: "நீங்கள் உள்ளே செல்லும் போது உங்கள் மருத்துவருக்கு உங்கள் கதை முன்பே தெரிந்திருக்க வேண்டும்",
    gu: "તમે અંદર જાઓ ત્યારે તમારા ડૉક્ટરને તમારી વાત પહેલેથી જ ખબર હોવી જોઈએ",
    pa: "ਜਦੋਂ ਤੁਸੀਂ ਅੰਦਰ ਜਾਓ ਤਾਂ ਤੁਹਾਡੇ ਡਾਕਟਰ ਨੂੰ ਤੁਹਾਡੀ ਕਹਾਣੀ ਪਹਿਲਾਂ ਹੀ ਪਤਾ ਹੋਣੀ ਚਾਹੀਦੀ ਹੈ",
  },
  landingSubhead: {
    en: "MediKiosk collects a patient's medical history before the consultation — by voice, in their own language — so the few minutes with the doctor are spent on the problem, not on paperwork.",
    hi: "मेडीकियोस्क परामर्श से पहले रोगी का चिकित्सा इतिहास एकत्र करता है — उनकी भाषा में, बोलकर — जिससे डॉक्टर के साथ मिले कुछ मिनट काग़ज़ी काम में नहीं, समस्या पर लगें।",
  },
  landingPrimaryCta: { en: "Try the patient flow", hi: "रोगी प्रवाह देखें" },
  landingSecondaryCta: { en: "See a demo patient", hi: "डेमो रोगी देखें" },

  landingProblemTitle: { en: "The problem is time", hi: "समस्या समय की है" },
  landingProblemBody: {
    en: "A patient repeats their history at every visit. The clinician spends most of a very short consultation writing it down. Both lose, and the record still ends up thin.",
    hi: "रोगी हर मुलाक़ात में अपना इतिहास दोहराता है। चिकित्सक बहुत छोटे परामर्श का अधिकांश समय उसे लिखने में लगाता है। दोनों का नुक़सान होता है, और रिकॉर्ड फिर भी अधूरा रहता है।",
  },
  landingStatsTitle: { en: "Why it matters here", hi: "यह यहाँ क्यों मायने रखता है" },
  landingStatsNote: {
    en: "Figures are published estimates, shown with their source and year. Please re-check them against the latest release before citing.",
    hi: "ये प्रकाशित अनुमान हैं, अपने स्रोत और वर्ष के साथ दिखाए गए। उद्धृत करने से पहले कृपया नवीनतम आँकड़ों से मिला लें।",
  },

  landingTickerLabel: { en: "Illustrative arithmetic", hi: "उदाहरणात्मक गणना" },
  landingTickerBefore: { en: "In the", hi: "इन" },
  landingTickerMiddle: {
    en: "you have spent on this page, a doctor working at India's average pace would have seen about",
    hi: "में जो आपने इस पेज पर बिताए, भारत की औसत गति से काम करने वाले डॉक्टर ने लगभग",
  },
  landingTickerAfter: { en: "patients.", hi: "रोगी देख लिए होंगे।" },
  landingTickerBasis: {
    en: "Derived from the average consultation length, not a live measurement",
    hi: "औसत परामर्श अवधि से निकाला गया, कोई सजीव माप नहीं",
  },

  landingHowTitle: { en: "How it works", hi: "यह कैसे काम करता है" },
  landingHow1: { en: "Before the visit", hi: "मुलाक़ात से पहले" },
  landingHow1Body: {
    en: "The patient answers simple questions at a kiosk or on their phone — speaking or tapping, in English or an Indian language.",
    hi: "रोगी कियोस्क या अपने फ़ोन पर आसान सवालों के जवाब देता है — बोलकर या छूकर, अंग्रेज़ी या किसी भारतीय भाषा में।",
  },
  landingHow2: { en: "Old records are read", hi: "पुराने रिकॉर्ड पढ़े जाते हैं" },
  landingHow2Body: {
    en: "A photo of a prescription or lab report is scanned, and the medicines, diagnoses and test values found in it are listed for the patient to confirm.",
    hi: "पर्चे या लैब रिपोर्ट की फ़ोटो स्कैन की जाती है, और उसमें मिली दवाइयाँ, निदान और जाँच के मान रोगी की पुष्टि के लिए दिखाए जाते हैं।",
  },
  landingHow3: { en: "The clinician gets a history", hi: "चिकित्सक को इतिहास मिलता है" },
  landingHow3Body: {
    en: "A structured summary, with each fact labelled as reported by the patient, read from a document, or already on record.",
    hi: "एक संरचित सारांश, जिसमें प्रत्येक तथ्य पर अंकित होता है कि वह रोगी ने बताया, दस्तावेज़ से पढ़ा गया, या पहले से दर्ज था।",
  },
  landingReturningTitle: { en: "The second visit is the point", hi: "दूसरी मुलाक़ात ही असली बात है" },
  landingReturningBody: {
    en: "A returning patient does not repeat anything. They describe what is wrong today, and the questions adapt around what is already known.",
    hi: "लौटने वाला रोगी कुछ नहीं दोहराता। वह बताता है कि आज क्या तकलीफ़ है, और सवाल उस जानकारी के आसपास ढल जाते हैं जो पहले से मौजूद है।",
  },

  landingFeaturesTitle: { en: "What it does", hi: "यह क्या करता है" },
  featVoiceTitle: { en: "Voice, in your language", hi: "आपकी भाषा में आवाज़" },
  featVoiceBody: {
    en: "Speak your answers and correct the transcription before it is saved. Typing and tapping are always available — voice is never required.",
    hi: "अपने जवाब बोलें और सहेजने से पहले लिखावट सुधारें। टाइप करना और छूना हमेशा उपलब्ध है — आवाज़ कभी अनिवार्य नहीं।",
  },
  featAccessTitle: { en: "Built for every patient", hi: "हर रोगी के लिए बनाया गया" },
  featAccessBody: {
    en: "A short comfort check suggests text size, contrast, audio and a simpler screen layout. Age alone never decides it, and the patient can override anything.",
    hi: "एक छोटी सुविधा जाँच टेक्स्ट आकार, कंट्रास्ट, आवाज़ और आसान स्क्रीन सुझाती है। केवल उम्र से कभी तय नहीं होता, और रोगी कुछ भी बदल सकता है।",
  },
  featOcrTitle: { en: "Reads old records", hi: "पुराने रिकॉर्ड पढ़ता है" },
  featOcrBody: {
    en: "Prescriptions and lab reports are scanned on the server. Lab values are compared only against the range printed on the report — never guessed.",
    hi: "पर्चे और लैब रिपोर्ट सर्वर पर स्कैन होते हैं। जाँच के मान केवल रिपोर्ट पर छपी सीमा से तुलना किए जाते हैं — कभी अनुमान नहीं।",
  },
  featSafetyTitle: { en: "Flags what should not wait", hi: "जो इंतज़ार न कर सके, उसे चिह्नित करता है" },
  featSafetyBody: {
    en: "Answers are screened for presentations that need prompt attention. The patient is told to speak to staff, and the flag cannot be switched off from the kiosk.",
    hi: "जवाबों की जाँच होती है कि कहीं तत्काल ध्यान की ज़रूरत न हो। रोगी को कर्मचारियों से बात करने को कहा जाता है, और यह चिह्न कियोस्क से हटाया नहीं जा सकता।",
  },
  featAyushTitle: { en: "Allopathy and AYUSH", hi: "एलोपैथी और आयुष" },
  featAyushBody: {
    en: "The patient chooses which system of medicine they are here for. An Ayurvedic visit adds the Dashavidha and Ashtasthana examination; an allopathic visit stays short.",
    hi: "रोगी चुनता है कि वह किस चिकित्सा पद्धति के लिए आया है। आयुर्वेदिक मुलाक़ात में दशविध और अष्टस्थान परीक्षा जुड़ती है; एलोपैथिक मुलाक़ात छोटी रहती है।",
  },
  featConsentTitle: { en: "Consent, and nothing implied", hi: "सहमति, और कुछ भी अप्रत्यक्ष नहीं" },
  featConsentBody: {
    en: "Health information is collected only after the patient agrees, per purpose, and consent can be withdrawn. Health-ID linkage is prepared for ABDM but not connected.",
    hi: "स्वास्थ्य जानकारी रोगी की सहमति के बाद ही एकत्र होती है, प्रत्येक उद्देश्य के लिए, और सहमति वापस ली जा सकती है। हेल्थ आईडी ABDM के लिए तैयार है, जुड़ी नहीं।",
  },

  landingSafetyTitle: { en: "What it does not do", hi: "यह क्या नहीं करता" },
  landingSafetyBody: {
    en: "MediKiosk does not diagnose, does not prescribe, and does not replace a clinician. It organises what the patient tells us and what their documents say, and labels which is which.",
    hi: "मेडीकियोस्क निदान नहीं करता, दवा नहीं लिखता, और चिकित्सक का विकल्प नहीं है। यह रोगी की बताई बात और उनके दस्तावेज़ों की जानकारी को व्यवस्थित करता है, और बताता है कि कौन-सी कौन है।",
  },

  landingSpecsTitle: { en: "Specifications", hi: "विवरण" },
  specStack: { en: "Stack", hi: "तकनीक" },
  specStackBody: {
    en: "React and TypeScript on the front, FastAPI and PostgreSQL behind, as a modular monolith. Alembic migrations, Docker images for both halves.",
    hi: "आगे React और TypeScript, पीछे FastAPI और PostgreSQL, एक मॉड्यूलर मोनोलिथ के रूप में। Alembic माइग्रेशन, दोनों के लिए Docker इमेज।",
  },
  specData: { en: "Clinical data", hi: "चिकित्सीय डेटा" },
  specDataBody: {
    en: "Every fact carries its source, confidence and whether a person has verified it. A new visit never overwrites the historical record.",
    hi: "प्रत्येक तथ्य के साथ उसका स्रोत, विश्वास स्तर और यह दर्ज होता है कि किसी व्यक्ति ने उसकी पुष्टि की या नहीं। नई मुलाक़ात पुराने रिकॉर्ड को कभी नहीं बदलती।",
  },
  specAi: { en: "AI", hi: "एआई" },
  specAiBody: {
    en: "The interview is a deterministic state machine. A model may help read an answer or a document, but its output is schema-validated and every path works with AI switched off.",
    hi: "साक्षात्कार एक निर्धारित स्टेट मशीन है। मॉडल किसी जवाब या दस्तावेज़ को पढ़ने में मदद कर सकता है, पर उसका आउटपुट स्कीमा से जाँचा जाता है और एआई बंद होने पर भी हर रास्ता काम करता है।",
  },
  specLanguages: { en: "Languages", hi: "भाषाएँ" },
  specLanguagesBody: {
    en:
      "All six languages are complete: English, Hindi, Marathi, Tamil, Gujarati and Punjabi. The four regional translations are machine-authored and marked for review by a speaker of each; anything still untranslated falls back rather than breaking.",
    hi: "छहों भाषाएँ पूर्ण हैं: अंग्रेज़ी, हिन्दी, मराठी, तमिल, गुजराती और पंजाबी। चारों क्षेत्रीय अनुवाद मशीन से किए गए हैं और उन भाषाओं के वक्ताओं की समीक्षा के लिए चिह्नित हैं; जो अभी अनूदित नहीं है वह टूटने के बजाय वापस दूसरी भाषा पर आ जाता है।",
  },
  specFailure: { en: "Failure behaviour", hi: "विफलता व्यवहार" },
  specFailureBody: {
    en: "No workflow depends on one external service. If AI, voice, scanning or the health-ID service is unavailable, the patient keeps going and nothing already entered is lost.",
    hi: "कोई भी प्रक्रिया एक बाहरी सेवा पर निर्भर नहीं है। यदि एआई, आवाज़, स्कैनिंग या हेल्थ आईडी सेवा उपलब्ध न हो, तो रोगी आगे बढ़ता रहता है और दर्ज की गई जानकारी नहीं जाती।",
  },
  specAccess: { en: "Accessibility", hi: "सुगम्यता" },
  specAccessBody: {
    en: "Keyboard navigable, visible focus, semantic landmarks, large touch targets, and status never conveyed by colour alone.",
    hi: "कीबोर्ड से चलने योग्य, दिखने वाला फ़ोकस, अर्थपूर्ण लैंडमार्क, बड़े टच लक्ष्य, और स्थिति कभी केवल रंग से नहीं बताई जाती।",
  },

  landingClinicTitle: { en: "For clinics", hi: "क्लिनिक के लिए" },
  landingClinicBody: {
    en: "Runs on a tablet at reception or on the patient's own phone. Records live in your PostgreSQL database, and the schema is shaped for the clinician view that comes next.",
    hi: "रिसेप्शन पर टैबलेट या रोगी के अपने फ़ोन पर चलता है। रिकॉर्ड आपके PostgreSQL डेटाबेस में रहते हैं, और स्कीमा उस चिकित्सक दृश्य के लिए बना है जो आगे आ रहा है।",
  },
  landingClosingTitle: { en: "See it work", hi: "इसे चलते देखें" },
  landingClosingBody: {
    en: "Sign in with a mobile number, or open a demo patient with a full history already on file.",
    hi: "मोबाइल नंबर से साइन इन करें, या पूरा इतिहास पहले से मौजूद डेमो रोगी खोलें।",
  },
  landingPrototypeNote: {
    en: "Prototype. All demo patients and medical records are fictional. Health-ID verification is simulated and not connected to ABDM.",
    hi: "प्रोटोटाइप। सभी डेमो रोगी और चिकित्सा रिकॉर्ड काल्पनिक हैं। हेल्थ आईडी सत्यापन नक़ली है और ABDM से जुड़ा नहीं है।",
  },

  // --- Returning patient home -------------------------------------------
  homeStartVisit: { en: "Start a new health visit", hi: "नई स्वास्थ्य मुलाक़ात शुरू करें" },
  homeStartVisitHelp: {
    en: "Tell us what is troubling you today. We already have your history.",
    hi: "बताएं आज आपको क्या तकलीफ़ है। आपका इतिहास हमारे पास है।",
  },
  homeResumeVisit: { en: "Continue your visit", hi: "अपनी मुलाक़ात जारी रखें" },
  homeYourHealth: { en: "Your health summary", hi: "आपका स्वास्थ्य सारांश" },
  homeConditions: { en: "Ongoing conditions", hi: "चल रही बीमारियाँ" },
  homeMedications: { en: "Your medicines", hi: "आपकी दवाइयाँ" },
  homeAllergies: { en: "Allergies", hi: "एलर्जी" },
  homeRecentRecords: { en: "Recent records", hi: "हाल के रिकॉर्ड" },
  homeRecentActivity: { en: "Recent activity", hi: "हाल की गतिविधि" },
  homeLastVisit: { en: "Last visit", hi: "पिछली मुलाक़ात" },
  homeVisitCount: { en: "visits recorded", hi: "मुलाक़ातें दर्ज" },
  homeProfileIncomplete: { en: "Finish setting up your profile", hi: "अपनी प्रोफ़ाइल पूरी करें" },
  homeNothingYet: { en: "Nothing recorded yet", hi: "अभी कुछ दर्ज नहीं" },
  homeNoRecordsTitle: { en: "You have not added any medical records yet", hi: "आपने अभी कोई मेडिकल रिकॉर्ड नहीं जोड़ा" },
  homeNoRecordsBody: {
    en: "A photo of a prescription or lab report helps your doctor see your history.",
    hi: "किसी पर्चे या लैब रिपोर्ट की फ़ोटो आपके डॉक्टर को आपका इतिहास देखने में मदद करती है।",
  },
  homeNoAllergies: { en: "No allergies recorded", hi: "कोई एलर्जी दर्ज नहीं" },
  homeViewAll: { en: "View all", hi: "सब देखें" },
  homeUpdateHistory: { en: "Update my health history", hi: "मेरा स्वास्थ्य इतिहास अपडेट करें" },

  // --- New visit ---------------------------------------------------------
  visitHeading: { en: "What brings you here today?", hi: "आज आप यहाँ किस वजह से आए हैं?" },
  visitBody: {
    en: "Describe it in your own words — speak, type, or tap a common answer.",
    hi: "अपने शब्दों में बताएं — बोलें, टाइप करें, या कोई सामान्य जवाब छुएं।",
  },
  visitBegin: { en: "Continue", hi: "आगे बढ़ें" },
  visitWeKnow: { en: "We already know about", hi: "हमें पहले से पता है" },
  visitWeKnowHelp: {
    en: "You will not be asked about these again. You can update them from your profile.",
    hi: "इनके बारे में फिर नहीं पूछा जाएगा। आप इन्हें अपनी प्रोफ़ाइल से अपडेट कर सकते हैं।",
  },
  visitTodayOnly: { en: "About today only", hi: "केवल आज के बारे में" },
  visitNewInfo: { en: "New today", hi: "आज नया" },
  visitExistingInfo: { en: "Already on record", hi: "पहले से दर्ज" },
  visitDone: { en: "That is everything for today", hi: "आज के लिए इतना ही" },
  visitDoneBody: {
    en: "Please check what you told us before we send it to the care team.",
    hi: "देखभाल टीम को भेजने से पहले कृपया अपनी दी गई जानकारी जाँच लें।",
  },
  visitReview: { en: "Check and submit", hi: "जाँचें और भेजें" },

  // --- Emergency / red flag ---------------------------------------------
  urgentBadge: { en: "Marked urgent", hi: "अत्यावश्यक चिह्नित" },
  urgentBanner: {
    en: "Marked urgent — please stay near the staff desk.",
    hi: "अत्यावश्यक चिह्नित — कृपया स्टाफ़ डेस्क के पास रहें।",
  },
  urgentWhy: { en: "What you told us", hi: "आपने हमें क्या बताया" },
  urgentCannotRemove: {
    en: "A member of staff will review this with you. This cannot be turned off from here.",
    hi: "कोई कर्मचारी इसे आपके साथ देखेगा। इसे यहाँ से बंद नहीं किया जा सकता।",
  },
  urgentAssistanceSent: {
    en: "Staff have been notified. Please stay where you are.",
    hi: "कर्मचारियों को सूचित कर दिया गया है। कृपया वहीं रहें।",
  },

  // --- Encounter review -------------------------------------------------
  encounterReviewHeading: { en: "Check today's visit", hi: "आज की मुलाक़ात जाँचें" },
  encounterReviewBody: {
    en: "Please make sure this is right. You can change today's answers.",
    hi: "कृपया देख लें कि यह सही है। आप आज के जवाब बदल सकते हैं।",
  },
  encounterTodayConcern: { en: "Today's concern", hi: "आज की तकलीफ़" },
  encounterFollowUps: { en: "What you told us today", hi: "आज आपने क्या बताया" },
  encounterSkipped: { en: "questions you chose to skip", hi: "सवाल जो आपने छोड़े" },
  encounterSeverity: { en: "How much it troubles you", hi: "यह आपको कितना परेशान करता है" },
  encounterSeverityScale: { en: "out of 10", hi: "10 में से" },
  encounterUrgentReason: {
    en: "This rating is not what made your visit urgent — that came from the symptoms you described.",
    hi: "आपकी मुलाक़ात इस अंक से अत्यावश्यक नहीं हुई — वह आपके बताए लक्षणों से हुई।",
  },
  encounterRelevantHistory: { en: "Relevant existing history", hi: "संबंधित पिछला इतिहास" },
  encounterHistoryNote: {
    en: "From your earlier visits. Editing this happens in your health history, not here.",
    hi: "आपकी पिछली मुलाक़ातों से। इसे आपके स्वास्थ्य इतिहास में बदला जाता है, यहाँ नहीं।",
  },
  encounterDocsToday: { en: "Records added today", hi: "आज जोड़े गए रिकॉर्ड" },
  encounterEditToday: { en: "Change today's answers", hi: "आज के जवाब बदलें" },
  encounterSummary: { en: "Summary for the care team", hi: "देखभाल टीम के लिए सारांश" },
  encounterMissing: { en: "Still needed", hi: "अभी आवश्यक" },
  encounterConfirmHeading: { en: "Before you send this", hi: "इसे भेजने से पहले" },
  encounterConfirmSymptoms: {
    en: "My current symptoms were recorded correctly",
    hi: "मेरे वर्तमान लक्षण सही दर्ज किए गए हैं",
  },
  encounterConfirmReviewed: {
    en: "I have reviewed the information above",
    hi: "मैंने ऊपर दी गई जानकारी देख ली है",
  },
  encounterConfirmUnderstands: {
    en: "I understand this will be used to support my healthcare visit",
    hi: "मैं समझता/समझती हूँ कि इसका उपयोग मेरी स्वास्थ्य देखभाल में सहायता के लिए होगा",
  },
  encounterSubmit: { en: "Send to the care team", hi: "देखभाल टीम को भेजें" },
  encounterSubmitting: { en: "Sending…", hi: "भेजा जा रहा है…" },
  encounterSubmitted: { en: "Sent", hi: "भेज दिया गया" },
  encounterSubmittedHeading: { en: "Your visit has been sent", hi: "आपकी मुलाक़ात भेज दी गई" },
  encounterBackHome: { en: "Back to home", hi: "होम पर जाएँ" },
  encounterAlreadySubmitted: {
    en: "This visit has already been sent. Start a new visit if something has changed.",
    hi: "यह मुलाक़ात पहले ही भेजी जा चुकी है। कुछ बदला हो तो नई मुलाक़ात शुरू करें।",
  },

  // --- Settings ----------------------------------------------------------
  settingsHeading: { en: "Settings", hi: "सेटिंग" },
  settingsBody: {
    en: "Change how MediKiosk looks and sounds. Your answers are not affected.",
    hi: "बदलें कि मेडीकियोस्क कैसा दिखता और सुनाई देता है। आपके जवाब प्रभावित नहीं होंगे।",
  },
  settingsSaved: { en: "Settings saved", hi: "सेटिंग सहेजी गई" },
  settingsRetake: { en: "Retake the comfort check", hi: "सुविधा जाँच फिर से करें" },
  settingsRetakeHelp: {
    en: "Optional. We will suggest settings again based on your answers.",
    hi: "वैकल्पिक। हम आपके जवाबों के आधार पर फिर सेटिंग सुझाएंगे।",
  },
  settingsLanguage: { en: "Language", hi: "भाषा" },

  // --- Errors ------------------------------------------------------------
  errorGeneric: {
    en: "Something went wrong. Please try again.",
    hi: "कुछ गड़बड़ हो गई। कृपया फिर कोशिश करें।",
  },
  errorNetwork: {
    en: "We could not reach the server. Check the connection and try again.",
    hi: "हम सर्वर से संपर्क नहीं कर सके। कनेक्शन जाँचें और फिर कोशिश करें।",
  },
  errorSessionExpired: {
    en: "Your session has ended. Please sign in again.",
    hi: "आपका सत्र समाप्त हो गया। कृपया फिर साइन इन करें।",
  },
  errorRequired: { en: "This is needed to continue", hi: "आगे बढ़ने के लिए यह आवश्यक है" },
  statApproximately: { en: "about", hi: "लगभग" },
  demoShow: {
    en: "Show",
    hi: "दिखाएँ",
    mr: "दाखवा",
    ta: "காட்டு",
    gu: "બતાવો",
    pa: "ਦਿਖਾਓ",
  },
  demoHide: {
    en: "Hide",
    hi: "छिपाएँ",
    mr: "लपवा",
    ta: "மறை",
    gu: "છુપાવો",
    pa: "ਲੁਕਾਓ",
  },
  stepperLabel: {
    en: "Onboarding progress",
    hi: "पंजीकरण की प्रगति",
    mr: "नोंदणीची प्रगती",
    ta: "பதிவின் நிலை",
    gu: "નોંધણીની પ્રગતિ",
    pa: "ਰਜਿਸਟਰੇਸ਼ਨ ਦੀ ਪ੍ਰਗਤੀ",
  },
  stepperPosition: {
    en: "Step {current} of {total}",
    hi: "चरण {current} / {total}",
    mr: "टप्पा {current} / {total}",
    ta: "படி {current} / {total}",
    gu: "પગલું {current} / {total}",
    pa: "ਕਦਮ {current} / {total}",
  },
  skipToContent: { en: "Skip to main content", hi: "मुख्य सामग्री पर जाएँ" },
  timelineFoundIn: { en: "Found in {name}", hi: "{name} में मिला" },
  progressSavedNote: {
    en: "Your answers are saved as you go — you can stop and come back.",
    hi: "आपके जवाब साथ-साथ सहेजे जाते हैं — आप रुककर वापस आ सकते हैं।",
  },

  // --- Universal Navigation & Portal ------------------------------------
  navHome: { en: "Home", hi: "होम", mr: "होम", ta: "முகப்பு", gu: "હોમ", pa: "ਹੋਮ" },
  navRecords: { en: "Records", hi: "रिकॉर्ड", mr: "नोंदी", ta: "பதிவுகள்", gu: "રેકોર્ડ્સ", pa: "ਰਿਕਾਰਡ" },
  navTimeline: { en: "Timeline", hi: "टाइमलाइन", mr: "टाइमलाइन", ta: "காலவரிசை", gu: "સમયરેખા", pa: "ਸਮਾਂ-ਰੇਖਾ" },
  navProfile: { en: "Profile", hi: "प्रोफ़ाइल", mr: "प्रोफाइल", ta: "சுயவிவரம்", gu: "પ્રોફાઇલ", pa: "ਪ੍ਰੋਫਾਈਲ" },
  navSettings: { en: "Settings", hi: "सेटिंग्स", mr: "सेटिंग्ज", ta: "அமைப்புகள்", gu: "સેટિંગ્સ", pa: "ਸੈਟਿੰਗਾਂ" },
  backToHome: { en: "Back to home", hi: "होम पर वापस जाएँ", mr: "होमवर परत जा", ta: "முகப்புக்குத் திரும்பு", gu: "હોમ પર પાછા જાઓ", pa: "ਹੋਮ 'ਤੇ ਵਾਪਸ ਜਾਓ" },

  // --- Login Experience --------------------------------------------------
  loginSecureBadge: {
    en: "Shared only with your consent",
    hi: "केवल आपकी सहमति से साझा",
    mr: "केवळ तुमच्या संमतीने सामायिक",
    ta: "உங்கள் ஒப்புதலுடன் மட்டுமே பங்கிடப்படும்",
    gu: "ફક્ત તમારી સંમતિથી વહેંચાય છે",
    pa: "ਸਿਰਫ਼ ਤੁਹਾਡੀ ਸਹਿਮਤੀ ਨਾਲ ਸਾਂਝਾ",
  },
  loginHeroHeading: {
    en: "Healthcare built around your story",
    hi: "आपकी कहानी के इर्द-गिर्द बनी स्वास्थ्य सेवा",
    mr: "तुमच्या आरोग्याची काळजी, एकाच ठिकाणी",
    ta: "உங்களுக்காக அமைக்கப்பட்ட மருத்துவ தளம்",
    gu: "તમારી જરૂરિયાતો અનુસાર બનાવેલ આરોગ્ય સેવા",
    pa: "ਤੁਹਾਡੀ ਦੇਖਭਾਲ ਲਈ ਤਿਆਰ ਕੀਤਾ ਸਿਹਤ ਮੰਚ",
  },
  loginHeroSubhead: {
    en: "Access your saved medical records, complete pre-visit check-ins, or share today's symptoms with your doctor.",
    hi: "अपने सहेजे गए मेडिकल रिकॉर्ड देखें, मुलाक़ात से पहले जाँच पूरी करें, या आज के लक्षण अपने डॉक्टर से साझा करें।",
    mr: "तुमच्या आरोग्य नोंदी पाहण्यासाठी किंवा आजची लक्षणे सांगण्यासाठी साइन इन करा.",
    ta: "உங்கள் மருத்துவ பதிவுகளைப் பார்க்க அல்லது அறிகுறிகளைப் பகிர உள்நுழையவும்.",
    gu: "તમારા તબીબી રેકોર્ડ્સ જોવા અથવા લક્ષણો શેર કરવા માટે સાઇન ઇન કરો.",
    pa: "ਆਪਣੇ ਮੈਡੀਕਲ ਰਿਕਾਰਡ ਦੇਖਣ ਜਾਂ ਲੱਛਣ ਸਾਂਝੇ ਕਰਨ ਲਈ ਸਾਈਨ ਇਨ ਕਰੋ।",
  },
  loginFeature1Title: {
    en: "Never repeat your history",
    hi: "इतिहास दोहराने की ज़रूरत नहीं",
    mr: "इतिहास पुन्हा सांगण्याची गरज नाही",
    ta: "உங்கள் வரலாற்றை மீண்டும் கூற வேண்டாம்",
    gu: "તમારો ઈતિહાસ ફરીથી કહેવાની જરૂર નથી",
    pa: "ਆਪਣਾ ਇਤਿਹਾਸ ਦੁਹਰਾਉਣ ਦੀ ਲੋੜ ਨਹੀਂ",
  },
  loginFeature1Body: {
    en: "Your standing medical history is securely saved once and available for every visit.",
    hi: "आपकी स्थायी स्वास्थ्य जानकारी एक बार सुरक्षित रूप से सहेजी जाती है और हर मुलाक़ात में उपलब्ध रहती है।",
    mr: "तुमची वैद्यकीय माहिती एकाच वेळी सुरक्षित ठेवली जाते.",
    ta: "உங்கள் மருத்துவ வரலாறு ஒரு முறை பாதுகாப்பாக சேமிக்கப்படும்.",
    gu: "તમારી તબીબી માહિતી એકવાર સુરક્ષિત રીતે સચવાય છે.",
    pa: "ਤੁਹਾਡੀ ਸਿਹਤ ਜਾਣਕਾਰੀ ਇੱਕ ਵਾਰ ਸੁਰੱਖਿਅਤ ਰੱਖੀ ਜਾਂਦੀ ਹੈ।",
  },
  loginFeature2Title: {
    en: "Accessible and multilingual",
    hi: "सुलभ और बहुभाषी",
    mr: "सुलभ आणि बहुभाषिक",
    ta: "அணுகக்கூடிய மற்றும் பலமொழிகள்",
    gu: "સુલભ અને બહુભાષી",
    pa: "ਪਹੁੰਚਯੋਗ ਅਤੇ ਬਹੁ-ਭਾਸ਼ਾਈ",
  },
  loginFeature2Body: {
    en: "Voice dictation, large font sizing, high contrast, and audio instructions tailored to you.",
    hi: "आपकी सुविधा के लिए वॉइस इनपुट, बड़े फॉन्ट, उच्च कंट्रास्ट और ऑडियो मार्गदर्शन की व्यवस्था।",
    mr: "व्हॉइस इनपुट, मोठे फॉन्ट आणि ऑडिओ मार्गदर्शन.",
    ta: "குரல் உள்ளீடு, பெரிய எழுத்துக்கள் மற்றும் ஆடியோ வழிகாட்டுதல்.",
    gu: "વૉઇસ ઇનપુટ, મોટા ફોન્ટ્સ અને ઑડિયો માર્ગદર્શન.",
    pa: "ਵੌਇਸ ਇਨਪੁਟ, ਵੱਡੇ ਫੌਂਟ ਅਤੇ ਆਡੀਓ ਮਾਰਗਦਰਸ਼ਨ।" },
  loginFeature3Title: {
    en: "AI that never decides",
    hi: "एआई जो निर्णय नहीं लेता",
    mr: "निर्णय न घेणारे एआय",
    ta: "முடிவெடுக்காத ஏஐ",
    gu: "નિર્ણય ન લેતું એઆઈ",
    pa: "ਫ਼ੈਸਲਾ ਨਾ ਲੈਣ ਵਾਲਾ ਏਆਈ",
  },
  loginFeature3Body: {
    en: "AI only helps read your answers and your documents. Every finding is labelled with where it came from and shown to you to confirm. Nothing here is a diagnosis.",
    hi: "एआई केवल आपके जवाब और दस्तावेज़ पढ़ने में मदद करता है। हर जानकारी के साथ लिखा होता है कि वह कहाँ से आई, और पुष्टि के लिए आपको दिखाई जाती है। यहाँ कुछ भी निदान नहीं है।",
    mr: "एआय फक्त तुमची उत्तरे आणि कागदपत्रे वाचण्यात मदत करते. प्रत्येक माहितीसोबत ती कुठून आली हे लिहिलेले असते, आणि खात्रीसाठी ती तुम्हाला दाखवली जाते. येथे काहीही निदान नाही.",
    ta: "ஏஐ உங்கள் பதில்களையும் ஆவணங்களையும் படிக்க மட்டுமே உதவுகிறது. ஒவ்வொரு தகவலுடனும் அது எங்கிருந்து வந்தது என்று குறிக்கப்பட்டு, உறுதிப்படுத்த உங்களுக்குக் காட்டப்படும். இங்கே எதுவும் நோய் கண்டறிதல் அல்ல.",
    gu: "એઆઈ ફક્ત તમારા જવાબો અને દસ્તાવેજો વાંચવામાં મદદ કરે છે. દરેક માહિતી સાથે તે ક્યાંથી આવી તે લખેલું હોય છે, અને ખાતરી માટે તમને બતાવાય છે. આ નિદાન નથી.",
    pa: "ਏਆਈ ਸਿਰਫ਼ ਤੁਹਾਡੇ ਜਵਾਬ ਅਤੇ ਕਾਗਜ਼ ਪੜ੍ਹਨ ਵਿੱਚ ਮਦਦ ਕਰਦਾ ਹੈ। ਹਰ ਜਾਣਕਾਰੀ ਨਾਲ ਲਿਖਿਆ ਹੁੰਦਾ ਹੈ ਕਿ ਉਹ ਕਿੱਥੋਂ ਆਈ, ਅਤੇ ਪੁਸ਼ਟੀ ਲਈ ਤੁਹਾਨੂੰ ਦਿਖਾਈ ਜਾਂਦੀ ਹੈ। ਇੱਥੇ ਕੁਝ ਵੀ ਨਿਦਾਨ ਨਹੀਂ ਹੈ।",
  },

  // --- Sample Personas (Testing) -----------------------------------------
  samplePersonasTitle: {
    en: "Demo Personas for Evaluation",
    hi: "मूल्यांकन के लिए डेमो प्रोफ़ाइल",
    mr: "चाचणीसाठी डेमो प्रोफाईल",
    ta: "மதிப்பீட்டிற்கான மாதிரி சுயவிவரங்கள்",
    gu: "મૂલ્યાંકન માટે ડેમો પ્રોફાઇલ્સ",
    pa: "ਮੁਲਾਂਕਣ ਲਈ ਡੈਮੋ ਪ੍ਰੋਫਾਈਲਾਂ",
  },
  samplePersonasSubtitle: {
    en: "Explore MediKiosk with pre-configured fictional patient scenarios (No real data)",
    hi: "पूर्व-कॉन्फ़िगर किए गए काल्पनिक रोगी परिदृश्यों के साथ मेडीकियोस्क देखें (कोई वास्तविक डेटा नहीं)",
    mr: "काल्पनिक रुग्ण प्रोफाइलसह मेडीकियोस्क एक्सप्लोर करा (वास्तविक डेटा नाही)",
    ta: "மாதிரி நோயாளி சுயவிவரங்களுடன் மெடிகியோஸ்க்கை ஆராயுங்கள் (உண்மையான தரவு இல்லை)",
    gu: "કાલ્પનિક દર્દી પ્રોફાઇલ્સ સાથે મેડિકિઓસ્ક અન્વેષણ કરો (વાસ્તવિક ડેટા નથી)",
    pa: "ਕਾਲਪਨਿਕ ਮਰੀਜ਼ ਪ੍ਰੋਫਾਈਲਾਂ ਨਾਲ ਮੈਡੀਕਿਓਸਕ ਦੀ ਪੜਚੋਲ ਕਰੋ (ਕੋਈ ਅਸਲ ਡਾਟਾ ਨਹੀਂ)",
  },
  samplePersonaStandard: {
    en: "Returning Patient Demo",
    hi: "पुराने मरीज़ का डेमो",
    mr: "परत येणाऱ्या रुग्णाचा डेमो",
    ta: "மீண்டும் வரும் நோயாளி மாதிரி",
    gu: "પાછા ફરતા દર્દીનો ડેમો",
    pa: "ਵਾਪਸ ਆਉਣ ਵਾਲੇ ਮਰੀਜ਼ ਦਾ ਡੈਮੋ",
  },
  samplePersonaEasy: {
    en: "Easy Mode & Audio Demo",
    hi: "आसान मोड और ऑडियो डेमो",
    mr: "सोपा मोड आणि ऑडिओ डेमो",
    ta: "எளிதான பயன்முறை மற்றும் ஆடியோ மாதிரி",
    gu: "સરળ મોડ અને ઑડિયો ડેમો",
    pa: "ਆਸਾਨ ਮੋਡ ਅਤੇ ਆਡੀਓ ਡੈਮੋ",
  },
  samplePersonaLowVision: {
    en: "High Contrast / Large Text Demo",
    hi: "उच्च कंट्रास्ट / बड़े टेक्स्ट का डेमो",
    mr: "उच्च कॉन्ट्रास्ट / मोठा मजकूर डेमो",
    ta: "உயர் மாறுபாடு / பெரிய உரை மாதிரி",
    gu: "ઉચ્ચ કોન્ટ્રાસ્ટ / મોટા ટેક્સ્ટ ડેમો",
    pa: "ਉੱਚ ਕੰਟ੍ਰਾਸਟ / ਵੱਡਾ ਟੈਕਸਟ ਡੈਮੋ",
  },
  samplePersonaIncomplete: {
    en: "Partial Onboarding Resumption",
    hi: "अधूरी प्रोफ़ाइल फिर शुरू करने का डेमो",
    mr: "अपूर्ण प्रोफाइल पुन्हा सुरू करण्याचा डेमो",
    ta: "அரைகுறை சுயவிவர தொடர்ச்சி",
    gu: "અપૂર્ણ પ્રોફાઇલ ફરી શરૂ કરવાનો ડેમો",
    pa: "ਅਧੂਰੀ ਪ੍ਰੋਫਾਈਲ ਮੁੜ ਸ਼ੁਰੂ ਕਰਨ ਦਾ ਡੈਮੋ",
  },

  // --- Clinical Transparency & Consultation Readiness -------------------
  aiVerificationNotice: {
    en: "Clinician Review Required: This draft summary was generated to assist your doctor. All clinical information is reviewed and verified during your consultation.",
    hi: "चिकित्सक समीक्षा आवश्यक: यह मसौदा सारांश आपके डॉक्टर की सहायता के लिए तैयार किया गया है। परामर्श के दौरान आपके चिकित्सक द्वारा सभी जानकारी की समीक्षा और सत्यापन किया जाता है।",
    mr: "वैद्यकीय पुनरावलोकन आवश्यक: हा मसुदा तुमच्या डॉक्टरांच्या मदतीसाठी तयार केला आहे. भेटीदरम्यान सर्व माहितीची पडताळणी केली जाते.",
    ta: "மருத்துவ மதிப்பாய்வு தேவை: இந்த சுருக்கம் உங்கள் மருத்துவருக்கு உதவ உருவாக்கப்பட்டது. அனைத்து தகவல்களும் ஆலோசனையின் போது சரிபார்க்கப்படும்.",
    gu: "તબીબી સમીક્ષા આવશ્યક: આ સારાંશ તમારા ડૉક્ટરની મદદ માટે તૈયાર કરવામાં આવ્યો છે. પરામર્શ દરમિયાન તમામ માહિતીની સમીક્ષા કરવામાં આવે છે.",
    pa: "ਡਾਕਟਰੀ ਸਮੀਖਿਆ ਦੀ ਲੋੜ ਹੈ: ਇਹ ਖਰੜਾ ਤੁਹਾਡੇ ਡਾਕਟਰ ਦੀ ਮਦਦ ਲਈ ਤਿਆਰ ਕੀਤਾ ਗਿਆ ਹੈ। ਮੁਲਾਕਾਤ ਦੌਰਾਨ ਸਾਰੀ ਜਾਣਕਾਰੀ ਦੀ ਪੁਸ਼ਟੀ ਕੀਤੀ ਜਾਂਦੀ ਹੈ।",
  },
  consultationReadyTitle: {
    en: "Consultation-Ready Check-in",
    hi: "परामर्श के लिए तैयार चेक-इन",
    mr: "सल्लामसलतीसाठी तयार चेक-इन",
    ta: "ஆலோசனைக்கு தயார்",
    gu: "પરામર્શ માટે તૈયાર ચેક-ઇન",
    pa: "ਸਲਾਹ-ਮਸ਼ਵਰੇ ਲਈ ਤਿਆਰ ਚੈੱਕ-ਇਨ",
  },
  consultationReadyBody: {
    en: "By collecting your history and today's symptoms in advance, 100% of your time with the clinician is spent on examination, diagnosis, and care.",
    hi: "अपनी पिछली जानकारी और आज के लक्षण पहले से साझा करके, डॉक्टर के साथ आपका पूरा समय जांच, निदान और उपचार पर खर्च होता है।",
    mr: "तुमचा इतिहास आणि लक्षणे आधीच सांगून, डॉक्टरांसोबतचा संपूर्ण वेळ उपचारांवर खर्च होतो.",
    ta: "உங்கள் வரலாற்றை முன்பே பகிர்வதன் மூலம் முழு நேரமும் சிகிச்சையில் செலவிடப்படுகிறது.",
    gu: "તમારો ઇતિહાસ અગાઉથી શેર કરીને, ડૉક્ટર સાથેનો સંપૂર્ણ સમય સારવાર પર ખર્ચવામાં આવે છે.",
    pa: "ਆਪਣਾ ਇਤਿਹਾਸ ਪਹਿਲਾਂ ਸਾਂਝਾ ਕਰਕੇ, ਡਾਕਟਰ ਨਾਲ ਪੂਰਾ ਸਮਾਂ ਇਲਾਜ 'ਤੇ ਖਰਚ ਹੁੰਦਾ ਹੈ।",
  },
  recordsPortalTitle: {
    en: "Medical Records & Documents",
    hi: "मेडिकल रिकॉर्ड और दस्तावेज़",
    mr: "वैद्यकीय नोंदी आणि कागदपत्रे",
    ta: "மருத்துவ பதிவுகள் மற்றும் ஆவணங்கள்",
    gu: "તબીબી રેકોર્ડ્સ અને દસ્તાવેજો",
    pa: "ਮੈਡੀਕਲ ਰਿਕਾਰਡ ਅਤੇ ਦਸਤਾਵੇਜ਼",
  },
  recordsPortalBody: {
    en: "Upload, review, and manage your prescriptions, laboratory test reports, and hospital summaries.",
    hi: "अपने पर्चे, लैब टेस्ट रिपोर्ट और डिस्चार्ज सारांश अपलोड करें, समीक्षा करें और प्रबंधित करें।",
    mr: "तुमची प्रिस्क्रिप्शन आणि लॅब रिपोर्ट्स अपलोड करा आणि व्यवस्थापित करा.",
    ta: "உங்கள் மருந்துக் குறிப்புகள் மற்றும் ஆய்வக அறிக்கைகளை பதிவேற்றவும்.",
    gu: "તમારા પ્રિસ્ક્રિપ્શન્સ અને લેબ રિપોર્ટ્સ અપલોડ કરો અને મેનેજ કરો.",
    pa: "ਆਪਣੀਆਂ ਪਰਚੀਆਂ ਅਤੇ ਲੈਬ ਰਿਪੋਰਟਾਂ ਅੱਪਲੋਡ ਕਰੋ ਅਤੇ ਸੰਭਾਲੋ।",
  },
  notFoundHeading: {
    en: "Page not found",
    hi: "पृष्ठ नहीं मिला",
    mr: "पृष्ठ आढळले नाही",
    ta: "பக்கம் கிடைக்கவில்லை",
    gu: "પૃષ્ઠ મળ્યું નથી",
    pa: "ਪੰਨਾ ਨਹੀਂ ਮਿਲਿਆ",
  },
  notFoundText: {
    en: "The link you followed may be outdated or the page has moved.",
    hi: "यह लिंक पुराना हो सकता है या पृष्ठ हटा दिया गया है।",
    mr: "हा दुवा जुना असू शकतो किंवा पृष्ठ हलवले गेले आहे.",
    ta: "இந்த இணைப்பு பழையதாக இருக்கலாம் அல்லது பக்கம் மாற்றப்பட்டிருக்கலாம்.",
    gu: "આ લિંક જૂની હોઈ શકે છે અથવા પૃષ્ઠ ખસેડવામાં આવ્યું છે.",
    pa: "ਇਹ ਲਿੰਕ ਪੁਰਾਣਾ ਹੋ ਸਕਦਾ ਹੈ ਜਾਂ ਪੰਨਾ ਬਦਲਿਆ ਗਿਆ ਹੈ।",
  },
} as const satisfies Record<string, Translations>;

/**
 * A UI string. English is required; other languages are optional so a
 * partially-translated language still renders through the fallback chain
 * instead of showing blanks.
 */
export type Translations = { en: string } & Partial<Record<Language, string>>;

export type StringKey = keyof typeof STRINGS;

export function translate(key: StringKey, language: Language): string {
  return localised(withOverlay(STRINGS[key], language), language);
}

/**
 * A localised value plus its overlay translation, if the entry itself has
 * none for this language. An inline key always wins, so a wrong overlay entry
 * can be corrected in `STRINGS` directly.
 */
export function withOverlay(
  value: Translations,
  language: Language,
): Partial<Record<string, string>> {
  if (value[language]) return value;
  const translated = overlay(value.en, language);
  return translated ? { ...value, [language]: translated } : value;
}

/** Which UI strings are missing a translation. Used by the audit test. */
export function untranslated(language: Language): StringKey[] {
  return (Object.keys(STRINGS) as StringKey[]).filter(
    (key) => !withOverlay(STRINGS[key], language)[language],
  );
}
