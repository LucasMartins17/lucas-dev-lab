import { StatCard } from "@/components/shared/StatCard"
import { FolderOpen, DollarSign, Clock, CheckCircle, TrendingUp } from "lucide-react"
import { 
  Area, 
  AreaChart, 
  CartesianGrid, 
  XAxis, 
} from "recharts"
import {
  type ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"

const chartData = [
  { month: "Jan", projects: 4 },
  { month: "Fev", projects: 7 },
  { month: "Mar", projects: 5 },
  { month: "Abr", projects: 12 },
]

const chartConfig = {
  projects: {
    label: "Projetos",
    color: "var(--primary)",
  },
} satisfies ChartConfig

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
        <p className="text-muted-foreground">
          Gerenciamento de produtividade / Productivity Management.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Total de Projetos" value="12" icon={FolderOpen} description="Projetos cadastrados" />
        <StatCard title="Receita / Revenue" value="R$ 4.500,00" icon={DollarSign} description="+15% este mês" />
        <StatCard title="Em Andamento" value="5" icon={Clock} />
        <StatCard title="Concluídos" value="7" icon={CheckCircle} />
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Area Chart - Gradient</CardTitle>
          <CardDescription>Mostrando total de projetos nos últimos meses</CardDescription>
        </CardHeader>
        <CardContent>
          <ChartContainer config={chartConfig} className="h-[300px] w-full">
            <AreaChart accessibilityLayer data={chartData} margin={{ left: 12, right: 12 }}>
              <defs>
                {/* Definição do Gradiente (SVG Gradient) */}
                <linearGradient id="fillProjects" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="var(--color-projects)" stopOpacity={0.8} />
                  <stop offset="95%" stopColor="var(--color-projects)" stopOpacity={0.1} />
                </linearGradient>
              </defs>
              <CartesianGrid vertical={false} strokeDasharray="3 3" opacity={0.1} />
              <XAxis
                dataKey="month"
                tickLine={false}
                axisLine={false}
                tickMargin={8}
                tickFormatter={(value) => value.slice(0, 3)}
              />
              <ChartTooltip cursor={false} content={<ChartTooltipContent hideLabel />} />
              <Area
                dataKey="projects"
                type="natural" // Deixa a linha suave/curvada como na imagem
                fill="url(#fillProjects)" // Chama o gradiente acima
                stroke="var(--color-projects)"
                stackId="a"
              />
            </AreaChart>
          </ChartContainer>
        </CardContent>
        <CardFooter>
          <div className="flex w-full items-start gap-2 text-sm">
            <div className="grid gap-2">
              <div className="flex items-center gap-2 font-medium leading-none">
                Trending up by 5.2% this month <TrendingUp className="h-4 w-4" />
              </div>
              <div className="flex items-center gap-2 leading-none text-muted-foreground">
                Janeiro - Abril 2026
              </div>
            </div>
          </div>
        </CardFooter>
      </Card>
    </div>
  )
}