import { Component } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Router, ActivatedRoute } from '@angular/router';
import { routerTransition } from '../../../../router.animations';

@Component({
    moduleId: module.id,
    selector: 'app-news-detail',
    templateUrl: 'news-detail.component.html',
    styleUrls: ['news-detail.component.scss'],
    animations: [routerTransition()]
})
export class NewsDetailComponent {
    public news: any = null;

    constructor(private http: Http,
                private router: Router,
                private route: ActivatedRoute) {
        this.route.params.subscribe(params => {
            this.http.get(`/api/v1/admin/news/${params['id']}`)
                .subscribe((data: Response) => {
                    this.news = data.json();
                    console.log(this.news);
                }, (error) => {
                    this.router.navigate(['/not-found']);
                });
        });
    }
}