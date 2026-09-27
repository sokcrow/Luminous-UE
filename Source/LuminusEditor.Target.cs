using UnrealBuildTool;
using System.Collections.Generic;

public class LuminusEditorTarget : TargetRules
{
    public LuminusEditorTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Editor;
        ExtraModuleNames.Add("Luminus");
    }
}
