import { Opportunity } from "@/lib/types";

export default async function OpportunityDetails({
	params,
}: {
	params: {opportunityId:string}
}) {
	const res = await fetch(`http://localhost:5000/api/opportunities/${params.opportunityId}`);
	const opportunity: Opportunity = await res.json();
	return (
		<div>
			<h1>Title: {opportunity.title}</h1>
			<div>
				<h1>Description</h1>
				<ul>
					{opportunity.description.map((sentence, i) => (
						<li key={i}>{sentence}</li>
					))}
				</ul>
			</div>
			<div>
				<h1>Interests</h1>
				<ul>
					{opportunity.interests.map((interest, i) => (
						<li key={i}>{interest}</li>
					))}
				</ul>
			</div>
			<div>
				<h1>Location</h1>
				<p>{opportunity.location}</p>
			</div>
			<div>
				<h1>Organization</h1>
				<p>{opportunity.organization}</p>
			</div>
			<div>

				<h1>Remaining Spots</h1>
				<p>{opportunity.remaining_spots}</p>
			</div>
			<div>

				<h1>Requirements</h1>
				<ul>
					{opportunity.requirements.map((requirement, i) => (
						<li key={i}>{requirement}</li>
					))}
				</ul>
			</div>
			<div>

				<h1>Shifts</h1>
				<ul>
					{opportunity.shifts.map((shift, i) => (
						<li key={i}>{shift.date} @ {shift.start_time} to {shift.end_time}</li>
					))}
				</ul>
			</div>
		</div>
	)
}