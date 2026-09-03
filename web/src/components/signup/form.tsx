import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { ButtonGroup } from "@/components/ui/button-group"
import { Eye } from "lucide-react"
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
  FieldSeparator
} from "@/components/ui/field"
import { Checkbox } from "@/components/ui/checkbox"
import { Input } from "@/components/ui/input"
import { useState } from "react"
import { Link } from "react-router-dom";
import { toast } from "@/components/ui/toast"

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
  const [formData, setFormData] = useState({});

  function handleChange(event: React.ChangeEvent<HTMLInputElement>) {
        const { name, value } = event.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    }

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    fetch("/signup", {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    }).then(response => {
      if (!response.ok) {
        toast.add({
          type: "error",
          title: "Sign up failed",
        });
      }
      return response.json();
    }).then(userData => {
      console.log(userData);
      toast.add({
        type: "info",
        title: "Sign up successfully",
      });
    }).catch(() => {
      toast.add({
        type: "error",
        title: "Sign up failed (INTERNAL)",
      });
    });
  }

  return (
    <form className={cn("flex flex-col gap-6", className)} {...props} onSubmit={handleSubmit}>
      <FieldGroup>
        <div className="flex flex-col items-center gap-1 text-center">
          <h1 className="text-2xl font-bold">Create your account</h1>
          <p className="text-sm text-balance text-muted-foreground">
            Enter your email below to signup your account
          </p>
        </div>
        <Field>
          <FieldLabel htmlFor="email">Email</FieldLabel>
          <Input id="email" name="email" type="email" placeholder="m@example.com" required onChange={handleChange}/>
        </Field>
        <Field>
          <div className="flex items-center">
            <FieldLabel htmlFor="password">Password</FieldLabel>
          </div>
          <ButtonGroup>
            <Input id="password" name="password" type={viewPassword ? "password" : "text"} required onChange={handleChange}/>
            <Button variant={viewPassword ? "outline" : "default"} onClick={() => setViewPassword(!viewPassword)}><Eye/></Button>
          </ButtonGroup>
        </Field>
        <Field>
          <div className="flex items-center">
            <FieldLabel htmlFor="password">Confirm your password</FieldLabel>
          </div>
          <ButtonGroup>
            <Input id="password" name="confirm_password" type={viewConfirmPassword ? "password" : "text"} required onChange={handleChange}/>
            <Button variant={viewConfirmPassword ? "outline" : "default"} onClick={() => setViewConfirmPassword(!viewConfirmPassword)}><Eye/></Button>
          </ButtonGroup>
        </Field>
          <Field orientation="horizontal">
          <Checkbox
            id="terms-checkbox-2"
            name="terms-checkbox-2"
            defaultChecked
          />
          <FieldLabel htmlFor="terms-checkbox-2">
            Accept
            <Link to="/terms" className="underline underline-offset-4" >terms</Link>
            and
            <Link to="/condition" className="underline underline-offset-4" >conditions</Link>
          </FieldLabel>
        </Field>
        <Field>
          <Button type="submit">Sign-up</Button>
        </Field>
        <FieldSeparator>Or continue with</FieldSeparator>
        <Field>
          <FieldDescription className="text-center">
            Already have an account ?{" "}
            <a href="#" onClick={() => func(true)} className="underline underline-offset-4">
              Login
            </a>
          </FieldDescription>
        </Field>
      </FieldGroup>
    </form>
  )
}
