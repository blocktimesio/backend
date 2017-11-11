import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { routerTransition } from '../router.animations';
import { Http, Response } from '@angular/http';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
    selector: 'app-login',
    templateUrl: './login.component.html',
    styleUrls: ['./login.component.scss'],
    animations: [routerTransition()]
})
export class LoginComponent {
    public signInForm: FormGroup;
    public errorMessage: string = null;

    constructor(private http: Http, public router: Router, private fb: FormBuilder) {
        this.signInForm = fb.group({
            'username' : [null, Validators.required],
            'password' : [null, Validators.required],
        });
    }

    signIn() {
        const data = this.signInForm.value;
        this.http.post('/api/v1/sign-in', data)
            .subscribe((response: Response) => {
                localStorage.setItem('sessionId', response.json()['sessionid']);
                localStorage.setItem('isSignIn', 'true');
                this.router.navigate(['/dashboard']);
            }, (error) => {
                this.errorMessage = 'Username or password is wrong';
                setTimeout(() => this.errorMessage = null, 20000);
            });
    }

}
