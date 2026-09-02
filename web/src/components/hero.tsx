import heroBg from '@/assets/hero-bg.png';

export function Hero() {
  return (
    <div className="w-full">
      <section className="relative flex h-72 w-full flex-col justify-center items-center overflow-hidden  border border-white/5 sm:h-96 md:h-[420px]">
        <img
          src={heroBg}
          alt="tactyx hero banner"
          className="absolute inset-0 h-full w-full object-cover object-center"
        />

        <div className="absolute inset-0 bg-gradient-to-t from-[#07070B] via-[#07070B]/30 via-25% to-transparent" />

        <div className="relative z-10 flex flex-col items-start p-6 sm:p-10 md:p-12">
          <h1 className="text-left text-3xl font-extrabold tracking-tight text-white sm:text-4xl md:text-5xl lg:text-6xl">
            Stop guessing, start{' '}
            <span className="bg-gradient-to-r from-[#4E80EE] via-[#38E1FF] to-[#70A6FF] bg-clip-text text-transparent">
              winning.
            </span>
          </h1>

          <p className="mt-2 text-left text-xs font-normal text-neutral-300 sm:mt-3 sm:text-sm md:text-base">
            Real stats from millions of ranked games, refreshed each patch.
          </p>
        </div>
      </section>

      <div className="mt-8 space-y-6">
      </div>
    </div>
  );
}