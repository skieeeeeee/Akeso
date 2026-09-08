/**
 * Public health statistics used on the landing page.
 *
 * Every figure carries its own source and year, and is rendered with them —
 * an unsourced health number on a health product is worse than no number.
 *
 * Deliberately absent: any "deaths per minute from missed check-ups" figure.
 * Nobody measures that, so it could only be invented, and a fabricated live
 * death counter is the first thing a clinician would check and disbelieve.
 * The `derived` ticker below is arithmetic from a cited average and says so.
 *
 * These were compiled from published sources; re-verify the numbers before
 * any public presentation, since all of them are periodically restated.
 */
import type { Language, Localised } from "@/types/api";
import { overlay } from "@/lib/translations";

export const FIGURES_COMPILED = "2026";

export type Statistic = {
  id: string;
  /** The number to count up to. */
  value: number;
  /** Rendered after the number, e.g. "million" or "%". */
  unit?: Localised;
  /** Shown as "~" before the value when the figure is an estimate. */
  approximate: boolean;
  label: Localised;
  detail: Localised;
  source: string;
  year: string;
};

const REGIONAL: Language[] = ["mr", "ta", "gu", "pa"];

/**
 * A localised statistic label.
 *
 * English and Hindi are written here; the regional languages come from the
 * overlay files, keyed by the English source, exactly as `STRINGS` does. This
 * file had its own two-language helper once, which is why the figures stayed
 * English on a Tamil landing page.
 */
const t = (en: string, hi: string): Localised => {
  const value: Localised = { en, hi };
  for (const language of REGIONAL) {
    const translated = overlay(en, language);
    if (translated) value[language] = translated;
  }
  return value;
};

export const HEADLINE: Statistic = {
  id: "consultation-length",
  value: 2,
  unit: t("minutes", "मिनट"),
  approximate: true,
  label: t(
    "the average primary-care consultation in India",
    "भारत में औसत प्राथमिक चिकित्सा परामर्श",
  ),
  detail: t(
    "Among the shortest measured anywhere. Almost all of it goes on collecting a history the clinic could already have had.",
    "यह दुनिया में मापे गए सबसे छोटे परामर्शों में है। इसका लगभग पूरा समय वह इतिहास पूछने में जाता है जो क्लिनिक के पास पहले से हो सकता था।",
  ),
  source: "Irving et al., BMJ Open",
  year: "2017",
};

export const STATISTICS: Statistic[] = [
  {
    id: "diabetes",
    value: 101,
    unit: t("million", "मिलियन"),
    approximate: true,
    label: t("people in India live with diabetes", "भारत में मधुमेह से ग्रस्त लोग"),
    detail: t(
      "A further 136 million are prediabetic — a group early detection actually changes.",
      "अन्य 136 मिलियन प्री-डायबिटिक हैं — यह वह समूह है जिसमें शीघ्र पहचान वास्तव में फ़र्क़ लाती है।",
    ),
    source: "ICMR-INDIAB",
    year: "2023",
  },
  {
    id: "hypertension",
    value: 315,
    unit: t("million", "मिलियन"),
    approximate: true,
    label: t("adults live with hypertension", "उच्च रक्तचाप से ग्रस्त वयस्क"),
    detail: t(
      "Only a small fraction have it under control, and many do not know they have it.",
      "बहुत कम लोगों का यह नियंत्रण में है, और कई को पता ही नहीं है कि उन्हें यह है।",
    ),
    source: "ICMR-INDIAB",
    year: "2023",
  },
  {
    id: "ncd-deaths",
    value: 66,
    unit: t("%", "%"),
    approximate: true,
    label: t("of deaths in India are from NCDs", "भारत में एनसीडी से होने वाली मौतें"),
    detail: t(
      "Non-communicable disease — the category where a timely history and follow-up matter most.",
      "गैर-संचारी रोग — जहाँ समय पर इतिहास और फ़ॉलो-अप सबसे ज़्यादा मायने रखते हैं।",
    ),
    source: "WHO",
    year: "2023",
  },
  {
    id: "out-of-pocket",
    value: 47,
    unit: t("%", "%"),
    approximate: true,
    label: t("of health spending is out of pocket", "स्वास्थ्य खर्च जो जेब से होता है"),
    detail: t(
      "Which is why a repeated test or a lost prescription is not a small inconvenience.",
      "इसीलिए दोबारा जाँच या खोया हुआ पर्चा छोटी असुविधा नहीं है।",
    ),
    source: "National Health Accounts",
    year: "2022",
  },
];

/**
 * The live ticker.
 *
 * Not an event stream and not a death toll: it is the 2-minute average
 * divided into the time the visitor has spent on the page, and the UI states
 * that it is arithmetic.
 */
export const CONSULTATION_SECONDS = 120;

export function consultationsInElapsed(elapsedSeconds: number): number {
  return Math.floor(elapsedSeconds / CONSULTATION_SECONDS);
}
