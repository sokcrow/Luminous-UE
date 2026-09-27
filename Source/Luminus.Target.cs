using UnrealBuildTool;
using System.Collections.Generic;

public class LuminusTarget : TargetRules
{
    public LuminusTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;
        ExtraModuleNames.Add("Luminus");
    }
}
