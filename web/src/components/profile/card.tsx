import { Card, CardContent } from "@/components/ui/card";
import { useAppSelector } from '@/store/hooks';
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { initialsOf } from "@/lib/utils";
import { useTranslation } from "react-i18next";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import i18n from "@/lib/i18n";

const languageOptions = [
    { value: 'en', label: 'English' },
    { value: 'fr', label: 'Français' },
    { value: 'es', label: 'Español' },
];

export function ProfileCard() {
    const { username, picture, email, id } = useAppSelector(state => state.user);
    const { t } = useTranslation();
    const [language, setLanguage] = useState(i18n.language || 'en');

    const handleSaveLanguage = () => {
        void i18n.changeLanguage(language);
    };

    return <Card>
        <CardContent>
            <div className="space-y-12">
                <div className="flex flex-col items-center space-y-4">
                    <Avatar>
                        <AvatarImage src={picture} alt={username} />
                        <AvatarFallback className="text-xs">{initialsOf(username)}</AvatarFallback>
                    </Avatar>
                   <div className="text-center">
                        <h5 className="text-xl font-semibold">{username}</h5>
                        <div className="text-muted-foreground text-sm">{email}</div>
                    </div>
                </div>
                <div className="bg-muted grid grid-cols-3 divide-x rounded-md border text-center *:py-3">
                    <div>
                        <h5 className="text-lg font-semibold">{id}</h5>
                        <div className="text-muted-foreground text-sm">{t('profile.id')}</div>
                    </div>
                </div>

                <div className="space-y-3 border-t pt-4">
                    <div className="text-sm font-medium">{t('common.language', 'Language')}</div>
                    <div className="flex gap-2">
                        <Select value={language} onValueChange={(value) => setLanguage(value ?? 'en')}>
                            <SelectTrigger className="w-full">
                                <SelectValue placeholder="Language" />
                            </SelectTrigger>
                            <SelectContent>
                                {languageOptions.map((option) => (
                                    <SelectItem key={option.value} value={option.value}>
                                        {option.label}
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                        <Button type="button" onClick={handleSaveLanguage}>
                            {t('common.save', 'Save')}
                        </Button>
                    </div>
                </div>
            </div>
        </CardContent>
    </Card>
}