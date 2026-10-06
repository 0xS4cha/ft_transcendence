import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { ButtonGroup } from "@/components/ui/button-group";
import { Eye } from "lucide-react";
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
  FieldSeparator
} from "@/components/ui/field";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { useState } from "react";
import { Link } from "react-router-dom";
import { toast } from "@/components/ui/toast";
import { useNavigate } from "react-router-dom";
import { useAppDispatch } from "@/store/hooks";
import { signupUser } from "@/store/reducers/userSlice";
import { type SignupPayload } from "@/types/user";
import { useTranslation } from "react-i18next";

type SignupFormProps = React.ComponentProps<"form"> & {
  func: (type: boolean) => void;
};

export function SignupForm({
  className,
  func,
  ...props
}: SignupFormProps) {
  const [viewPassword, setViewPassword] = useState(true);
  const [viewConfirmPassword, setViewConfirmPassword] = useState(true);
  const [checked, setChecked] = useState(false);
  const [formData, setFormData] = useState<SignupPayload>({
    email: "",
    password: "",
    confirm_password: "",
  });
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const { t } = useTranslation();

  function handleChange(event: React.ChangeEvent<HTMLInputElement>) {
    const { name, value } = event.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!checked) {
      toast.add({
        type: "error",
        title: t('auth.checkTerms'),
      });
      return ;
    };
    try {
      await dispatch(signupUser(formData)).unwrap();
      navigate("/profile");
      toast.add({
        type: "info",
        title: t('auth.signupSuccess'),
      });
    } catch {
      toast.add({
        type: "error",
        title: t('auth.signupFailed'),
      });
    }
  }

  return (
    <form className={cn("flex flex-col gap-6", className)} {...props} onSubmit={handleSubmit}>
      <FieldGroup>
        <div className="flex flex-col items-center gap-1 text-center">
          <h1 className="text-2xl font-bold">{t('auth.signupTitle')}</h1>
          <p className="text-sm text-balance text-muted-foreground">
            {t('auth.signupSubtitle')}
          </p>
        </div>
        <Field>
          <FieldLabel htmlFor="username">{t('common.username')}</FieldLabel>
          <Input id="username" name="username" type="text" placeholder={t('auth.usernamePlaceholder')} required onChange={handleChange}/>
        </Field>
        <Field>
          <FieldLabel htmlFor="email">{t('common.email')}</FieldLabel>
          <Input id="email" name="email" type="email" placeholder={t('auth.emailPlaceholder')} required value={formData.email} onChange={handleChange}/>
        </Field>
        <Field>
          <div className="flex items-center">
            <FieldLabel htmlFor="password">{t('common.password')}</FieldLabel>
          </div>
          <ButtonGroup>
            <Input id="password" name="password" type={viewPassword ? "password" : "text"} required value={formData.password} onChange={handleChange}/>
            <Button type="button" variant={viewPassword ? "outline" : "default"} onClick={() => setViewPassword(!viewPassword)}><Eye/></Button>
          </ButtonGroup>
        </Field>
        <Field>
          <div className="flex items-center">
            <FieldLabel htmlFor="confirm_password">{t('common.confirmPassword')}</FieldLabel>
          </div>
          <ButtonGroup>
            <Input id="confirm_password" name="confirm_password" type={viewConfirmPassword ? "password" : "text"} required value={formData.confirm_password} onChange={handleChange}/>
            <Button type="button" variant={viewConfirmPassword ? "outline" : "default"} onClick={() => setViewConfirmPassword(!viewConfirmPassword)}><Eye/></Button>
          </ButtonGroup>
        </Field>
          <Field orientation="horizontal">
          <Checkbox
            id="terms-checkbox-2"
            name="terms-checkbox-2"
            onCheckedChange={setChecked}
            checked={checked}
          />
          <FieldLabel htmlFor="terms-checkbox-2">
            {t('auth.accept')}{" "}
            <Link to="/terms" className="underline underline-offset-4" >{t('auth.terms')}</Link>{" "}
            {t('auth.and')}{" "}
            <Link to="/conditions" className="underline underline-offset-4" >{t('auth.conditions')}</Link>
          </FieldLabel>
        </Field>
        <Field>
          <Button type="submit">{t('auth.signup')}</Button>
        </Field>
        <FieldSeparator>{t('auth.continueWith')}</FieldSeparator>
        <Field>
          <FieldDescription className="text-center">
            {t('auth.hasAccount')} {" "}
            <a href="#" onClick={() => func(true)} className="underline underline-offset-4">
              {t('auth.login')}
            </a>
          </FieldDescription>
        </Field>
      </FieldGroup>
    </form>
  );
}
