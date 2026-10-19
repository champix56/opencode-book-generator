$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = Get-Command py -ErrorAction SilentlyContinue
if ($Python) { & py -3 (Join-Path $Root 'generators/bookgen.py') @args; exit $LASTEXITCODE }
$Python = Get-Command python -ErrorAction SilentlyContinue
if (-not $Python) { Write-Error 'Python 3 est requis.'; exit 127 }
& python (Join-Path $Root 'generators/bookgen.py') @args
exit $LASTEXITCODE
