import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

// ROUTING
import { AppRoutingModule } from './app-routing.module';

// COMPONENTS & SERVICES
import { AppComponent } from './app.component';

import { AuthComponent } from './auth/auth.component';

import { EventComponent } from './event/event.component';

import { HomeComponent } from './home/home.component';
import { HomeListComponent } from './home/home-list/home-list.component';

import { HumeComponent } from './hume/hume.component';
import { HumeListComponent } from './hume/hume-list/hume-list.component';

import { DeviceComponent } from './device/device.component';
import { DeviceListComponent } from './device/device-list/device-list.component';

import { HeaderComponent } from './header/header.component';

import { StartComponent } from './start/start.component';

import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

@NgModule({
  declarations: [
    AppComponent,

    AuthComponent,

    EventComponent,

    HomeComponent,
    HomeListComponent,

    HumeComponent,
    HumeListComponent,

    DeviceComponent,
    DeviceListComponent,

    HeaderComponent,

    StartComponent,

    PageNotFoundComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
