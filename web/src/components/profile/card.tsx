import { Card, CardAction, CardContent } from "@/components/ui/card";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { setTheme } from "@/store/reducers/userSlice";
import { initialsOf } from "@/lib/utils";
import i18n from "@/lib/i18n";
import { useTranslation } from "react-i18next";
import { Moon, Sun, Trash, Info , Pencil, Upload} from "lucide-react";
import { Button } from "@/components/ui/button";
import { deleteUser, setUsername, setPicture } from "@/store/reducers/userSlice";
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
import { Input } from "@base-ui/react";
import { changeUsername, changePicture, deletePicture } from "@/services/authService";

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
    const [deletePictureOpen, setDeletePictureOpen] = useState(false);
    
    const [editOpen, setEditOpen] = useState(false);
    const [editUsername, setEditUsername] = useState(username || "");
    const [editPicturePreview, setEditPicturePreview] = useState(picture || "");
    const [selectedFile, setSelectedFile] = useState<File | null>(null);

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

    const handleDeletePicture = async () => {
        try {
            if (picture) {
                await deletePicture();
                dispatch(setPicture(""));
            }
            setEditPicturePreview("");
            setSelectedFile(null);
            setDeletePictureOpen(false);
        } catch (error) {
            console.error("Erreur lors de la suppression de la photo de profil :", error);
            setDeletePictureOpen(false);
        }
    };

    const handleSaveProfile = async () => {
        try {
            if (editUsername.trim() !== "" && editUsername !== username) {
                await changeUsername(editUsername.trim());
                dispatch(setUsername(editUsername.trim()));
            }

            if (selectedFile) {
                const response = await changePicture(selectedFile);
                if (response?.picture) {
                    dispatch(setPicture(response.picture));
                }
                setSelectedFile(null);
            }

            setEditOpen(false);
        } catch (error) {
            console.error("Erreur lors de la sauvegarde du profil :", error);
        }
    };

    const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            setSelectedFile(file);
            const reader = new FileReader();
            reader.onloadend = () => {
                setEditPicturePreview(reader.result as string);
            };
            reader.readAsDataURL(file);
        }
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
                            <h2 className="text-xl font-semibold">{username}
                            <Button 
                                    variant="ghost" 
                                    size="icon"
                                    className="h-6 w-6"
                                    onClick={() => {
                                        setEditUsername(username || "");
                                        setEditPicturePreview(picture || "");
                                        setSelectedFile(null);
                                        setEditOpen(true);
                                    }}
                                >
                                    <Pencil className="h-2 w-2" />
                                </Button>
                                </h2>
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
                                "Are you sure ? This action is permanent."
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
            <AlertDialog open={deletePictureOpen} onOpenChange={setDeletePictureOpen}>
                <AlertDialogContent>
                    <AlertDialogHeader>
                        <AlertDialogTitle>{t("profile.deletePicTitle", "Delete profile picture?")}</AlertDialogTitle>
                        <AlertDialogDescription>
                            {t(
                                "profile.deletePicDescription",
                                "Are you sure you want to delete your profile picture?"
                            )}
                        </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                        <AlertDialogCancel>{t("common.cancel", "Cancel")}</AlertDialogCancel>
                        <AlertDialogAction
                            onClick={() => {
                                void handleDeletePicture();
                            }}
                        >
                            {t("profile.deletePicConfirm", "Delete picture")}
                        </AlertDialogAction>
                    </AlertDialogFooter>
                </AlertDialogContent>
            </AlertDialog>

            <Dialog open={editOpen} onOpenChange={setEditOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>{t("profile.editTitle", "Edit Profile")}</DialogTitle>
                        <DialogDescription>
                            {t("profile.editDescription", "Make changes to your profile here.")}
                        </DialogDescription>
                    </DialogHeader>
                    
                    <div className="grid gap-4 py-4">
                        <div className="grid gap-2">
                            <Label htmlFor="username">{t("profile.username", "Username")}</Label>
                            <Input 
                                className="border-2 rounded-md hover:bg-white/10 border-white/10 hover:border-white/30"
                                id="username" 
                                value={editUsername} 
                                onChange={(e) => setEditUsername(e.target.value || "")} 
                            />
                        </div>
                        <div className="grid gap-2">
                            <Label>{t("profile.avatar", "Avatar")}</Label>
                            <Label 
                            htmlFor="picture-upload"
                            className="flex flex-col items-center justify-center w-full h-32 border-2 rounded-lg cursor-pointer  hover:bg-white/10 border-white/10 hover:border-white/30 transition-colors"
                            >
                              <div className="flex flex-col items-center justify-center pt-5 pb-6">
                                <Upload className="w-8 h-8 mb-3 text-neutral-400" />
                                  <p className="mb-2 text-sm text-neutral-400">
                                    <span className="font-semibold text-white">Click to upload</span> or drag and drop
                                  </p>
                                  <p className="text-xs text-neutral-500">SVG, PNG, JPG or GIF</p>
                              </div>
                                <Input 
                                    id="picture-upload" 
                                    type="file" 
                                    accept="image/*" 
                                    className="hidden" 
                                    onChange={handleImageUpload}
                                />
                            </Label>
                            {editPicturePreview && (
                                 <div className="mt-2 flex justify-center">
                                     <Avatar className="size-16 border border-white/10">
                                         <AvatarImage src={editPicturePreview} alt="Preview" className="object-cover" />
                                     </Avatar>
                                 </div>
                            )}
                            <div className="flex justify-center flex-col">
                                <Label htmlFor="picture-delete">{t("profile.pic", "Delete picture")}</Label>
                                <Button
                                    id="picture-delete"
                                    className="mt-2"
                                    type="button"
                                    variant="destructive"
                                    size="icon"
                                    onClick={() => setDeletePictureOpen(true)}
                                    disabled={!picture && !editPicturePreview}
                                    aria-label={t("profile.pic", "Delete picture")}
                                >
                                    <Trash />
                                </Button>
                            </div>
                        </div>
                    </div>
                    <DialogFooter>
                        <Button
                            variant="outline"
                            onClick={() => {
                                setEditOpen(false);
                                setSelectedFile(null);
                            }}
                        >
                            {t("common.cancel", "Cancel")}
                        </Button>
                        <Button onClick={handleSaveProfile}>
                            {t("common.save", "Save")}
                        </Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </Card>
    );
}
