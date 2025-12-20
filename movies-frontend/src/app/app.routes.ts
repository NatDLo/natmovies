import { Routes } from '@angular/router';
import { UsersGuard } from './guards/users.guard';
import { Login } from './components/login/login';
import { Movies } from './components/movies/movies';
import { UserForm } from './components/users/users-form';
import { MoviesForm } from './components/movies/forms/movies-form';


export const routes: Routes = [
    { path: 'login', component: Login},
    
    { path: 'users/create', component: UserForm},
    { path: 'profile', component: UserForm, canActivate: [UsersGuard]},
    { path: 'users/:id', component: UserForm, canActivate: [UsersGuard]},

    { path: 'movies', component: Movies, canActivate: [UsersGuard]},
    { path: 'movies/:id/edit', component: MoviesForm, canActivate: [UsersGuard]},
    { path: 'movies/create', component: MoviesForm, canActivate: [UsersGuard]},
    { path: 'movies/view/:id', component: Movies, canActivate: [UsersGuard]},   

    { path: '', redirectTo: 'movies', pathMatch: 'full'},

];
