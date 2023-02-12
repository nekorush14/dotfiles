# Deploy client click once app command
msbuild $CSPROJ_FILE -t:"clean;rebuild;publish;CopyPublishedApplication" -p:Configuration=Release -p:PublishUrl="$PublishUrl" -p:MapFileExtensions=true -p:BootstrapperEnabled=true -p:ApplicationVersion="0.0.0.*" -p:ApplicationRevision="0"

# Required configs
# Add .csproj

# <Target Name="CopyPublishedApplication">
#   <ItemGroup>
#     <MySourceFiles Include="$(PublishDir)**\*.*" Exclude="$(PublishDir)$(AssemblyName).exe" />
#   </ItemGroup>
#   <PropertyGroup>
#     <AppricationDir>$(_DeploymentApplicationDir.Substring($(PublishDir.Length)))</AppricationDir>
#   </PropertyGroup>
#   <Copy SourceFiles="@(MySourceFiles)" DestinationFiles="@(MySourceFiles->'$(PublishUrl)%(RecursiveDir)%(Filename)%(Extension)')" />
# </Target>

# Deploy web app for IIS command
msbuild $WEB_CS_PROJ_FILE -t:"clean;rebuild" -p:Configuration=Release -p:PublishDir="C:\Program-Release\WpfApp1\web\" -p:PublishProfile="FolderProfile.pubxml" -p:DeployOnBuild=true -p:DeployTarget=WebPublish

