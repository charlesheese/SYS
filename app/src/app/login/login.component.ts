import { Component } from '@angular/core';
import { NavbarComponent } from '../navbar/navbar.component';
import { CommonModule } from '@angular/common';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router, RouterLink } from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';


@Component({
  selector: 'app-login',
  standalone: true,
  templateUrl: './login.component.html',
  imports: [NavbarComponent, RouterLink, ReactiveFormsModule, HttpClientModule],
  styleUrl: './login.component.css',
})
export class LoginComponent {
  loginForm = new FormGroup({
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', Validators.required),
  });

  errorMessage: string = ''; // Holds error message for UI feedback

  constructor(private http: HttpClient, private router: Router) {}

  login() {
    if (this.loginForm.invalid) {
      this.errorMessage = 'Please fill in all required fields correctly.';
      return;
    }

    const loginData = this.loginForm.value; // Get form data
    const apiUrl = 'https://postgres-production-82f9.up.railway.app/api/login'; // Django API endpoint

    this.http.post(apiUrl, loginData).subscribe({
      next: (response: any) => {
        // Save the token in localStorage
        localStorage.setItem('token', response.token);

        // Redirect to a protected route (e.g., Dashboard)
        this.router.navigate(['/home']);
      },
      error: (error) => {
        console.error('Login error:', error);
        this.errorMessage = 'Invalid email or password. Please try again.';
      },
    });
  }
}
