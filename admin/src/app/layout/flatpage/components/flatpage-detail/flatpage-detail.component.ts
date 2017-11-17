import { Component, OnInit } from '@angular/core';
import { routerTransition } from '../../../../router.animations';
import { Http, Response } from '@angular/http';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import * as $ from 'jquery/dist/jquery.min.js';

@Component({
    moduleId: module.id,
    selector: 'app-flatpage-detail',
    templateUrl: 'flatpage-detail.component.html',
    styleUrls: ['flatpage-detail.component.scss'],
    animations: [routerTransition()]
})
export class FlatpageDetailComponent implements OnInit {
    public flatpageForm: FormGroup;

    public editorConfig = {
        imageUploadURL: '/api/v1/admin/upload-image',
        imageUploadMethod: 'POST',
        imageMaxSize: 30 * 1024 * 1024,
        imageAllowedTypes: ['jpeg', 'jpg', 'png'],
    };

    constructor(private fb: FormBuilder,
                private http: Http,
                private router: Router,
                private route: ActivatedRoute) {
        this.flatpageForm = fb.group({
            'title' : [
                null,
                Validators.compose([
                    Validators.required,
                    Validators.maxLength(128)
                ])
            ],
            'slug' : [
                null,
                Validators.compose([
                    Validators.required,
                    Validators.maxLength(128),
                    Validators.pattern('[-0-9a-z]+')
                ])
            ],
            'is_show' : [null],
            'content' : [
                null,
                Validators.compose([Validators.required])
            ],
        });

        this.route.params.subscribe(params => {
            this.http.get(`/api/v1/admin/flatpage/${params['slug']}/`)
                .subscribe((response: Response) => {
                    const data = response.json();
                    this.flatpageForm.reset(data);
                });
        });
    }

    ngOnInit() {
        setTimeout(() => $('.fr-wrapper > div > a').remove(), 1000);
    }

    public submit(): void {
        this.route.params.subscribe(params => {
            const sendData = this.flatpageForm.value;
            this.http.patch(`/api/v1/admin/flatpage/${params['slug']}/`, sendData)
                .subscribe((response: Response) => {
                    const data = response.json();
                    this.flatpageForm.reset(data);
                });
        });
    }
}
