import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { RouterLink } from '@angular/router';
import { NavbarComponent } from '../navbar/navbar.component';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [ReactiveFormsModule, HttpClientModule, RouterLink, NavbarComponent], // Add HttpClientModule here
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent {
  loginForm = new FormGroup({
    username: new FormControl('', Validators.required),
    email: new FormControl('', [Validators.required, Validators.email]),
    number: new FormControl('', Validators.required),
    password: new FormControl('', [Validators.required, Validators.minLength(8)])
  });

  private apiUrl = 'http://localhost:3002/user-create'; // Mockoon or backend URL

  constructor(private http: HttpClient) {}

  signup(data: any): Observable<any> {
    return this.http.post<any>(this.apiUrl, data);
  }

  onSignupSubmit() {
    // Collect the form data
    const signupData = this.loginForm.value;

    // Make the POST request
    this.signup(signupData).subscribe(
      (response) => {
        console.log('Signup successful:', response);
      },
      (error) => {
        console.error('Signup failed:', error);
      }
    );
  }
}
