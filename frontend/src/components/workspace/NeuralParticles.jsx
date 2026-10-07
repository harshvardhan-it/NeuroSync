export default function NeuralParticles() {
  const particles = Array.from(
    { length: 24 },
    (_, i) => ({
      id: i,
      left: ((i * 37) % 100),
      top: ((i * 37) % 100),
      size: (i % 3) + 2,
      duration: (i % 5) + 8,
      delay: (i % 4),
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