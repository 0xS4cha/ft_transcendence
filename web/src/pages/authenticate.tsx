import { LoginForm } from "@/components/login/form"
import { SignupForm } from "@/components/signup/form"
import { useState } from "react"

export default function Authenticate() {
    const [isLogin, setIsLogin] = useState(true);
    return (
    <div className="grid min-h-svh lg:grid-cols-2">
      <div className="flex flex-col gap-4 p-6 md:p-10">
        <div className="flex justify-center gap-2 md:justify-start">
          <a href="#" className="flex items-center gap-2 font-medium">
            Tactyx
          </a>
        </div>
        <div className="flex flex-1 items-center justify-center">
          <div className="w-full max-w-xs">
            {isLogin ? <LoginForm func={setIsLogin} /> : <SignupForm func={setIsLogin} /> }
          </div>
        </div>
      </div>
      <div className="relative hidden bg-muted lg:block">
        <img
          src="/bg-wallpaper.jpg"
          alt="Image"
          className="absolute inset-0 h-full w-full object-cover"
        />
      </div>
    </div>
  )
}
