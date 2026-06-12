export default function NeuralParticles() {
  const particles = Array.from(
    { length: 24 },
    (_, i) => ({
      id: i,
      left: Math.random() * 100,
      top: Math.random() * 100,
      size: Math.random() * 4 + 2,
      duration: Math.random() * 12 + 8,
      delay: Math.random() * 5,
      color:
        i % 2 === 0
          ? "#E7B75F"
          : "#B3264A",
    })
  );

  return (
    <div
      className="
        absolute
        inset-0
        overflow-hidden
        pointer-events-none
      "
    >
      {particles.map((particle) => (
        <div
          key={particle.id}
          className="neural-particle"
          style={{
            left: `${particle.left}%`,
            top: `${particle.top}%`,
            width: `${particle.size}px`,
            height: `${particle.size}px`,
            background:
              particle.color,
            animationDuration:
              `${particle.duration}s`,
            animationDelay:
              `${particle.delay}s`,
          }}
        />
      ))}
    </div>
  );
}