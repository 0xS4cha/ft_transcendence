import { cn } from '@/lib/utils';

interface StatItem {
	readonly value: string;
	readonly label: string;
	readonly highlight?: boolean;
}

const STATS: readonly StatItem[]= [
	{ value: '2.4M', label : 'games analyzed', highlight: false},
	{ value: '140+', label : 'teams ranked', highlight: false },
	{ value: '#1', label : 'team builder', highlight: true },
	{ value: '>10m', label : 'to update after every patch', highlight: false },
];

export default function Appstat(){
	return (
		<div className="mx-auto w-full max-w-7xl px-4 sm:px-6 -mt-16 sm:-mt-20 md:-mt-24">
      <div className="grid grid-cols-2 gap-5 sm:gap-5 md:grid-cols-4 h-28 sm:h-32 md:h-36">
        {STATS.map((stat) => (
          <div key={stat.label}
          className="flex flex-col items-center 
                    justify-center rounded-xl border 
                    border-white/10 bg-transparent p-5 text-center 
                    backdrop-blur-sm transition-colors 
                    hover:border-white/10 hover:bg-white/[0.04]">
            <span className={cn('text-2xl font-black tracking-tight sm:text-3xl text-white', stat.highlight &&
              'bg-linear-to-r from-[#93C5FD] via-[#38E1FF] to-[#70A6FF] bg-clip-text text-transparent')}>
              {stat.value}
            </span>
            <span className={cn('mt-1 text-xs text-neutral-400', stat.highlight &&
                  'bg-linear-to-r from-[#93C5FD] via-[#38E1FF] to-[#70A6FF] bg-clip-text font-semibold text-transparent')}>
              {stat.label}
            </span>
          </div>
        ))}
		  </div>
		</div>
	)
}