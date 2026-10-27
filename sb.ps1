<#
.SYNOPSIS
  Second Brain automation for Windows (PowerShell). Mirror of the Makefile.
  Thin wrappers around the coding-agent CLI in headless mode.

.DESCRIPTION
  Requires the `claude` CLI on PATH.
  --permission-mode acceptEdits lets the agent write wiki files without prompting.

.EXAMPLE
  ./sb.ps1 ingest "raw/artigo.md"
  ./sb.ps1 ingest "https://example.com/article"
  ./sb.ps1 process-inbox
  ./sb.ps1 query "what do my notes say about big-o for linked lists?"
  ./sb.ps1 lint
  ./sb.ps1 capture "a fleeting thought"
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet('ingest', 'process-inbox', 'query', 'lint', 'capture', 'study', 'explain', 'gaps', 'help',
                 'status', 'entrevista', 'diagnostico', 'trilha', 'dia', 'semana', 'ideias', 'post', 'decisao', 'brag', 'tese', 'projeto')]
    [string]$Command,

    [Parameter(Position = 1, ValueFromRemainingArguments = $true)]
    [string[]]$Rest
)

$ErrorActionPreference = 'Stop'
$Claude = if ($env:CLAUDE) { $env:CLAUDE } else { 'claude' }
$Perm   = @('--permission-mode', 'acceptEdits')
$Arg    = ($Rest -join ' ')
# Run from the vault root (this script's folder) so vault-relative paths resolve.
Set-Location -Path $PSScriptRoot

switch ($Command) {
    'ingest' {
        if (-not $Arg) { throw 'Usage: ./sb.ps1 ingest "path-or-URL"' }
        & $Claude -p "/ingest $Arg" @Perm
    }
    'process-inbox' { & $Claude -p '/process-inbox' @Perm }
    'query' {
        if (-not $Arg) { throw 'Usage: ./sb.ps1 query "your question"' }
        & $Claude -p "/query $Arg" @Perm
    }
    'lint' { & $Claude -p '/lint' @Perm }
    'capture' {
        if (-not $Arg) { throw 'Usage: ./sb.ps1 capture "a thought"' }
        $inbox = Join-Path $PSScriptRoot 'raw/inbox.md'
        $old = Get-Content -Path $inbox -Raw
        Set-Content -Path $inbox -Value ("$Arg`n$old") -NoNewline
        Write-Host 'Captured to raw/inbox.md'
    }
    # Interactive: open a live agent session so it can ask you questions.
    'study'   { & $Claude "/study $Arg" @Perm }
    'explain' {
        if (-not $Arg) { throw 'Usage: ./sb.ps1 explain "a concept"' }
        & $Claude "/explain $Arg" @Perm
    }
    'gaps'    { & $Claude -p '/gaps' @Perm }
    # ---- personal OS (areas/ + journal/) ----
    'status'      { python scripts/os_status.py --human }
    # Interactive skills (live session, one question at a time).
    'entrevista'  { & $Claude '/entrevista' @Perm }
    'diagnostico' { & $Claude '/diagnostico' @Perm }
    'trilha'      { & $Claude "/trilha $Arg" @Perm }
    'dia'         { & $Claude '/dia' @Perm }
    'semana'      { & $Claude '/semana' @Perm }
    'decisao' {
        if (-not $Arg) { throw 'Usage: ./sb.ps1 decisao <frente>' }
        & $Claude "/decisao $Arg" @Perm
    }
    'brag'        {
        if (-not $Arg) { throw 'Usage: ./sb.ps1 brag add <texto>|colher|revisar <periodo>|listar' }
        & $Claude "/brag $Arg" @Perm
    }
    'tese'        { & $Claude "/tese $Arg" @Perm }
    'projeto'     { & $Claude "/projeto $Arg" @Perm }
    # Headless.
    'ideias'      { & $Claude -p "/ideias $Arg" @Perm }
    'post' {
        if (-not $Arg) { throw 'Usage: ./sb.ps1 post "<tema> [x|linkedin|medium]"' }
        & $Claude -p "/post $Arg" @Perm
    }
    'help' {
        Write-Host 'Second Brain commands:'
        Write-Host '  ./sb.ps1 ingest "path-or-URL"   Ingest one source into the wiki'
        Write-Host '  ./sb.ps1 process-inbox          Triage raw/inbox.md into the wiki'
        Write-Host '  ./sb.ps1 query "question"       Ask the wiki; answer saved to output/'
        Write-Host '  ./sb.ps1 lint                   Health-check the wiki'
        Write-Host '  ./sb.ps1 capture "a thought"    Append a line to raw/inbox.md (no LLM)'
        Write-Host '  -- learning --'
        Write-Host '  ./sb.ps1 study [N]              Spaced-repetition session (interactive)'
        Write-Host '  ./sb.ps1 explain "a concept"    Feynman mode (interactive)'
        Write-Host '  ./sb.ps1 gaps                   Learning health check -> output/study-plan.md'
        Write-Host '  -- personal OS --'
        Write-Host '  ./sb.ps1 status                 System state (python scripts/os_status.py --human, no LLM)'
        Write-Host '  ./sb.ps1 entrevista             First conversation: field, fronts, goals, domains (interactive)'
        Write-Host '  ./sb.ps1 diagnostico            Diagnostic interview -> areas/estudos/gap-map.md (interactive)'
        Write-Host '  ./sb.ps1 trilha nova "<tema>"   Study tracks: nova|continuar|listar|fechar (interactive)'
        Write-Host '  ./sb.ps1 dia                    Open the day -> journal/<today>.md (interactive)'
        Write-Host '  ./sb.ps1 semana                 Weekly review -> journal/semanas/<week>.md (interactive)'
        Write-Host '  ./sb.ps1 ideias [N]             Post ideas -> areas/publico/ideias.md'
        Write-Host '  ./sb.ps1 post "<tema> [x|linkedin|medium]"  Draft a post -> areas/publico/posts/'
        Write-Host '  ./sb.ps1 decisao <frente>       Record a work decision (interactive)'
        Write-Host '  ./sb.ps1 brag <colher|add ...>  Brag document: harvest, add, review (interactive)'
        Write-Host '  ./sb.ps1 tese nova "<enunciado>" Theses: nova|revisar|desafiar|listar (interactive)'
        Write-Host '  ./sb.ps1 projeto novo "<nome>"  Public projects: novo|continuar|publicar|listar (interactive)'
    }
}
