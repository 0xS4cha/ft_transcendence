import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { ButtonGroup } from "@/components/ui/button-group"
import { Eye } from "lucide-react"
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
  FieldSeparator,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import { useState } from "react"

type LoginFormProps = React.ComponentProps<"form"> & {
  func?: (type: boolean) => void;
};

export function SignupForm({
  className,
  func,
  ...props
}: LoginFormProps) {
  const [viewPassword, setViewPassword] = useState(true)
  return (
    <form className={cn("flex flex-col gap-6", className)} {...props}>
      <FieldGroup>
        <div className="flex flex-col items-center gap-1 text-center">
          <h1 className="text-2xl font-bold">Login to your account</h1>
          <p className="text-sm text-balance text-muted-foreground">
            Enter your email below to login to your account
          </p>
        </div>
        <Field>
          <FieldLabel htmlFor="email">Email</FieldLabel>
          <Input id="email" type="email" placeholder="m@example.com" required />
        </Field>
        <Field>
          <div className="flex items-center">
            <FieldLabel htmlFor="password">Password</FieldLabel>
          </div>
          <ButtonGroup>
            <Input id="password" type={viewPassword ? "password" : "text"} required />
            <Button variant={viewPassword ? "outline" : "default"} onClick={() => setViewPassword(!viewPassword)}><Eye/></Button>
          </ButtonGroup>
          <a
            href="#"
            className="ml-auto text-sm underline-offset-4 hover:underline"
          >
            Forgot your password?
          </a>
        </Field>
        <Field>
          <Button type="submit">Login</Button>
        </Field>
        <FieldSeparator>Or continue with</FieldSeparator>
        <Field>
          <div className="grid grid-cols-2 gap-2 w-full">
            <Button variant="outline" type="button" className="w-full">
                <img src="/42.svg" className="w-4"/>
              Login with 42
            </Button>
            <Button variant="outline" type="button" className="w-full">
              <img src="/riot.svg" className="w-4"/>
              Login with Riot
            </Button>
          </div>
          <FieldDescription className="text-center">
            Don&apos;t have an ?{" "}
            <a href="#" onClick={() => func(true)} className="underline underline-offset-4">
              Sign up
            </a>
          </FieldDescription>
        </Field>
      </FieldGroup>
    </form>
  )
}
