#define MyAppName "OBS Recording Overlay"
#define MyAppVersion "1.0"

[Setup]
AppId={#MyAppName}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={commonpf64}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=..\setup_output
OutputBaseFilename={#MyAppName} - Setup v{#MyAppVersion}
UninstallDisplayIcon={app}\{#MyAppName}.exe
UninstallDisplayName={#MyAppName}
SetupIconFile=logo.ico
WizardImageFile=logo-WizardImageFile.bmp
WizardSmallImageFile=logo-WizardSmallImageFile.bmp
SetupMutex=SetupMutex{#SetupSetting("AppId")}

[Files]
Source: "..\dist\app\{#MyAppName}.exe"; DestDir: "{app}";
Source: "..\dist\app\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppName}.exe";
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppName}.exe";
Name: "{userstartup}\{#MyAppName}"; Filename: "{app}\{#MyAppName}.exe"; Tasks:StartAtStartup;

[Tasks]
Name: "StartAtStartup"; Description: "Start {#MyAppName} at Windows startup"; GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
Filename: "{app}\{#MyAppName}.exe"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent