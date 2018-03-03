import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AuthComponent } from './auth/auth.component';
import { HomeComponent } from './home/home.component';

import { AuthGuardService } from './auth-guard.service';
import { EventListenerService } from "./events/event-listener.service";
import { EventHandlerService } from "./events/event-handler.service";
import { SurveillanceComponent } from './surveillance/surveillance.component';
import { PictureComponent } from './surveillance/picture/picture.component';


@NgModule({
  declarations: [
    AppComponent,
    AuthComponent,
    HomeComponent,
    SurveillanceComponent,
    PictureComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    // The module imported will be the exported RouterModule from AppRoutingModule
    AppRoutingModule
  ],
  // Guards and services go here! Guards are essentially services.
  providers: [
    AuthGuardService,
    EventListenerService,
    EventHandlerService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
