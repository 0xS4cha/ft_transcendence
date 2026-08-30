import heroBg from '@/assets/hero-bg.png';

export function Hero() {
  return (
    <section className="relative w-full -mt-16 aspect-2/1 min-h-120 overflow-hidden bg-[#07070B]">
      <img
        src={heroBg}
        alt="Tactyx abstract background"
        className="absolute inset-0 h-full w-full object-contain object-top">
      </img>
      <div className="relative z-10 flex h-full w-full items-end pb-16">
        <div className="mx-auto w-full max-w-7xl px-8 md:px-16">
          <h1 className="text-4xl font-extrabold tracking-tight text-black sm:text-5xl md:text-6xl">
            Stop guessing, start{' '}
            <span className="bg-linear-to-r from-[#8EAEFF] via-[#A6B8FF] to-[#E8B5FF] bg-clip-text text-transparent">
              winning.
            </span>
          </h1>

          <p className="mt-4 max-w-xl text-sm font-medium text-black/80 sm:text-base">
            Real stats from millions of ranked games, refreshed each patch.
          </p>
        </div>
      </div>
    </section>
  );
}