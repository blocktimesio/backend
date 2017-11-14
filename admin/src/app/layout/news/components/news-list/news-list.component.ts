import { Component } from '@angular/core';
import { routerTransition } from '../../../../router.animations';
import { Http, Response } from '@angular/http';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
    moduleId: module.id,
    selector: 'app-tables',
    templateUrl: 'news-list.component.html',
    styleUrls: ['news-list.component.scss'],
    animations: [routerTransition()]
})
export class NewsListComponent {
    public newsList: Array<any> = [];
    public domainsList: Array<any> = [];

    public filterForm: FormGroup;
    public rankConfigForm: FormGroup;
    public isRankFormCollapsed: Boolean = false;
    public isNewsCardsCollapsed: Boolean = false;

    public pageSize: Number = 10;
    public totalCount: Number = 0;
    public currentPage: Number = 1;

    constructor(private http: Http, private fb: FormBuilder) {
        this.filterForm = fb.group({
            'domains' : [null, ],
        });

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

        const isRankFormCollapsed = localStorage.getItem('isRankFormCollapsed');
        if (isRankFormCollapsed && isRankFormCollapsed === '1') {
            this.isRankFormCollapsed = true;
        }

        const isNewsCardsCollapsed = localStorage.getItem('isNewsCardsCollapsed');
        if (isNewsCardsCollapsed && isNewsCardsCollapsed === '1') {
            this.isNewsCardsCollapsed = true;
        }
        this.newsList.forEach(function(news) {
            news.isCollapsed = !this.isNewsCardsCollapsed;
        });

        this.loadDomains();
    }

    public changePage(selectedPage: number): void {
        this.currentPage = selectedPage;
        this.loadNews();
    }

    public submitFilterForm(): void {
        this.currentPage = 1;
        this.loadNews();
    }

    public submitRankConfig(): void {
        const data = this.rankConfigForm.value;
        this.http.post('/api/v1/admin/config/rank', data)
            .subscribe((response: Response) => this.loadNews());
    }

    private loadNews(): void {
        // /api/v1/news/?limit=10&offset=50
        let offset = 0;
        if (this.currentPage > 1) {
            offset = Number(this.pageSize) * Number(this.currentPage);
        }

        let url = `/api/v1/admin/news?limit=${this.pageSize}&offset=${offset}`;
        if (this.filterForm.value['domains']) {
            const domains = this.filterForm.value['domains'].join();
            url += `&domain__id__in=${domains}`;
        }
        this.http.get(url)
            .subscribe((response: Response) => {
                const data = response.json();
                this.newsList = data['results'];
                this.totalCount = Number(data['count']) - Number(this.pageSize);
            });
    }

    private loadRankConfigForm() {
        this.http.get('/api/v1/admin/config/rank')
            .subscribe((response: Response) => {
                const data = response.json();
                this.rankConfigForm.reset(data);
            });
    }

    public collapseRankForm(): void {
        this.isRankFormCollapsed = !this.isRankFormCollapsed;

        if (this.isRankFormCollapsed) {
            localStorage.setItem('isRankFormCollapsed', '1');
        }
        else {
            localStorage.setItem('isRankFormCollapsed', '0');
        }
    }

    public collapseNewsCards(): void {
        this.isNewsCardsCollapsed = !this.isNewsCardsCollapsed;

        this.newsList.forEach(function(news) {
            news.isCollapsed = !news.isCollapsed;
        });

        if (this.isNewsCardsCollapsed) {
            localStorage.setItem('isNewsCardsCollapsed', '1');
        }
        else {
            localStorage.setItem('isNewsCardsCollapsed', '0');
        }
    }

    private loadDomains(): void {
        this.http.get('/api/v1/admin/domain')
            .subscribe((response: Response) => {
                const data = response.json();
                this.domainsList = data.results;
            });
    }
}
