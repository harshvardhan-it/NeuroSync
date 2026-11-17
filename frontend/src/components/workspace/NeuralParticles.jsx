export default function NeuralParticles() {
  const particles = Array.from({ length: 24 }, (_, index) => {
    const seed = index + 1;

    return {
      id: index,
      left: (seed * 37) % 100,
      top: (seed * 61) % 100,
      size: 2 + ((seed * 13) % 4),
      duration: 8 + ((seed * 7) % 12),
      delay: (seed * 11) % 5,
      color: index % 2 === 0 ? "#E7B75F" : "#B3264A",
    };
  });

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none" aria-hidden="true">
      {particles.map((particle) => (
        <div
          key={particle.id}
          className="neural-particle"
          style={{
            left: `${particle.left}%`,
            top: `${particle.top}%`,
            width: `${particle.size}px`,
            height: `${particle.size}px`,
            background: particle.color,
            animationDuration: `${particle.duration}s`,
            animationDelay: `${particle.delay}s`,
          }}
        />
      ))}
    </div>
  );
}
