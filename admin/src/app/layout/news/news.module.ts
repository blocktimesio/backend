import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { NewsComponent } from './news.component';
import { NewsRoutingModule } from './news-routing.module';
import { PageHeaderModule } from './../../shared';
import { NgbAlertConfig, NgbPaginationConfig, NgbModule} from '@ng-bootstrap/ng-bootstrap';

@NgModule({
    imports: [
        CommonModule,
        NewsRoutingModule,
        PageHeaderModule,
        NgbModule,
    ],
    declarations: [NewsComponent],
    providers: [NgbAlertConfig, NgbPaginationConfig]
})
export class NewsModule { }
