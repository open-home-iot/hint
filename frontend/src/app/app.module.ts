import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

// ROUTING
import { AppRoutingModule } from './app-routing.module';

// CORE COMPONENTS AND SERVICES
import { AppComponent } from './app.component';
import { AuthComponent } from './core/auth/auth.component';
import { EventComponent } from './core/event/event.component';
import { HeaderComponent } from './core/header/header.component';
import { StartComponent } from './core/start/start.component';
import { PageNotFoundComponent } from './core/page-not-found/page-not-found.component';

// FEATURE MODULES
import { HomeModule } from './home/home.module';
import { HumeModule } from './hume/hume.module';
import { DeviceModule } from './device/device.module';

@NgModule({
  declarations: [
    AppComponent,
    AuthComponent,
    EventComponent,

    HeaderComponent,
    StartComponent,
    PageNotFoundComponent
  ],
  imports: [
    BrowserModule,

    HomeModule,
    HumeModule,
    DeviceModule,

    // NEEDS TO DECLARED LAST OR CATCH ALL ROUTE REGISTERS BEFORE CHILD ROUTES!
    AppRoutingModule
    // NEEDS TO DECLARED LAST OR CATCH ALL ROUTE REGISTERS BEFORE CHILD ROUTES!
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
