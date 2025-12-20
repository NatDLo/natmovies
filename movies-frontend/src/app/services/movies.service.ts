import { Injectable } from "@angular/core";
import { HttpClient, HttpParams } from "@angular/common/http";
import { Observable } from "rxjs";
import { Movie } from "../models/movies.model";
import { baseUrl } from "./config";

interface PaginatedResponse<T> {
    count: number;
    next: string | null;
    previous: string | null;
    results: T[];
    }

@Injectable({ providedIn: 'root' })
export class MoviesService {
    private apiBase = baseUrl + 'movies/';

    constructor(private http: HttpClient) {}

    getMovies(
        page: number = 1,
        filters?: {
            genre?: string;
            rating?: number;
        }
    ): Observable<PaginatedResponse<Movie>> {
        let params = new HttpParams();
        if (filters) {
            if (filters.genre) params = params.set('genre', filters.genre);
            if (filters.rating !== undefined) params = params.set('rating', filters.rating.toString());
        }
        return this.http.get<PaginatedResponse<Movie>>(`${this.apiBase}?page=${page}`, {
            params,
        });
    }

    getMovie(id: number): Observable<Movie> {
        return this.http.get<Movie>(`${this.apiBase}${id}/`);
    }

    createMovie(payload: Partial<Movie>): Observable<Movie> {
        const body: any = {
        title: payload.title,
        description: payload.description,
        director: payload.director,
        release_date: payload.release_date,
        genre: payload.genre,
        rating: payload.rating,
        cast: payload.cast,
        };
        return this.http.post<Movie>(`${this.apiBase}`, body);
    }

    updateMovie(id: number, payload: Partial<Movie>): Observable<Movie> {
        const body: any = {
        title: payload.title,
        description: payload.description,
        director: payload.director,
        release_date: payload.release_date,
        genre: payload.genre,
        rating: payload.rating,
        cast: payload.cast,
        };
        return this.http.put<Movie>(`${this.apiBase}${id}/`, body);
    }

    deleteMovie(id: number): Observable<void> {
        return this.http.delete<void>(`${this.apiBase}${id}/`);
    }


}