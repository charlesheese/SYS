import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule  } from '@angular/common/http';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-verify',
  templateUrl: './verify.component.html',
  styleUrls: ['./verify.component.css'],
  imports: [ReactiveFormsModule, HttpClientModule],
  standalone: true
})
export class VerifyComponent {
  verifyForm = new FormGroup({
    email: new FormControl('', Validators.required),
    verification_code: new FormControl('', Validators.required),
  });

  private verifyUrl = 'http://127.0.0.1:8000/api/verify-code/';

  constructor(private http: HttpClient, private route: ActivatedRoute, private router: Router) {
    this.route.queryParams.subscribe((params) => {
      if (params['email']) {
        this.verifyForm.patchValue({ email: params['email'] });
      } else {
        alert('Email is missing in the URL. Please sign up again.');
        this.router.navigate(['/signup']);
      }
    });
  }

  onVerifySubmit() {
    const verifyData = this.verifyForm.value;
    const email = verifyData.email;
  
    this.http.post<any>(`${this.verifyUrl}${email}/`, { verification_code: verifyData.verification_code }).subscribe(
      (response) => {
        console.log('Verification successful:', response);
        this.router.navigate(['/login']); // Redirect to login after success
      },
      (error) => {
        console.error('Verification failed:', error);
        // Display error to the user
        if (error.status === 400) {
          alert('Invalid verification code. Please try again.');
        } else {
          alert('An unexpected error occurred. Please try again later.');
        }
      }
    );
  }
}  
