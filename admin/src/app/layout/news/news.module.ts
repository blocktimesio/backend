import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { NewsListComponent } from './components/news-list/news-list.component';
import { NewsRoutingModule } from './news-routing.module';
import { PageHeaderModule } from './../../shared';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgbAlertConfig, NgbPaginationConfig, NgbModule} from '@ng-bootstrap/ng-bootstrap';

@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        ReactiveFormsModule,
        NewsRoutingModule,
        PageHeaderModule,
        NgbModule,
    ],
    declarations: [NewsListComponent],
    providers: [NgbAlertConfig, NgbPaginationConfig]
})
export class NewsModule { }
