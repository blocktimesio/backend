import { Injectable } from '@angular/core';
import { Subject } from 'rxjs/Subject';
import { Observable } from 'rxjs/Observable';
import { Alert, AlertType } from './alert.model';

@Injectable()
export class AlertService {
    private subject = new Subject<Alert>();

    public getAlert(): Observable<any> {
        return this.subject.asObservable();
    }

    public success(message: string) {
        this.alert(AlertType.Success, message);
    }

    public error(message: string) {
        this.alert(AlertType.Error, message);
    }

    public info(message: string) {
        this.alert(AlertType.Info, message);
    }

    public warn(message: string) {
        this.alert(AlertType.Warning, message);
    }

    public alert(type: AlertType, message: string) {
        this.subject.next(<Alert>{ type: type, message: message });
    }

    public clear() {
        this.subject.next();
    }
}
