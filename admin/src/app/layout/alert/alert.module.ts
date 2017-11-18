import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgbModule, NgbAlertConfig } from '@ng-bootstrap/ng-bootstrap';
import { AlertComponent } from './alert.component';

@NgModule({
    imports: [
        NgbModule,
        CommonModule,
    ],
    declarations: [
        AlertComponent,
    ],
    providers: [
        NgbAlertConfig,
    ]
})
export class AlertModule { }
