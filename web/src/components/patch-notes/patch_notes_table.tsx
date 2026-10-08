import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { useTranslation } from "react-i18next";

export default function PatchNotePage() {
  const { t } = useTranslation();
  const [patchHtml, setPatchHtml] = useState<string>("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPatchNote = async () => {
      try {
        const response = await fetch("/api/patchnote/latest");
        const htmlString = await response.text(); 
        setPatchHtml(htmlString);
      } catch (error) {
        console.log("Error while fetch the latest patch note", error);
      } finally {
        setLoading(false);
      }
    };

    fetchPatchNote();
  }, []);

  if (loading) {
    return <div className="p-8 text-center text-muted-foreground">{t("patchnote.loading", "Loading patch note ...")}</div>;
  }

  return (
    <div className="min-h-screen p-6 w-full max-w-5xl mx-auto">
      <Card className="border-border bg-card text-card-foreground dark:border-white/10 dark:bg-[#202020]">
        <CardContent className="p-8">
          <div 
            className="patch-note-container"
            dangerouslySetInnerHTML={{ __html: patchHtml }} 
          />
        </CardContent>
      </Card>
    </div>
  );
}