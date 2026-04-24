import { StatCard } from "@/components/shared/StatCard"
import { FolderOpen, DollarSign, Clock, CheckCircle } from "lucide-react"

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
        <p className="text-muted-foreground">
          Bem-vindo ao seu painel de controle 
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard 
          title="Total de Projetos" 
          value="12" 
          icon={FolderOpen} 
          description="Projetos cadastrados" 
        />
        <StatCard 
          title="Receita / Revenue" 
          value="R$ 4.500,00" 
          icon={DollarSign} 
          description="+15% em relação ao mês passado" 
        />
        <StatCard 
          title="Em Andamento" 
          value="5" 
          icon={Clock} 
          description="Tasks pendentes" 
        />
        <StatCard 
          title="Concluídos" 
          value="7" 
          icon={CheckCircle} 
          description="Finalizados com sucesso" 
        />
      </div>

      {/* Espaço para um gráfico ou tabela futura */}
      <div className="h-[300px] w-full rounded-xl border border-dashed flex items-center justify-center text-muted-foreground">
        Área do Gráfico
      </div>
    </div>
  )
}