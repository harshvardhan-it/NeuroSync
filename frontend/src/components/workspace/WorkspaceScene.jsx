import NeuralParticles from "./NeuralParticles";

export default function WorkspaceScene() {
  return (
    <>
      <NeuralParticles />

      {/* Left Wine Glow */}

      <div
        className="
          absolute
          left-[-250px]
          top-[25%]
          w-[700px]
          h-[700px]
          rounded-full
          blur-[160px]
          animate-neural-float
        "
        style={{
          background:
            "rgba(179,38,74,0.12)",
        }}
      />

      {/* Right Gold Glow */}

      <div
        className="
          absolute
          right-[-250px]
          top-[20%]
          w-[700px]
          h-[700px]
          rounded-full
          blur-[160px]
          animate-neural-float-reverse
        "
        style={{
          background:
            "rgba(231,183,95,0.12)",
        }}
      />
    </>
  );
}