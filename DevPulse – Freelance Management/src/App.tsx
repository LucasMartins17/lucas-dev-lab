import { BrowserRouter, Routes, Route } from "react-router-dom";
import { SidebarProvider, SidebarInset, SidebarTrigger } from "@/components/ui/sidebar";
import { TooltipProvider } from "@/components/ui/tooltip";
import { AppSidebar } from "@/components/layout/Sidebar";
import Dashboard from "@/pages/Dashboard";


function App() {
  return (
    <BrowserRouter>
      <TooltipProvider>
        <SidebarProvider>
          <AppSidebar />
          <SidebarInset>
            <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
              <SidebarTrigger />
              <div className="flex items-center gap-2 px-3">
                <span className="text-sm font-semibold">Fatec Lab</span>
                <span className="text-muted-foreground">/</span>
                <span className="text-sm text-muted-foreground">Project Manager</span>
              </div>
            </header>

            <main className="flex-1 overflow-y-auto p-6">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                {/* Página de Login separada depois */}
              </Routes>
            </main>
          </SidebarInset>
        </SidebarProvider>
      </TooltipProvider>
    </BrowserRouter>
  );
}

export default App;