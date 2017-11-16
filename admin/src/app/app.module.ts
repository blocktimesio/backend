import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CookieXSRFStrategy, HttpModule, XSRFStrategy } from '@angular/http';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AuthGuard } from './shared';
import { FlatpageComponent } from './layout/flatpage/flatpage.component';

@NgModule({
    declarations: [
        AppComponent,
        FlatpageComponent,
    ],
    imports: [
        BrowserModule,
        BrowserAnimationsModule,
        FormsModule,
        HttpModule,
        AppRoutingModule,
    ],
    providers: [
        AuthGuard,
        {
            provide: XSRFStrategy,
            useValue: new CookieXSRFStrategy('csrftoken', 'X-CSRFToken')
        }
    ],
    bootstrap: [AppComponent]
})
export class AppModule {}
