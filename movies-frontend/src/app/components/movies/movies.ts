import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MoviesService } from '../../services/movies.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Movie } from '../../models/movies.model';

@Component({
  selector: 'app-movies',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './movies.html',
})
export class Movies implements OnInit {
  loading = false;
  movies: Movie[] = []
  selectedMovie: Movie | null = null;
  totalMovies = 0;
  currentPage = 1;
  nextPage: string | null = '';
  previousPage: string | null = '';
  totalPages = 1;

  genres: string[] = [
    'Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Drama', 'Fantasy',
    'Horror', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'Documentary'
  ];
  ratings: number[] = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5];

  filters = {
    genre: '',
    rating: null as number | null,
  };

  get selectedCast(): string {
    const cast = this.selectedMovie?.cast;
    if (!cast) return '';
    return Array.isArray(cast) ? cast.join(', ') : cast;
  }

  constructor(
    private moviesService: MoviesService,
    private route: ActivatedRoute,
    private router: Router,
    private cdr: ChangeDetectorRef // Injected ChangeDetectorRef for manual change detection
  ) {}

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      if (params['genre']) {
        this.filters.genre = params['genre'];
      } else {
        this.filters.genre = '';
      }
      this.currentPage = 1;
      this.loadMovies();
    });
  }

  getTotalMoviesFiltrados(): number {
    return this.totalMovies;
  }

  loadMovies() {
    this.loading = true;

    const filters: any = {};

    if (this.filters.genre) {
      filters.genre = this.filters.genre;
    }
    if (this.filters.rating !== null) {
      filters.rating = Number(this.filters.rating);
    }

    this.moviesService.getMovies(this.currentPage, filters).subscribe({
      next: (data) => {
        this.movies = (data.results || [])
          .slice()
          .sort((a, b) => {
            const at = (a.title || '').toLowerCase();
            const bt = (b.title || '').toLowerCase();
            return at.localeCompare(bt);
          });
        this.totalMovies = data.count || 0;
        this.nextPage = data.next;
        this.previousPage = data.previous;
        this.totalPages = Math.ceil(this.totalMovies / 10); // Assuming 10 items per page
        this.loading = false;
        this.cdr.detectChanges(); // Force UI update after data load
      },
      error: (error) => {
        console.error('Error loading movies', error);
        this.loading = false;
        this.cdr.detectChanges(); // Force UI update after error
      },
    });
  }

  viewMovieDetails(movie: Movie) {
    this.selectedMovie = movie;
  }
  
  updateMovie(movie: Movie) {
    this.router.navigate(['/movies', movie.id, 'edit']);
  }

  createMovie() {
    this.router.navigate(['/movies/create']);
  }

  deleteMovie(movie: Movie) {
    if (confirm(`Are you sure you want to delete the movie "${movie.title}"?`)) {
      this.moviesService.deleteMovie(movie.id).subscribe({
        next: () => {
          this.loadMovies();
          if (this.selectedMovie && this.selectedMovie.id === movie.id) {
            this.selectedMovie = null;
          }
        },
        error: (error) => {
          console.error('Error deleting movie', error);
        },
      });
    }
  }

  closeMovieDetails() {
    this.selectedMovie = null;
  }

  applyFilters() {
    this.currentPage = 1;
    this.loadMovies();
  }

  clearFilters() {
    this.filters.genre = '';
    this.filters.rating = null;
    this.currentPage = 1;
    this.loadMovies();
  }


}
