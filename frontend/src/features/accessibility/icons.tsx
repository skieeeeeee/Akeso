import {
  Activity,
  AlertTriangle,
  BookOpen,
  Check,
  Ear,
  Eye,
  FlaskConical,
  HandHelping,
  Hand,
  Layers,
  MessageSquare,
  Mic,
  Minus,
  Pill,
  Scissors,
  Signature,
  Smartphone,
  Sparkles,
  Stethoscope,
  ThumbsUp,
  Users,
} from "lucide-react";
import type { ReactNode } from "react";

/**
 * Maps the icon names the API returns onto components.
 *
 * Icons are named server-side (alongside the localised label) so a question
 * can be added without a frontend change, and this map is the only place that
 * knows how a name becomes a picture.
 */
const ICONS: Record<string, ReactNode> = {
  check: <Check className="h-6 w-6" />,
  minus: <Minus className="h-6 w-6" />,
  alert: <AlertTriangle className="h-6 w-6" />,
  smartphone: <Smartphone className="h-6 w-6" />,
  "thumbs-up": <ThumbsUp className="h-6 w-6" />,
  "helping-hand": <HandHelping className="h-6 w-6" />,
  sparkles: <Sparkles className="h-6 w-6" />,
  mic: <Mic className="h-6 w-6" />,
  hand: <Hand className="h-6 w-6" />,
  layers: <Layers className="h-6 w-6" />,
  book: <BookOpen className="h-6 w-6" />,
  eye: <Eye className="h-6 w-6" />,
  ear: <Ear className="h-6 w-6" />,
  users: <Users className="h-6 w-6" />,
  signing: <Signature className="h-6 w-6" />,
  stethoscope: <Stethoscope className="h-6 w-6" />,
  pill: <Pill className="h-6 w-6" />,
  "alert-triangle": <AlertTriangle className="h-6 w-6" />,
  scissors: <Scissors className="h-6 w-6" />,
  activity: <Activity className="h-6 w-6" />,
  flask: <FlaskConical className="h-6 w-6" />,
  message: <MessageSquare className="h-6 w-6" />,
};

export function iconFor(name: string | undefined): ReactNode | undefined {
  return name ? ICONS[name] : undefined;
}
