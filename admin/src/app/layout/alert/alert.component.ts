import { AlertService } from './alert.service';
import { Alert, AlertType } from './alert.model';
import { Component, OnInit } from '@angular/core';

@Component({
    moduleId: module.id,
    selector: 'app-alert',
    templateUrl: 'alert.component.html',
    styleUrls: ['alert.component.scss'],
})
export class AlertComponent implements OnInit {
    public alerts: Alert[] = [];

    constructor(private alertService: AlertService) { }

    ngOnInit() {
        this.alertService.getAlert().subscribe((alert: Alert) => {
            if (!alert) {
                this.alerts = [];
            }
            else {
                this.alerts.push(alert);
                setTimeout(() => this.removeAlert(alert), 5000);
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
