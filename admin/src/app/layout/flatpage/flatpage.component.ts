import { Component, OnInit, ViewEncapsulation } from '@angular/core';

@Component({
    moduleId: module.id,
    selector: 'app-flatpage',
    templateUrl: 'flatpage.component.html',
    styleUrls: ['flatpage.component.scss'],
    encapsulation: ViewEncapsulation.None
})
export class FlatpageComponent implements OnInit {

    constructor() { }

    ngOnInit() {
    }

}
