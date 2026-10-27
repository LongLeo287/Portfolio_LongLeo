$ErrorActionPreference = "Stop"

$browserId = "3b097077"
$bskPath = Join-Path $env:USERPROFILE ".local\bin\bsk.exe"

if (-not (Test-Path -LiteralPath $bskPath -PathType Leaf)) {
    throw "BrowserSkill CLI not found at '$bskPath'. Reconnect/install BrowserSkill for the existing LongLeo profile before retrying."
}

& $bskPath session start --browser $browserId --json
if ($LASTEXITCODE -ne 0) {
    throw "BrowserSkill could not connect to LongLeo (instance $browserId). Reconnect this profile; no alternate browser instance will be selected."
}
