import { useState } from "react";

import WorkspaceHero from "../components/workspace/WorkspaceHero";
import WorkspaceScene from "../components/workspace/WorkspaceScene";
import AICopilot from "../components/workspace/AICopilot";

export default function WorkspacePage() {
  const [datasetMeta, setDatasetMeta] =
    useState(
      JSON.parse(
        localStorage.getItem(
          "dataset_meta"
        ) || "{}"
      )
    );

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

      <WorkspaceHero
        setDatasetMeta={
          setDatasetMeta
        }
      />

      <div className="mt-8">
        <AICopilot
          datasetMeta={
            datasetMeta
          }
        />
      </div>
    </main>
  );
}