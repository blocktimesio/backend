import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { NewsComponent } from './news.component';
import { NewsRoutingModule } from './news-routing.module';
import { PageHeaderModule } from './../../shared';

@NgModule({
    imports: [
        CommonModule,
        NewsRoutingModule,
        PageHeaderModule
    ],
    declarations: [NewsComponent]
})
export class NewsModule { }
