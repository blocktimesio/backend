import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { NewsRoutingModule } from './news-routing.module';
import { PageHeaderModule } from './../../shared';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgbAlertConfig, NgbPaginationConfig, NgbModule} from '@ng-bootstrap/ng-bootstrap';
import { NewsListComponent } from './components/news-list/news-list.component';
import { NewsDetailComponent } from './components/news-detail/news-detail.component';
import { FroalaEditorModule, FroalaViewModule } from 'angular-froala-wysiwyg';

@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        ReactiveFormsModule,
        NewsRoutingModule,
        PageHeaderModule,
        NgbModule,
        FroalaEditorModule.forRoot(),
        FroalaViewModule.forRoot(),
    ],
    declarations: [
        NewsListComponent,
        NewsDetailComponent,
    ],
    providers: [NgbAlertConfig, NgbPaginationConfig]
})
export class NewsModule { }
