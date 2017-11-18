import { Component, OnInit } from '@angular/core';
import { routerTransition } from '../../../../router.animations';
import { Http, Request, Response, RequestOptions } from '@angular/http';
import { Router, ActivatedRoute } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AlertService } from '../../../alert/alert.service';
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
    public isCreated: Boolean = false;

    public editorConfig = {
        imageUploadURL: '/api/v1/admin/upload-image',
        imageUploadMethod: 'POST',
        imageMaxSize: 30 * 1024 * 1024,
        imageAllowedTypes: ['jpeg', 'jpg', 'png'],
        placeholder: 'Page text',
        // events : {
        //     'froalaEditor.image.error' : function(e, editor, error, response) {
        //         this.alertService.warn('Oops! Uploading image is wrong');
        //     },
        // }
    };

    constructor(private fb: FormBuilder,
                private http: Http,
                private router: Router,
                private route: ActivatedRoute,
                private alertService: AlertService) {
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
            'content' : [
                null,
                Validators.required
            ],
        });

        this.route.params.subscribe(params => {
            console.log(params['id']);
            if (params['id'] === 'create') {
                this.flatpageForm.controls['title'].valueChanges.subscribe(
                    (title) => {
                        const slug = this.slugify(title);
                        this.flatpageForm.patchValue({slug});
                    }
                );
                this.isCreated = true;
                return ;
            }

            this.http.get(`/api/v1/admin/flatpage/${params['id']}/`)
                .subscribe((response: Response) => {
                    const data = response.json();
                    this.flatpageForm.reset(data);
                    setTimeout(() => $('.fr-wrapper > div > a').remove(), 1000);
                }, (error) => {
                    this.alertService.warn('Oops! Something is wrong');
                });
        });
    }

    private slugify(text: String): String {
        let slug = text.toLowerCase().trim();
        slug = slug.replace(/[^a-z0-9\s-]/g, ' ');
        slug = slug.replace(/[\s-]+/g, '-');
        return slug;
    }

    ngOnInit() {
        setTimeout(() => $('.fr-wrapper > div > a').remove(), 1000);
    }

    public submit(): void {
        this.route.params.subscribe(params => {
            const options = new RequestOptions();
            options.body = this.flatpageForm.value;
            options.responseType = 1;
            if (this.isCreated) {
                options.url = '/api/v1/admin/flatpage/';
                options.method = 'post';
            }
            else {
                options.url = `/api/v1/admin/flatpage/${params['id']}/`;
                options.method = 'patch';
            }
            this.http.request(new Request(options))
                .subscribe((response: Response) => {
                    let message = '';
                    if (this.isCreated) {
                        message = 'Page was created';
                    }
                    else {
                        message = 'Page was saved';
                    }
                    this.alertService.success(message);

                    if (this.isCreated) {
                        const data = response.json();
                        this.router.navigate(['/flatpage/']);
                    }
                }, (response: Response) => {
                    const errors = response.json();
                    let message = '';
                    if (response.status === 400 && 'slug' in errors) {
                        message = 'This slug is not unique. Rename, please';
                    }
                    else {
                        if (this.isCreated) {
                            message = 'Oops! Something is wrong at creating the new page';
                        }
                        else {
                            message = 'Oops! Something is wrong at updating the page';
                        }
                    }
                    this.alertService.warn(message);
                });
        });
    }
}
