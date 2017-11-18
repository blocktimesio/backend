import { Http, Response } from '@angular/http';
import { Component, OnInit } from '@angular/core';
import { routerTransition } from '../../../../router.animations';
import { AlertService } from '../../../alert/alert.service';

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

}
