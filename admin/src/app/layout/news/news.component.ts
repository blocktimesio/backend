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

    public pageSize: Number = 10;
    public totalCount: Number = 0;
    public currentPage: Number = 1;

    constructor(private http: Http) {}

    public changePage(selectedPage: number): void {
        this.currentPage = selectedPage;
        this.loadNews();
    }

    ngOnInit() {
        this.loadNews();
    }

    private loadNews(): void {
        // /api/v1/news/?limit=10&offset=50
        const url = `/api/v1/admin/news?limit=${this.pageSize}&offset=${this.pageSize as number * this.currentPage as number}`;
        this.http.get(url)
            .subscribe((response: Response) => {
                const data = response.json();
                this.newsList = data['results'];
                this.totalCount = data['count'] - 1;
            });
    }
}
