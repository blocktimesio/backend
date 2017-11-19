import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Alert, AlertType, AlertService } from '../shared';

@Component({
    selector: 'app-layout',
    templateUrl: './layout.component.html',
    styleUrls: ['./layout.component.scss']
})
export class LayoutComponent implements OnInit {
    public alerts: Alert[] = [];

    constructor(public router: Router, private alertService: AlertService) { }

    ngOnInit() {
        if (this.router.url === '/') {
            this.router.navigate(['/dashboard']);
        }

        this.alertService.getAlert().subscribe((alert: Alert) => {
            if (!alert) {
                this.alerts = [];
            }
            else {
                this.alerts.push(alert);
                setTimeout(() => this.removeAlert(alert), 4000);
            }
        });
    }

    public removeAlert(alert: Alert) {
        this.alerts = this.alerts.filter(x => x !== alert);
    }

    public geType(alert: Alert): String {
        if (!alert) {
            return '';
        }

        switch (alert.type) {
            case AlertType.Success:
                return 'success';
            case AlertType.Error:
                return 'danger';
            case AlertType.Info:
                return 'info';
            case AlertType.Warning:
                return 'warning';
        }
        return '';
    }
}
