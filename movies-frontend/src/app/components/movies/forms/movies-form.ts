import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { MoviesService } from '../../../services/movies.service';

@Component({
  selector: 'app-movies-form',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './movies-form.html',
})
export class MoviesForm implements OnInit {
  // Reactive form instance
  movieForm!: FormGroup;

  // Predefined genres for the select input
  genres: string[] = [
    'Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Drama', 'Fantasy',
    'Horror', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'Documentary'
  ];

  // Edit state
  movieId: number | null = null;
  editMode = false;
  isSaving = false;

  constructor(
    private readonly moviesService: MoviesService,
    private readonly router: Router,
    private readonly route: ActivatedRoute,
    private readonly fb: FormBuilder,
  ) {
    // Build form controls and validators
    this.movieForm = this.fb.group({
      title: ['', [Validators.required, Validators.minLength(1)]],
      genre: ['', [Validators.required]],
      release_date: [''],                           // yyyy-mm-dd
      rating: [null, [Validators.min(0), Validators.max(10)]],
      director: [''],
      description: [''],
      // Use a comma-separated string in the UI; convert to string[] before sending
      cast: [''],
    });
  }

  ngOnInit(): void {
    // Detect edit mode by route param `id` and load the movie
    this.route.paramMap.subscribe(params => {
      const idParam = params.get('id');
      if (!idParam) return;

      const id = Number(idParam);
      if (Number.isNaN(id)) return;

      this.editMode = true;
      this.movieId = id;

      this.moviesService.getMovie(id).subscribe(movie => {
        // Patch form with server data
        this.movieForm.patchValue({
          title: movie.title ?? '',
          genre: movie.genre ?? '',
          // Ensure ISO date string fits the <input type="date">
          release_date: (movie.release_date ?? '').slice(0, 10),
          rating: movie.rating ?? null,
          director: movie.director ?? '',
          description: movie.description ?? '',
          // Convert string[] -> comma separated string for the input
          cast: Array.isArray(movie.cast) ? movie.cast.join(', ') : '',
        });
      });
    });
  }

  // Submit handler (create or update based on editMode)
  saveMovie(): void {
    if (this.isSaving) return;

    if (this.movieForm.invalid) {
      this.movieForm.markAllAsTouched();
      return;
    }

    this.isSaving = true;

    // Build payload and normalize fields
    const v = this.movieForm.value as any;

    // Normalize cast: "a, b, c" -> ["a","b","c"]
    const castArray =
      typeof v.cast === 'string' && v.cast.trim().length
        ? v.cast.split(',').map((s: string) => s.trim()).filter((s: string) => s.length)
        : [];

    const payload: any = {
      title: (v.title ?? '').trim(),
      genre: v.genre,
      release_date: v.release_date || null, // send null if empty
      rating: v.rating !== null && v.rating !== '' ? Number(v.rating) : null,
      director: (v.director ?? '').trim(),
      description: (v.description ?? '').trim(),
      cast: castArray,
    };

    // Choose create or update
    const req$ = this.editMode && this.movieId
      ? this.moviesService.updateMovie(this.movieId, payload)
      : this.moviesService.createMovie(payload);

    req$.subscribe({
      next: () => this.router.navigate(['/movies']),
      error: (e) => {
        console.error('Error saving movie', e);
        this.isSaving = false;
      },
      complete: () => (this.isSaving = false),
    });
  }

  // Navigate back to list
  navigateToMovies(): void {
    this.router.navigate(['/movies']);
  }

  // Convenience getter for template access (e.g., f.title.invalid)
  get f() {
    return this.movieForm.controls;
  }
}