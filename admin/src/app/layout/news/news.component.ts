import { Component, OnInit } from '@angular/core';
import { routerTransition } from '../../router.animations';

@Component({
    selector: 'app-tables',
    templateUrl: './news.component.html',
    styleUrls: ['./news.component.scss'],
    animations: [routerTransition()]
})
export class NewsComponent implements OnInit {
    constructor() { }

    ngOnInit() { }
}
