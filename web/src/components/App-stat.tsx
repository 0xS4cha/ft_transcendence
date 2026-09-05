interface StatItem {
	readonly value: string;
	readonly label: string;
	readonly highlight?: boolean;
}

const STATS: readonly StatItem[]= [
	{ value: '2.4M', label : 'games analyzed' },
	{ value: '140+', label : 'teams ranked' },
	{ value: '#1', label : 'team builder' },
	{ value: '>10m', label : 'to update after every patch' },
];

export default function Appstat(){
	return (
		<div className="mx-auto w-full max-w-7xl px-4 sm:px-6 -mt-16 sm:-mt-20 md:-mt-24">
      <div className="grid grid-cols-2 gap-5 sm:gap-5 md:grid-cols-4 h-28 sm:h-32 md:h-36">
        {STATS.map((stat) => (
          <div
          key={stat.label}
          className="flex flex-col items-center 
                    justify-center rounded-xl border 
                    border-white/10 bg-transparent p-5 text-center 
                    backdrop-blur-sm transition-colors 
                    hover:border-white/10 hover:bg-white/[0.04]"
          >
            <span
              className={`text-2xl font-black tracking-tight sm:text-3xl ${
                stat.highlight
                  ? 'bg-gradient-to-r from-[#4E80EE] to-[#38E1FF] bg-clip-text text-transparent'
                  : 'text-white'
              }`}>
                {stat.value}
            </span>
            <span className="mt-1 text-xs text-neutral-400">
              {stat.label}
            </span>
          </div>
        ))}
		  </div>
		</div>
	)
}