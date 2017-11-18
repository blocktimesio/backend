import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgbModule, NgbDropdownModule, NgbAlertConfig } from '@ng-bootstrap/ng-bootstrap';
import { LayoutRoutingModule } from './layout-routing.module';
import { LayoutComponent } from './layout.component';
import { HeaderComponent, SidebarComponent } from '../shared';
import { AlertService } from './alert/alert.service';
import { AlertComponent } from './alert/alert.component'

@NgModule({
    imports: [
        NgbModule,
        CommonModule,
        NgbDropdownModule.forRoot(),
        LayoutRoutingModule,
    ],
    declarations: [
        LayoutComponent,
        HeaderComponent,
        SidebarComponent,
        AlertComponent,
    ],
    providers: [
        NgbAlertConfig,
        AlertService,
    ]
})
export class LayoutModule { }
