import { Http, Response } from '@angular/http';
import { Component, OnInit, Input } from '@angular/core';
import { routerTransition } from '../../../../router.animations';
import { AlertService } from '../../../../shared';
import { NgbModal, NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';

@Component({
    moduleId: module.id,
    selector: 'app-flatpage-list2',
    template: `
        <div class="modal-header">
            <h4 class="modal-title">Remove page</h4>
            <button type="button" class="close" aria-label="Close" (click)="activeModal.dismiss('Cross click')">
                <span aria-hidden="true">&times;</span>
            </button>
        </div>
        <div class="modal-body">
            <p>Are you sure to delete page "{{ page.title }}"?</p>
        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-success" (click)="activeModal.close('Close click')">No</button>
            <button type="button" class="btn btn-danger" (click)="confirmRemove()">Yes</button>
        </div>
    `,
})
export class RemoveFlatpageModalComponent {
    @Input() page;
    @Input() callback;

    constructor(public activeModal: NgbActiveModal) {}

    public confirmRemove(): void {
        this.callback();
        this.activeModal.close('Close click');
    }
}

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
                private modalService: NgbModal,
                private alertService: AlertService) {
        this.http.get('/api/v1/admin/flatpage')
            .subscribe((response: Response) => {
                this.flatpageList = response.json();
            });
    }

    public removeFlatpage(page: any) {
        const modalRef = this.modalService.open(RemoveFlatpageModalComponent);
        modalRef.componentInstance.page = page;
        modalRef.componentInstance.callback = () => {
            this.http.delete(`/api/v1/admin/flatpage/${page.id}/`)
                .subscribe((response: Response) => {
                    this.flatpageList = this.flatpageList.filter(p => p !== page);
                    this.alertService.success(`Page "${page.title}" was removed`);
                });
        };
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
