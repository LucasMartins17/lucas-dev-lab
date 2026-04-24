import { LoginForm } from "@/components/login-form"

export default function Login() {
  return (
    // 'bg-background' ou 'bg-muted' para o fundo escuro
    <div className="flex min-h-svh flex-col items-center justify-center bg-background p-6 md:p-10">
      {/* AJUSTE AQUI: Adicione 'max-w-md' (médio) ou 'max-w-sm' (pequeno) */}
      <div className="w-full max-w-sm"> 
        <LoginForm />
      </div>
    </div>
  )
}