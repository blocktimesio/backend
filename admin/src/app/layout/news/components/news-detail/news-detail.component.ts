import { Component, OnInit } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Router, ActivatedRoute } from '@angular/router';
import { routerTransition } from '../../../../router.animations';
import * as $ from 'jquery/dist/jquery.min.js';

@Component({
    moduleId: module.id,
    selector: 'app-news-detail',
    templateUrl: 'news-detail.component.html',
    styleUrls: ['news-detail.component.scss'],
    animations: [routerTransition()]
})
export class NewsDetailComponent implements OnInit {
    public news: any = null;
    public alerts: Array<any> = [];

    constructor(private http: Http,
                private router: Router,
                private route: ActivatedRoute) {
        this.route.params.subscribe(params => {
            this.http.get(`/api/v1/admin/news/${params['id']}`)
                .subscribe((data: Response) => {
                    this.news = data.json();
                }, (error) => {
                    this.router.navigate(['/not-found']);
                });
        });
    }

    ngOnInit() {
        setTimeout(() => $('.fr-wrapper > div > a').remove(), 1000);
    }

    public editorEdit = {
        imageUploadURL: '/api/v1/admin/upload-image',
        imageUploadMethod: 'POST',
        imageMaxSize: 30 * 1024 * 1024,
        imageAllowedTypes: ['jpeg', 'jpg', 'png'],
    };

    public saveNews(): void {
        this.route.params.subscribe(params => {
            const data = {text: this.news.text};
            this.http.patch(`/api/v1/admin/news/${params['id']}/`, data)
                .subscribe((data: Response) => {
                    this.alerts.push({
                        type: 'success',
                        message: 'Saving news was succeed',
                    });
                }, (error) => {
                    this.alerts.push({
                        type: 'danger',
                        message: 'Saving news was failure',
                    });
                });
        });
    }

    public removeNews(): void {
        this.route.params.subscribe(params => {
            this.http.delete(`/api/v1/admin/news/${params['id']}/`)
                .subscribe((data: Response) => {
                    this.router.navigate(['/news']);
                }, (error) => {
                    this.alerts.push({
                        type: 'danger',
                        message: 'Removing news was failure',
                    });
                });
        });
    }

    public closeAlert(alert: any) {
        const index: number = this.alerts.indexOf(alert);
        this.alerts.splice(index, 1);
    }
}
