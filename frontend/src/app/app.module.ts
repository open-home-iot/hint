import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AuthComponent } from './auth/auth.component';
import { AreaComponent } from './area/area.component';
import { HumeComponent } from './hume/hume.component';
import { DeviceComponent } from './device/device.component';
import { EventComponent } from './event/event.component';
import { HttpComponent } from './http/http.component';
import { HeaderComponent } from './header/header.component';
import { StartComponent } from './start/start.component';

@NgModule({
  declarations: [
    AppComponent,
    AuthComponent,
    AreaComponent,
    HumeComponent,
    DeviceComponent,
    EventComponent,
    HttpComponent,
    HeaderComponent,
    StartComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
