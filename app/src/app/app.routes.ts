import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { SignupComponent } from './signup/signup.component';
import { EventsComponent } from './events/events.component';
import { AboutComponent } from './about/about.component';

export const routes: Routes = [
  {'path': 'home', 'title': 'Home', component: HomeComponent, 'data':{'breadcrumb':'Home'}},
  {'path': '',   redirectTo: '/home', pathMatch: 'full' },
  {'path' : 'events', 'title' : 'Events page', component: EventsComponent},
  {'path' : 'about', 'title' : 'Sign Up page', component: AboutComponent},
  {'path' : 'login', 'title' : 'Log In page', component: LoginComponent},
  {'path' : 'signup', 'title' : 'Sign Up page', component: SignupComponent},
  
];
