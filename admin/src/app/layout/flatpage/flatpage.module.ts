import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { NewsRoutingModule } from './flatpage-routing.module';
import { PageHeaderModule } from './../../shared';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgbAlertConfig, NgbPaginationConfig, NgbModule} from '@ng-bootstrap/ng-bootstrap';
import { FlatpageListComponent } from './components/flatpage-list/flatpage-list.component';
import { FlatpageDetailComponent } from './components/flatpage-detail/flatpage-detail.component';
import { FroalaEditorModule, FroalaViewModule } from 'angular-froala-wysiwyg';
import { UiSwitchModule } from 'ngx-ui-switch';

@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        ReactiveFormsModule,
        NewsRoutingModule,
        PageHeaderModule,
        NgbModule,
        UiSwitchModule,
        FroalaEditorModule.forRoot(),
        FroalaViewModule.forRoot(),
    ],
    declarations: [
        FlatpageListComponent,
        FlatpageDetailComponent,
    ],
    providers: [NgbAlertConfig, NgbPaginationConfig]
})
export class FlatpageModule { }
