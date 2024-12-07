import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Router, RouterLink } from '@angular/router';
import { NavbarComponent } from '../navbar/navbar.component';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [ReactiveFormsModule, HttpClientModule, RouterLink, NavbarComponent, CommonModule],
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css'],
})
export class SignupComponent {
  signupForm = new FormGroup({
    username: new FormControl('', Validators.required),
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [Validators.required, Validators.minLength(8)]),
  });

  private apiUrl = 'http://127.0.0.1:8000/api/user-create/';

  constructor(private http: HttpClient, private router: Router) {}

  signup(data: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, data);
  }

  onSignupSubmit() {
    // Collect the form data
    const signupData = this.signupForm.value;

    // Make the POST request
    this.signup(signupData).subscribe(
      (response) => {
        console.log('Signup successful:', response);
        // Redirect to the verification page, passing the email as a query parameter
        this.router.navigate(['/verify'], { queryParams: { email: signupData.email } });
      },
      (error) => {
        console.error('Signup failed:', error);
      }
    );
  }
}
