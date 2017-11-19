import { Component } from '@angular/core';
import { routerTransition } from '../../../../router.animations';
import { Http, Response } from '@angular/http';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AlertService } from '../../../../shared';

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

    constructor(private http: Http,
                private fb: FormBuilder,
                private alertService: AlertService) {
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

    public submitFilterForm(): void {
        this.loadNews();
    }

    public submitRankConfig(): void {
        const data = this.rankConfigForm.value;
        this.http.post('/api/v1/admin/config/rank', data)
            .subscribe((response: Response) => this.loadNews());
    }

    private loadNews(): void {
        let url = '/api/v1/admin/news';
        if (this.filterForm.value['domains']) {
            const domains = this.filterForm.value['domains'].join();
            url += `?domain__id__in=${domains}`;
        }
        this.http.get(url)
            .subscribe((response: Response) => {
                this.newsList = response.json();
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

    public updateDomain(domain: any): void {
        const url = `/api/v1/admin/domain/${domain.id}/`
        this.http.patch(url, {coef: domain.coef})
            .subscribe((response: Response) => {
                const message = `Coef for domain "${domain.name}" was updated`;
                this.alertService.success(message);
                this.loadNews();
            }, (error) => {
                const message = `Oops! Something is wrong. Coef for domain "${domain.name}" was not updated`;
                this.alertService.warn(message);
            });
    }
}
