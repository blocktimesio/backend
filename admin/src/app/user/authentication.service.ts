import { Injectable } from '@angular/core';
import { Http, Headers, Response } from '@angular/http';
import { Observable } from 'rxjs';
import 'rxjs/add/operator/map'

@Injectable()
export class AuthenticationService {
    public token: string;

    constructor(private http: Http) {
        const currentUser = JSON.parse(
            localStorage.getItem('currentUser')
        );
        this.token = currentUser && currentUser.token;
    }

    login(username: string, password: string): Observable<boolean> {
        const data = JSON.stringify({username: username, password: password});
        return this.http.post('/api/v1/admin/api-token-auth', data)
            .map((response: Response) => {
                const token = response.json() && response.json().token;
                if (token) {
                    this.token = token;
                    localStorage.setItem('currentUser', JSON.stringify({username: username, token: token}));

                    return true;
                } else {
                    return false;
                }
            });
    }

    logout(): void {
        this.token = null;
        localStorage.removeItem('currentUser');
    }
}
