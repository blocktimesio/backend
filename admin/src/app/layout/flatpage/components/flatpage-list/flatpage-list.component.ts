import { Http, Response } from '@angular/http';
import { Component, OnInit } from '@angular/core';
import { routerTransition } from '../../../../router.animations';
import { AlertService } from '../../../../shared';

@Component({
    moduleId: module.id,
    selector: 'app-flatpage-list',
    templateUrl: 'flatpage-list.component.html',
    styleUrls: ['flatpage-list.component.scss'],
    animations: [routerTransition()]
})
export class FlatpageListComponent implements OnInit {
    public flatpageList: Array<any> = [];

    constructor(private http: Http,
                private alertService: AlertService) {
        this.http.get('/api/v1/admin/flatpage')
            .subscribe((response: Response) => {
                this.flatpageList = response.json();
            });
    }

    public removeFlatpage(page: any) {
        this.http.delete(`/api/v1/admin/flatpage/${page.id}/`)
            .subscribe((response: Response) => {
                this.flatpageList = this.flatpageList.filter(p => p !== page);
            });
    }

    ngOnInit() {
    }

    public setEnable(page: any, isShow: Boolean): void {
        const url = `/api/v1/admin/flatpage/${page['id']}/`;
        this.http.patch(url, {is_show: isShow})
            .subscribe((response: Response) => {
                this.alertService.success(`Set is show value to "${isShow}" for page "${page.title}"`);
            });
    }
}
