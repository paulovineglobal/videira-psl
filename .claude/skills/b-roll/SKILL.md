---
name: b-roll
description: Busca clipes de b-roll gratuitos (Pexels) a partir de um roteiro, tema ou lista de cenas. Use quando o usuário pedir /b-roll, b-roll, imagens de apoio, footage ou vídeos de fundo para um vídeo. Retorna links de download em HD, sem marca d'água e com uso comercial liberado.
---

# /b-roll — Busca de b-roll gratuito no Pexels

Você vai transformar o pedido do usuário (um roteiro, tema ou lista de cenas) em
clipes de b-roll prontos para baixar, usando a API gratuita do Pexels.

## Pré-requisitos

- A variável de ambiente `PEXELS_API_KEY` precisa estar definida.
  Se não estiver, avise o usuário para adicioná-la nas configurações do
  ambiente (Claude Code → Environment → Environment variables) e pare.
- O domínio `api.pexels.com` precisa estar liberado na política de rede do
  ambiente. Se a chamada falhar com erro de proxy/403 no CONNECT, explique ao
  usuário que é a política de rede do ambiente e como liberar (Environment →
  Network access → adicionar `api.pexels.com`).

## Fluxo

1. **Entenda o pedido.** Se o usuário passou um roteiro ou texto, quebre-o em
   cenas/momentos (5 a 10 no máximo). Para cada cena, escreva 1 termo de busca
   curto **em inglês** (a busca do Pexels funciona muito melhor em inglês) —
   ex.: cena "pessoas adorando na igreja" → `church worship hands raised`.
   Se o usuário passou só um tema, gere 3 a 5 variações de busca.

2. **Busque os clipes** com o script auxiliar (um comando por cena):

   ```bash
   python3 .claude/skills/b-roll/scripts/pexels_broll.py "church worship" --per-page 5 --orientation landscape
   ```

   Opções úteis:
   - `--orientation portrait` para Reels/Shorts/TikTok; `landscape` para YouTube.
   - `--min-duration 5 --max-duration 30` para filtrar por duração.
   - `--download PASTA` para já baixar os .mp4.

3. **Selecione o melhor clipe por cena** (resolução ≥ 1080p, duração adequada,
   visual coerente com as outras cenas). Se uma busca não retornar nada bom,
   tente um termo mais genérico.

4. **Entregue o resultado** como uma tabela em português: cena → descrição do
   clipe → duração → link da página no Pexels → link de download direto.
   Sempre inclua o crédito do autor (o Pexels não exige, mas é boa prática).
   Se o usuário pediu para baixar, use `--download` e informe os caminhos.

## Regras

- Nunca imprima o valor de `PEXELS_API_KEY` na conversa nem o grave em arquivos.
- Limite: a API gratuita permite 200 requisições/hora — não dispare dezenas de
  buscas desnecessárias.
- Se o usuário pedir cenas impossíveis de achar em banco de vídeo (ex.: cena
  histórica específica, produto próprio), diga isso e sugira gerar com IA
  (Hailuo, Dreamina/Seedance têm créditos grátis diários) em vez de forçar uma
  busca ruim.
