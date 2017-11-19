import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NgbModule, NgbDropdownModule, NgbAlertConfig } from '@ng-bootstrap/ng-bootstrap';
import { LayoutRoutingModule } from './layout-routing.module';
import { LayoutComponent } from './layout.component';
import { HeaderComponent, SidebarComponent, AlertService } from '../shared';
import { FlatpageComponent } from './flatpage/flatpage.component';

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
        FlatpageComponent,
    ],
    providers: [
        NgbAlertConfig,
        AlertService,
    ]
})
export class LayoutModule { }
