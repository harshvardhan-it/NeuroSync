import WorkspaceHero from "../components/workspace/WorkspaceHero";
import PromptSuggestions from "../components/workspace/PromptSuggestions";
import WorkspaceScene from "../components/workspace/WorkspaceScene";

export default function WorkspacePage() {
  return (
    <main
      className="
        relative
        min-h-screen
        overflow-hidden
      "
      style={{
        background: "#05060A",
      }}
    >
      <WorkspaceScene />

      <WorkspaceHero />

      <PromptSuggestions />
    </main>
  );
}