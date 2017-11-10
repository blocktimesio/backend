import { Component, OnInit } from '@angular/core';
import { routerTransition } from '../../router.animations';
import { Http, Response } from '@angular/http';

@Component({
    selector: 'app-tables',
    templateUrl: './news.component.html',
    styleUrls: ['./news.component.scss'],
    animations: [routerTransition()]
})
export class NewsComponent implements OnInit {
    public newsList: Array<any> = [];

    constructor(private http: Http) {}

    ngOnInit() {
        this.http.get('/api/v1/news')
            .subscribe((data: Response) => {
                this.newsList = data.json().results;
            });
    }
}
