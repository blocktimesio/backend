import { Http, Response } from '@angular/http';
import { Component, OnInit } from '@angular/core';
import {routerTransition} from '../../../../router.animations';

@Component({
    moduleId: module.id,
    selector: 'app-flatpage-list',
    templateUrl: 'flatpage-list.component.html',
    styleUrls: ['flatpage-list.component.scss'],
    animations: [routerTransition()]
})
export class FlatpageListComponent implements OnInit {
    public flatpageList: Array<any> = [];

    constructor(private http: Http) {
        this.http.get('/api/v1/admin/flatpage')
            .subscribe((response: Response) => {
                const data = response.json();
                this.flatpageList = data['results'];
            });
    }

    ngOnInit() {
    }

}
