export interface Movie {
    id: number;
    title: string;
    description?: string;
    genre?: string;
    release_date?: string; //ISO yyyy-mm-dd
    rating?: number;
    director?: string;
    cast?: string[];  // backend JSONField
}

export interface PaginatedMovies {
    results: Movie[];
    count: number;
    next: string | null;
    previous: string | null;
}