import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import { SignupComponent } from './signup/signup.component';
import { EventsComponent } from './events/events.component';
import { AboutComponent } from './about/about.component';
import { BidComponent } from './bid/bid.component';
import { VerifyComponent } from './verify/verify.component';

export const routes: Routes = [
  {'path': 'home', 'title': 'Home', component: HomeComponent, 'data':{'breadcrumb':'Home'}},
  {'path': '',   redirectTo: '/home', pathMatch: 'full' },
  {'path' : 'events', 'title' : 'Events page', component: EventsComponent},
  {'path' : 'about', 'title' : 'About page', component: AboutComponent},
  {'path' : 'login', 'title' : 'Log In page', component: LoginComponent},
  {'path' : 'signup', 'title' : 'Sign Up page', component: SignupComponent},
  {'path' : 'bid', 'title' : 'Bid Page', component: BidComponent},
  {'path' : 'verify', 'title' : 'Verify Page', component: VerifyComponent}
];
