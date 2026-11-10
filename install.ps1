# AgentForge Skill Installer for PowerShell (Windows / macOS / Linux)
# TL;DR: Downloads a skill from AgentForge into your project directory.
# Default target agent: GitHub Copilot (.github\skills\<skill-name>\)

[CmdletBinding()]
param(
    [Parameter(Position = 0, Mandatory = $false)]
    [string]$SkillName,

    [Parameter(Position = 1, Mandatory = $false)]
    [ValidateSet("copilot", "antigravity", "cursor", "claude")]
    [string]$Agent = "copilot"
)

$RepoOrg  = "kolithadesilva"
$RepoName = "agentforge"
$Branch   = "main"
$RawBase  = "https://raw.githubusercontent.com/$RepoOrg/$RepoName/$Branch"

if ([string]::IsNullOrWhiteSpace($SkillName)) {
    Write-Host "Usage: .\install.ps1 -SkillName <skill-name> [-Agent copilot|antigravity|cursor|claude]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "One-liner:" -ForegroundColor Yellow
    Write-Host "  & ([scriptblock]::Create((irm $RawBase/install.ps1))) <skill-name> [copilot]"
    exit 1
}

$AgentPaths = @{
    "copilot"     = ".github/skills/$SkillName"
    "antigravity" = ".agents/skills/$SkillName"
    "cursor"      = ".cursor/skills/$SkillName"
    "claude"      = ".claude/skills/$SkillName"
}

$DestDir = $AgentPaths[$Agent]

Write-Host "=== AgentForge Skill Installer (PowerShell) ===" -ForegroundColor Cyan
Write-Host "Skill:  $SkillName"
Write-Host "Agent:  $Agent"
Write-Host "Target: $DestDir"
Write-Host ""

# Fetch catalog
$CatalogData = $null
$LocalCatalog = Join-Path $PSScriptRoot "catalog\catalog.json"

if (Test-Path $LocalCatalog) {
    $CatalogData = Get-Content -Raw $LocalCatalog | ConvertFrom-Json
} else {
    $CatalogUrl = "$RawBase/catalog/catalog.json"
    Write-Host "Fetching catalog from $CatalogUrl..."
    try {
        $CatalogData = Invoke-RestMethod -Uri $CatalogUrl -Method Get
    } catch {
        Write-Error "Failed to fetch catalog from AgentForge: $_"
        exit 1
    }
}

# Locate skill entry
$SkillEntry = $CatalogData | Where-Object { $_.name -eq $SkillName }

if (-not $SkillEntry) {
    Write-Error "Skill '$SkillName' was not found in catalog.json."
    exit 1
}

$SkillPath = $SkillEntry.path
Write-Host "Found skill at: $SkillPath"

# Create destination folder
if (-not (Test-Path $DestDir)) {
    New-Item -ItemType Directory -Path $DestDir -Force | Out-Null
}

$DestFile = Join-Path $DestDir "SKILL.md"
$LocalSkillFile = Join-Path $PSScriptRoot "$SkillPath/SKILL.md"

if (Test-Path $LocalSkillFile) {
    Copy-Item -Path $LocalSkillFile -Destination $DestFile -Force
} else {
    $FileUrl = "$RawBase/$SkillPath/SKILL.md"
    Write-Host "Downloading SKILL.md from $FileUrl..."
    Invoke-RestMethod -Uri $FileUrl -OutFile $DestFile
}

Write-Host ""
Write-Host "✔ Installation complete!" -ForegroundColor Green
Write-Host "Installed to: $DestFile"
Write-Host "Target Agent: $Agent"
