import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

// ROUTING
import { AppRoutingModule } from './app-routing.module';

// COMPONENTS & SERVICES
import { AppComponent } from './app.component';

import { AuthComponent } from './core/auth/auth.component';

import { EventComponent } from './core/event/event.component';

import { HomeComponent } from './home/home.component';
import { HomeListComponent } from './home/home-list/home-list.component';

import { HumeComponent } from './hume/hume.component';
import { HumeListComponent } from './hume/hume-list/hume-list.component';

import { DeviceModule } from './device/device.module';

import { HeaderComponent } from './core/header/header.component';

import { StartComponent } from './core/start/start.component';

import { PageNotFoundComponent } from './core/page-not-found/page-not-found.component';

@NgModule({
  declarations: [
    AppComponent,

    AuthComponent,

    EventComponent,

    HomeComponent,
    HomeListComponent,

    HumeComponent,
    HumeListComponent,

    HeaderComponent,

    StartComponent,

    PageNotFoundComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    DeviceModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
