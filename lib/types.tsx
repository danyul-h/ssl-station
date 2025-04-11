interface Shift{
    date: string;
    duration: string;
    end_time: string;
    start_time: string;
    total_spots: string;
    vacant_spots: string;
}

interface Opportunity{
    date: string;
    description: string[];
    id: string;
    interests: string[]
    location: string;
    organization: string;
    remaining_spots: string;
    requirements: string[]
    shifts: Shift[];
    time: string;
    title: string;
}

export type {
    Shift,
    Opportunity,
};