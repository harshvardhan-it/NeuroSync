const seededValue = (seed) => {
  const value = Math.sin(seed * 12.9898) * 43758.5453;
  return value - Math.floor(value);
};

const particles = Array.from({ length: 24 }, (_, index) => ({
  id: index,
  left: seededValue(index + 1) * 100,
  top: seededValue(index + 25) * 100,
  size: seededValue(index + 49) * 4 + 2,
  duration: seededValue(index + 73) * 12 + 8,
  delay: seededValue(index + 97) * 5,
  color: index % 2 === 0 ? "#E7B75F" : "#B3264A",
}));

export default function NeuralParticles() {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
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
