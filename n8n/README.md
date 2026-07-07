# n8n — Automação local (Videira PSL)

Configuração para rodar o [n8n](https://n8n.io) localmente com Docker,
para automações da igreja (Instagram, YouTube, avisos, integrações com o site etc.).

## Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Mac/Windows)
  ou Docker Engine + Docker Compose (Linux)

## Como iniciar

```bash
cd n8n
cp .env.example .env   # só na primeira vez
docker compose up -d
```

Acesse **http://localhost:5678** no navegador. Na primeira vez, o n8n pede
para criar a conta de administrador (usuário e senha ficam salvos localmente).

## Comandos úteis

| Ação                    | Comando                                      |
| ----------------------- | -------------------------------------------- |
| Iniciar                 | `docker compose up -d`                       |
| Parar                   | `docker compose down`                        |
| Ver logs                | `docker compose logs -f n8n`                 |
| Atualizar para a última versão | `docker compose pull && docker compose up -d` |

## Onde ficam os dados

Todos os workflows, credenciais e configurações ficam no volume Docker
`n8n_data`. Isso significa que:

- Parar/reiniciar/atualizar o container **não apaga nada**;
- `docker compose down -v` **apaga tudo** — não use `-v` a menos que queira
  zerar a instalação;
- Para backup, exporte os workflows pela interface (menu do workflow →
  *Download*) e guarde os JSONs — se quiser, versione-os na pasta
  `n8n/workflows/` deste repositório.

## Webhooks (receber eventos de serviços externos)

Rodando localmente, serviços externos não conseguem alcançar
`http://localhost:5678`. Para testar webhooks:

1. Suba um túnel, por exemplo com cloudflared:
   ```bash
   cloudflared tunnel --url http://localhost:5678
   ```
2. Copie a URL pública gerada e defina `WEBHOOK_URL` no arquivo `.env`;
3. Reinicie: `docker compose up -d`.

Para uso em produção (automações rodando 24h), o ideal é hospedar esta mesma
configuração em um VPS com HTTPS em vez de depender de uma máquina local ligada.

## Licença do n8n

O n8n usa a *Sustainable Use License* (fair-code): uso interno auto-hospedado
é gratuito e sem limite de workflows.
