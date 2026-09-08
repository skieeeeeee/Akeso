import { useCallback, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/providers/AuthProvider";

/**
 * Move to the next onboarding step.
 *
 * The server decides the destination (it returns `next_route`), and the
 * session is refreshed first so the step guard and the progress indicator
 * both see the new status before the navigation happens.
 */
export function useAdvance() {
  const { refresh } = useAuth();
  const navigate = useNavigate();
  const [isAdvancing, setIsAdvancing] = useState(false);

  const advance = useCallback(
    async (route: string) => {
      setIsAdvancing(true);
      try {
        await refresh();
        navigate(route);
      } finally {
        setIsAdvancing(false);
      }
    },
    [refresh, navigate],
  );

  return { advance, isAdvancing };
}
