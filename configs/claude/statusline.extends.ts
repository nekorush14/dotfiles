/**
 * Local configuration for statusline
 * This file can be customized per environment and should not be committed
 *
 * Example: Map ARN inference profile IDs to custom model names
 */

// Map of ARN suffix IDs to display names
const arnModelMap: Record<string, string> = {
  // Add your ARN ID mappings here
  "your-inference-profile-id-haiku": "Haiku 4.5",
  "your-inference-profile-id-sonnet": "Sonnet 4.5",
  "your-inference-profile-id-opus": "Opus 4.5",
};

/**
 * Returns the display name for the model
 * @param displayName - The raw model display name from session data
 * @returns Formatted model name for display
 */
export function getModelDisplayName(displayName: string | undefined): string {
  if (!displayName) {
    return "Unknown";
  }

  // AWS Inference Profile ARN pattern: arn:aws:bedrock:region:account:inference-profile/id
  if (displayName.startsWith("arn:aws:")) {
    // Extract the ID from the end of the ARN
    const arnParts = displayName.split("/");
    const profileId = arnParts[arnParts.length - 1];

    // Check if we have a custom name for this profile ID
    if (profileId && arnModelMap[profileId]) {
      return `${arnModelMap[profileId]} by AWS`;
    }

    return "by AWS";
  }

  return displayName;
}
