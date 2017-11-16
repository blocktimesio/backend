import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { FlatpageListComponent } from './components/flatpage-list/flatpage-list.component';
import { FlatpageDetailComponent } from './components/flatpage-detail/flatpage-detail.component';

const routes: Routes = [
    { path: '', component: FlatpageListComponent },
    { path: ':slug', component: FlatpageDetailComponent },
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class NewsRoutingModule { }
