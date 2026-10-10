param(
    [ValidateSet('Lint', 'Build', 'Run')]
    [string]$Action = 'Build',
    [string]$Sdk = ''
)

# 使用官方 SDK 校验源码或生成自带运行时的 Windows ZIP；不更改系统 PATH。
$ErrorActionPreference = 'Stop'
$projectRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
if (!$Sdk) {
    # 优先使用项目内只供开发的 SDK 副本，避免改写外部安装目录的编译缓存。
    $Sdk = Join-Path $projectRoot '.tools\renpy-8.2.0-sdk'
    # 外部 SDK 由环境变量或 -Sdk 指定，源码不记录开发者本机安装位置。
    if (!(Test-Path -LiteralPath $Sdk) -and $env:RENPY_SDK) { $Sdk = $env:RENPY_SDK }
}
$sdkRoot = [IO.Path]::GetFullPath($Sdk)
$runtimePython = Join-Path $sdkRoot 'lib\py3-windows-x86_64\python.exe'
$renpyScript = Join-Path $sdkRoot 'renpy.py'
$buildRoot = Join-Path $projectRoot 'build'
$distRoot = Join-Path $projectRoot 'dist'

if (!(Test-Path -LiteralPath $runtimePython) -or !(Test-Path -LiteralPath $renpyScript)) {
    throw "Ren'Py SDK not found. Pass -Sdk 'C:\path\to\renpy-sdk'."
}
New-Item -ItemType Directory -Force -Path $buildRoot, $distRoot | Out-Null

# 仅对当前进程生效：开发日志与存档凭据保留在工作区，不污染玩家存档。
$oldSaves = $env:RENPY_PATH_TO_SAVES
$oldLog = $env:RENPY_LOG_BASE
$env:RENPY_PATH_TO_SAVES = Join-Path $buildRoot 'saves'
$env:RENPY_LOG_BASE = $buildRoot

try {
    Push-Location $projectRoot
    if ($Action -eq 'Run') {
        & $runtimePython $renpyScript $projectRoot run
        if ($LASTEXITCODE -ne 0) { throw "Ren'Py exited with code $LASTEXITCODE." }
    } else {
        $lintLog = Join-Path $buildRoot 'lint.txt'
        & $runtimePython $renpyScript $projectRoot lint 2>&1 | Tee-Object -FilePath $lintLog
        if ($LASTEXITCODE -ne 0) { throw "Ren'Py lint failed; see $lintLog." }
        if ($Action -eq 'Build') {
            # SDK 对每个文件输出进度；完整保留在日志中，控制台只显示最终结果。
            $distributionLog = Join-Path $buildRoot 'distribution.txt'
            Write-Host 'Building Windows distribution...'
            & $runtimePython $renpyScript (Join-Path $sdkRoot 'launcher') distribute $projectRoot --package win --destination $distRoot *> $distributionLog
            if ($LASTEXITCODE -ne 0) {
                Get-Content -LiteralPath $distributionLog -Tail 40
                throw "Ren'Py distribution failed; see $distributionLog."
            }
            Get-ChildItem -LiteralPath $distRoot -File -Filter '*-win.zip' |
                Sort-Object LastWriteTime -Descending |
                Select-Object -First 1 FullName, Length, LastWriteTime
        }
    }
} finally {
    Pop-Location
    $env:RENPY_PATH_TO_SAVES = $oldSaves
    $env:RENPY_LOG_BASE = $oldLog
}
