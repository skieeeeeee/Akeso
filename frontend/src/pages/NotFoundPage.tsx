import { Link } from "react-router-dom";
import { Compass } from "lucide-react";
import { AppShell } from "@/components/layout/AppShell";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/States";
import { useI18n } from "@/providers/I18nProvider";

export function NotFoundPage() {
  const { t } = useI18n();
  return (
    <AppShell backRoute="/" backLabel={t("backToHome")}>
      <EmptyState
        asPageHeading
        icon={<Compass className="h-6 w-6" />}
        title={t("notFoundHeading")}
        description={t("notFoundText")}
        action={
          <Button asChild>
            <Link to="/">{t("backToHome")}</Link>
          </Button>
        }
      />
    </AppShell>
  );
}
