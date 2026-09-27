using UnrealBuildTool;

public class Luminus : ModuleRules
{
    public Luminus(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(new string[]
        {
            "Core",
            "CoreUObject",
            "Engine",
            "InputCore",
            "EnhancedInput",
            "Paper2D"
        });

        PrivateDependencyModuleNames.AddRange(new string[]
        {
            "UMG",
            "Slate",
            "SlateCore"
        });
    }
}
