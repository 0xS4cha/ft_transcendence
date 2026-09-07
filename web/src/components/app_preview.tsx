import BuilderPreview from '@/assets/builder.png';
import { ButtonWrap } from '@/components/button';

export function AppPreview() {
  return (
    <section className="relative w-full py-16 sm:px-34 sm:py-24">
      <div className="grid grid-cols-1 items-center gap-10 md:grid-cols-2">
        <div className="flex flex-col items-start relative z-10">
          <h2 className="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
            Trusted by the{' '}
            <span className="bg-linear-to-r from-[#93C5FD] via-[#38E1FF] to-[#70A6FF] bg-clip-text text-transparent">
                greatest{' '}
            </span>
            <span>
              players
            </span>
          </h2>
          <p className="mt-4 text-sm leading-relaxed text-neutral-400 sm:text-base">
            Optimized boards, early roll breakpoints and augment synergies
            used by Challenger lobbies around the globe.
          </p>
          <div className="py-5">
            <ButtonWrap />
          </div>
        </div>

        <div className="relative flex items-center justify-center">
          <div className="absolute" />

          <div className="relative">
            <img
              src={BuilderPreview}
              alt="Tactyx application interface preview"
              className="h-full w-full rounded-xl "
            />
          </div>
        </div>
      </div>
    </section>
  );
}