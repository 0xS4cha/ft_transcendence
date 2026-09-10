import { Grid, Search } from "lucide-react";
import { SelectDemo } from "./select_set";

export default function BuilderChampionsBar()
{
	return (
		<div className="flex items-center rounded-xl border border-white/10 bg-[#202020]">
			<header>
				<Search>Search for a champion...</Search>
			</header>
		</div>
	)
}