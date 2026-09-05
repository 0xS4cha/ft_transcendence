import heroBg from '@/assets/hero-bg.png';
import Appstat from './App-stat';

export function Hero() {
  return (
    <div className="w-full">
      <section className="relative flex h-72 w-full flex-col justify-center items-left overflow-hidden h-[65vh]">
        <img
          src={heroBg}
          alt="tactyx hero banner"
          className="absolute inset-0 h-full w-full "
        />

        <div className="absolute inset-0 bg-gradient-to-t from-[#07070B] via-[#07070B]/50 via-15% to-transparent" />

        <div className="relative z-10 flex flex-col items-start p-6 sm:p-10 md:p-12">
          <h1 className="text-left text-3xl font-extrabold tracking-tight text-[#07070B] sm:text-4xl md:text-5xl lg:text-6xl">
            Stop guessing, start{' '}
            <span className="bg-linear-to-r from-[#93C5FD] via-[#38E1FF] to-[#70A6FF] bg-clip-text text-transparent">
              winning.
            </span>
          </h1>

          <p className="mt-2 text-left text-xs font-normal text-[#07070B] sm:mt-3 sm:text-sm md:text-base">
            Real stats from millions of ranked games, refreshed each patch.
          </p>
        </div>
      </section>
        <Appstat />
      <div className="mt-8 space-y-6">
      </div>
    </div>
  );
}