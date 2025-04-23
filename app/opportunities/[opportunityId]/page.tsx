import { Opportunity } from "@/lib/types";
import { notFound } from "next/navigation";

export default async function OpportunityDetails({
	params,
}: {
	params: {opportunityId:string}
}) {
	const {opportunityId} = await params
	const res = await fetch(`http://localhost:5000/api/opportunities/${opportunityId}`);
	const opportunity: Opportunity = await res.json();
	
	if (Object.keys(opportunity).length === 0){
		return notFound()
	}

	return (
		<main>
        <div className="px-8">
          <div className="max-w-screen-xl py-4 md:py-8 mx-auto lg:max-w-none">
			<h1 className="max-w-screen mb-4 text-xl font-bold tracking-tight leading-none md:text-2xl xl:text-3xl dark:text-white italic">{opportunity.title}</h1>
			<div className="grid lg:items-center grid-cols-2 md:grid-cols-10 lg:grid-cols-12 gap-16">
				<div className="my-0 col-span-2 lg:col-span-8 md:col-span-8">
					{opportunity.description.map((sentence, i) => (
						<p className="my-4 indent-8" key={i}>{`${sentence}`}</p>
					))}
				</div>
				<div className="grid lg:grid-cols-4 place-self-start lg:col-span-4 gap-8">
					<div className="lg:col-span-2">
						<h1 className="font-medium italic">Interests</h1>
						<ul>
							{opportunity.interests.map((interest, i) => (
								<li key={i}>{interest}</li>
							))}
						</ul>
					</div>
					<div className="lg:col-span-2">
						<h1 className="font-medium italic">Location</h1>
						<p>{opportunity.location}</p>
					</div >
					<div className="lg:col-span-2">
						<h1 className="font-medium italic">Organization</h1>
						<p>{opportunity.organization}</p>
					</div>
					<div className="lg:col-span-2">
						<h1 className="font-medium italic">Remaining Spots</h1>
						<p>{opportunity.remaining_spots}</p>
					</div>
					<div className="lg:col-span-2">
						<h1 className="font-medium italic">Requirements</h1>
						<ul>
							{opportunity.requirements.map((requirement, i) => (
								<li key={i}>{requirement}</li>
							))}
						</ul>
					</div>
					<div className = "lg:col-span-4">
						<h1 className="font-medium italic">Shifts</h1>
						<ul>
							{opportunity.shifts.map((shift, i) => (
								<li key={i}>{shift.date} @ {shift.start_time} to {shift.end_time}</li>
							))}
						</ul>
					</div>
				</div>
			</div>
          </div>
        </div>
      </main>
	)
}