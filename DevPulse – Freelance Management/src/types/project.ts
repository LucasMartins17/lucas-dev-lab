export type ProjectStatus = 'active' | 'completed' | 'paused';

export interface Project {
  id: string;
  name: string;      // Project Name / Nome do Projeto
  client: string;    // Client / Cliente
  status: ProjectStatus;
  budget: number;    // Budget / Orçamento
  deadline: string;  // Deadline / Prazo
  category: string;  // Category / Categoria (ex: Web, Mobile, Design)
}