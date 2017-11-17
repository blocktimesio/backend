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
            'slug' : [
                null,
                Validators.required,
                // Validators.maxLength(128),
                // Validators.pattern('[-a-z0-9]+')
            ],
            'title' : [
                null,
                Validators.required,
                // Validators.maxLength(128)
            ],
            'is_show' : [null, Validators.required],
            'content' : [null, Validators.required],
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
    }

    public submit(): void {
        console.log(123);
    }
}
