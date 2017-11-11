import { Component, OnInit } from '@angular/core';
import { routerTransition } from '../../router.animations';
import { Http, Response } from '@angular/http';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
    selector: 'app-tables',
    templateUrl: './news.component.html',
    styleUrls: ['./news.component.scss'],
    animations: [routerTransition()]
})
export class NewsComponent {
    public newsList: Array<any> = [];

    public rankConfigForm: FormGroup;

    public pageSize: Number = 10;
    public totalCount: Number = 0;
    public currentPage: Number = 1;

    constructor(private http: Http, private fb: FormBuilder) {
        this.rankConfigForm = fb.group({
            'fb_shares' : [null, Validators.required],
            'linkedin_shares' : [null, Validators.required],
            'reddit_up' : [null, Validators.required],
            'twitter_shares' : [null, Validators.required],
            'views' : [null, Validators.required],
            'comments' : [null, Validators.required],
            'date_elapsed_seconds' : [null, Validators.required],
            'date_coef' : [null, Validators.required],
        });
        this.loadRankConfigForm();
        this.loadNews();
    }

    public changePage(selectedPage: number): void {
        this.currentPage = selectedPage;
        this.loadNews();
    }

    public submitRankConfig(): void {
        const data = this.rankConfigForm.value;
        this.http.post('/api/v1/admin/config/rank', data)
            .subscribe((response: Response) => this.loadNews());
    }

    private loadNews(): void {
        // /api/v1/news/?limit=10&offset=50
        const url = `/api/v1/admin/news?limit=${this.pageSize}&offset=${this.pageSize as number}`;
        this.http.get(url)
            .subscribe((response: Response) => {
                const data = response.json();
                this.newsList = data['results'];
                this.totalCount = data['count'] - 1;
            });
    }

    private loadRankConfigForm() {
        this.http.get('/api/v1/admin/config/rank')
            .subscribe((response: Response) => {
                const data = response.json();
                this.rankConfigForm.reset(data);
            });
    }
}
