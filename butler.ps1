# Butler Mode - PowerShell Wrapper
# Usage: butler [command] [args...]

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

$butlerDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonExe = Join-Path $butlerDir "venv\Scripts\python.exe"
$butlerScript = Join-Path $butlerDir "butler.py"

# Run butler.py with all arguments
& $pythonExe $butlerScript @Arguments
