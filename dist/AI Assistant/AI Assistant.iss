#define MyAppName "AI Assistant"
#define MyAppVersion "1.0"
#define MyAppPublisher "Your Name"
#define MyAppExeName "AI Assistant.exe"

[Setup]
AppId={{D7D7E7E2-8F61-4F9C-9D5F-123456789ABC}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\AI Assistant
DefaultGroupName={#MyAppName}
OutputDir=Output
OutputBaseFilename=AI Assistant Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"

[Files]
Source: "C:\Users\rutik\OneDrive\Desktop\AI Assisstant\ai-assistant\dist\AI Assistant\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\AI Assistant"; Filename: "{app}\AI Assistant.exe"
Name: "{autodesktop}\AI Assistant"; Filename: "{app}\AI Assistant.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\AI Assistant.exe"; Description: "Launch AI Assistant"; Flags: nowait postinstall skipifsilent