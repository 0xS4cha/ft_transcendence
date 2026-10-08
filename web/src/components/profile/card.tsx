import { Card, CardAction, CardContent } from "@/components/ui/card";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { setTheme } from "@/store/reducers/userSlice";
import { initialsOf } from "@/lib/utils";
import i18n from "@/lib/i18n";
import { useTranslation } from "react-i18next";
import { Moon, Sun, Trash, Info } from "lucide-react";
import { Button } from "@/components/ui/button";
import { deleteUser } from "@/store/reducers/userSlice";
import { useState } from "react";
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";

const languageOptions = [
    { value: "en", label: "🇺🇸 English" },
    { value: "fr", label: "🇫🇷 Français" },
    { value: "es", label: "🇪🇸 Español" },
] as const;

type ThemeValue = "light" | "dark";

export function ProfileCard() {
    const dispatch = useAppDispatch();
    const { t } = useTranslation();
    const { username, picture, email, id, isDark } = useAppSelector((state) => state.user);
    const [rgpdInfoOpen, setRgpdInfoOpen] = useState(false);
    const [deleteOpen, setDeleteOpen] = useState(false);

    const baseLang = (i18n.resolvedLanguage || i18n.language || "en").split("-")[0];
    const language = languageOptions.some((o) => o.value === baseLang) ? baseLang : "en";
    const theme: ThemeValue = isDark ? "dark" : "light";

    const themeOptions: { value: ThemeValue; label: string; icon: typeof Sun }[] = [
        { value: "light", label: t("common.light", "Light"), icon: Sun },
        { value: "dark", label: t("common.dark", "Dark"), icon: Moon },
    ];

    const handleLanguageChange = (value: string | null) => {
        if (!value) return;
        void i18n.changeLanguage(value);
    };

    const handleThemeChange = (value: string | null) => {
        if (value !== "light" && value !== "dark") return;
        const dark = value === "dark";
        dispatch(setTheme(dark));
        try {
            localStorage.setItem("isDark", String(dark));
        } catch {
        }
    };

    const deletergpd = async () => {
        await dispatch(deleteUser()).unwrap();
    };

    return (
        <Card>
            <CardContent>
                <div className="space-y-8">
                    <div className="flex flex-col items-center gap-4">
                        <Avatar className="size-20">
                            <AvatarImage src={picture} alt={username} />
                            <AvatarFallback className="text-lg">{initialsOf(username)}</AvatarFallback>
                        </Avatar>
                        <div className="text-center">
                            <h2 className="text-xl font-semibold">{username}</h2>
                            <p className="text-muted-foreground text-sm break-all">{email}</p>
                        </div>
                    </div>

                    <dl className="bg-muted flex items-center justify-between rounded-md border px-4 py-3">
                        <dt className="text-muted-foreground text-sm">{t("profile.id", "ID")}</dt>
                        <dd className="font-mono text-sm font-medium">{id}</dd>
                    </dl>

                    <div className="space-y-6 border-t pt-6">
                        <div className="space-y-2">
                            <Label id="language-label">{t("common.language", "Language")}</Label>
                            <Select value={language} onValueChange={handleLanguageChange}>
                                <SelectTrigger className="w-full" aria-labelledby="language-label">
                                    <SelectValue placeholder={t("common.language", "Language")} />
                                </SelectTrigger>
                                <SelectContent>
                                    {languageOptions.map((option) => (
                                        <SelectItem key={option.value} value={option.value}>
                                            {option.label}
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>

                        <div className="space-y-2">
                            <Label id="theme-label">{t("common.theme", "Theme")}</Label>
                            <Select value={theme} onValueChange={handleThemeChange}>
                                <SelectTrigger className="w-full" aria-labelledby="theme-label">
                                    <SelectValue placeholder={t("common.theme", "Theme")} />
                                </SelectTrigger>
                                <SelectContent>
                                    {themeOptions.map(({ value, label, icon: Icon }) => (
                                        <SelectItem key={value} value={value}>
                                            <span className="flex items-center gap-2">
                                                <Icon className="size-4" aria-hidden />
                                                {label}
                                            </span>
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>
                    </div>
                </div>
            </CardContent>
            <CardAction>
                <Button
                    type="button"
                    variant="outline"
                    size="icon"
                    onClick={() => setRgpdInfoOpen(true)}
                    aria-label={t("profile.rgpdInfoButton", "RGPD information")}
                >
                    <Info />
                </Button>
                <Button
                    type="button"
                    variant="destructive"
                    size="icon"
                    onClick={() => setDeleteOpen(true)}
                    aria-label={t("profile.rgpdDeleteButton", "Delete my account")}
                >
                    <Trash />
                </Button>
            </CardAction>
            <Dialog open={rgpdInfoOpen} onOpenChange={setRgpdInfoOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>{t("profile.rgpdInfoTitle", "Your personal data")}</DialogTitle>
                        <DialogDescription>
                            {t(
                                "profile.rgpdInfoDescription",
                                "To recover your personal data, send an email to test@tactyx.com."
                            )}
                        </DialogDescription>
                    </DialogHeader>
                    <DialogFooter>
                        <Button type="button" variant="outline" onClick={() => setRgpdInfoOpen(false)}>
                            {t("common.close", "Close")}
                        </Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
            <AlertDialog open={deleteOpen} onOpenChange={setDeleteOpen}>
                <AlertDialogContent>
                    <AlertDialogHeader>
                        <AlertDialogTitle>{t("profile.rgpdDeleteTitle", "Delete your account?")}</AlertDialogTitle>
                        <AlertDialogDescription>
                            {t(
                                "profile.rgpdDeleteDescription",
                                "This action is permanent. If you only need your information back, use the info button and contact test@tactyx.com."
                            )}
                        </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                        <AlertDialogCancel>{t("common.cancel", "Cancel")}</AlertDialogCancel>
                        <AlertDialogAction
                            onClick={() => {
                                void deletergpd();
                            }}
                        >
                            {t("profile.rgpdDeleteConfirm", "Delete account")}
                        </AlertDialogAction>
                    </AlertDialogFooter>
                </AlertDialogContent>
            </AlertDialog>
        </Card>
    );
}