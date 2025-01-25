export const allTools = ["run_coder_agent", "run_git_agent", "run_docs_agent"];

export async function copyToClipboard(text: string) {
  try {
    await navigator.clipboard.writeText(text);
  } catch (err) {
    console.error('Failed to copy text: ', err);
  }
}
