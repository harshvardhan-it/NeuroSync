import NeuralParticles from "../workspace/NeuralParticles";

export default function DashboardScene() {
  return (
    <>
      <NeuralParticles />

      {/* Left Wine Glow */}
      <div
        className="
          absolute
          left-[-250px]
          top-[20%]
          w-[700px]
          h-[700px]
          rounded-full
          blur-[160px]
          animate-neural-float
          pointer-events-none
        "
        style={{
          background: "rgba(179,38,74,0.12)",
        }}
      />

      {/* Right Gold Glow */}
      <div
        className="
          absolute
          right-[-250px]
          top-[10%]
          w-[700px]
          h-[700px]
          rounded-full
          blur-[160px]
          animate-neural-float-reverse
          pointer-events-none
        "
        style={{
          background: "rgba(231,183,95,0.12)",
        }}
      />
    </>
  );
}