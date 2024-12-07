import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-verify',
  templateUrl: './verify.component.html',
  styleUrls: ['./verify.component.css'],
  imports: [ReactiveFormsModule],
  standalone: true
})
export class VerifyComponent {
  verifyForm = new FormGroup({
    email: new FormControl('', Validators.required),
    verification_code: new FormControl('', Validators.required),
  });

  private verifyUrl = 'http://127.0.0.1:8000/api/verify-code/';

  constructor(private http: HttpClient, private route: ActivatedRoute, private router: Router) {
    // Pre-fill the email from query parameters
    this.route.queryParams.subscribe((params) => {
      this.verifyForm.patchValue({ email: params['email'] });
    });
  }

  onVerifySubmit() {
    const verifyData = this.verifyForm.value;

    this.http.post<any>(this.verifyUrl, verifyData).subscribe(
      (response) => {
        console.log('Verification successful:', response);
        this.router.navigate(['/login']); // Redirect to login after success
      },
      (error) => {
        console.error('Verification failed:', error);
      }
    );
  }
}
