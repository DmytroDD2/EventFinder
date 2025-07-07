

type TypeUserReview = {
    id: number;
    rating: number;
    description: string;
    user_id: number;
    event_id: number;
    image_url?: string | null;
    name?: string | null;   
}


export type {
    TypeUserReview
}