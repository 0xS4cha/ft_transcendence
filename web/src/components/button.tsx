import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { buttonVariants } from '@/components/ui/button';
import { cn } from '@/lib/utils';

export function ButtonWrap() {
  return (
    <div className="flex flex-wrap items-center gap-2">
      <Link
        to="/builder"
        className={cn(
          buttonVariants({ variant: 'outline', size: 'lg' }),
          'cursor-pointer border-white/15 bg-white/[0.03] text-sm font-medium text-white shadow-sm transition-all duration-150 hover:border-white/30 hover:bg-white/10 hover:text-white group flex items-center gap-2'
        )}
      >
        <span>Go to app</span>
        <ArrowRight className="h-4 w-4 text-neutral-400 transition-transform duration-150 group-hover:translate-x-1 group-hover:text-white" />
      </Link>
    </div>
  );
}