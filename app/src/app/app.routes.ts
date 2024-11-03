import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';

export const routes: Routes = [
  {'path': 'home', 'title': 'Home', component: HomeComponent, 'data':{'breadcrumb':'Home'}},
  {'path': '',   redirectTo: '/home', pathMatch: 'full' },
  {'path' : 'login', 'title' : 'Login page', component: LoginComponent},
  
];
