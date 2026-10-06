import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { ButtonGroup } from "@/components/ui/button-group";
import { Eye } from "lucide-react";
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
  FieldSeparator,
} from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { useState } from "react";
import { toast } from "@/components/ui/toast";
import { useNavigate } from "react-router-dom";
import { useAppDispatch } from "@/store/hooks";
import { loginUser } from "@/store/reducers/userSlice";
import { useTranslation } from "react-i18next";

type LoginFormProps = React.ComponentProps<"form"> & {
  func: (type: boolean) => void;
};

export function LoginForm({
  className,
  func,
  ...props
}: LoginFormProps) {
  const [viewPassword, setViewPassword] = useState(true);
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  function handleChange(event: React.ChangeEvent<HTMLInputElement>) {
    const { name, value } = event.target;

    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    try {
      await dispatch(loginUser(formData)).unwrap();
      navigate("/profile");
      toast.add({
        type: "info",
        title: t('auth.loginSuccess'),
      });
    } catch {
      toast.add({
        type: "error",
        title: t('auth.loginFailed'),
      });
    }
  }

  return (
    <form className={cn("flex flex-col gap-6", className)} onSubmit={handleSubmit} {...props}>
      <FieldGroup>
        <div className="flex flex-col items-center gap-1 text-center">
          <h1 className="text-2xl font-bold">{t('auth.loginTitle')}</h1>
          <p className="text-sm text-balance text-muted-foreground">
            {t('auth.loginSubtitle')}
          </p>
        </div>
        <Field>
          <FieldLabel htmlFor="email">{t('common.email')}</FieldLabel>
          <Input
            id="email"
            name="email"
            type="email"
            placeholder={t('auth.emailPlaceholder')}
            required
            value={formData.email}
            onChange={handleChange}
          />
        </Field>
        <Field>
          <div className="flex items-center">
            <FieldLabel htmlFor="password">{t('common.password')}</FieldLabel>
          </div>
          <ButtonGroup>
            <Input
              id="password"
              name="password"
              type={viewPassword ? "password" : "text"}
              required
              value={formData.password}
              onChange={handleChange}
            />
            <Button
              type="button"
              variant={viewPassword ? "outline" : "default"}
              onClick={() => setViewPassword(!viewPassword)}
            >
              <Eye />
            </Button>
          </ButtonGroup>
        </Field>
        <Field>
          <Button type="submit">{t('auth.login')}</Button>
        </Field>
        <FieldSeparator>{t('auth.continueWith')}</FieldSeparator>
        <Field>
          <div className="grid grid-cols-1 gap-2 w-full">
            <Button variant="outline" type="button" className="w-full" onClick={() => window.location.href = "https://localhost:8443/api/auth/login_with_42"}>
              <img src="/42.svg" className="w-4" />
              {t('auth.loginWith42')}
            </Button>
          </div>
          <FieldDescription className="text-center">
            {t('auth.noAccount')} {" "}
            <a href="#" onClick={() => func(false)} className="underline underline-offset-4">
              {t('auth.signUp')}
            </a>
          </FieldDescription>
        </Field>
      </FieldGroup>
    </form>
  );
}
