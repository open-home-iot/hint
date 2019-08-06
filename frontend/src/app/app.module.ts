import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

// ROUTING
import { AppRoutingModule } from './app-routing.module';

// CORE COMPONENTS, CORE SERVICES ARE PROVIDED IN ROOT IN THEIR RESPECTIVE TYPE-
// SCRIPT FILES.
import { AppComponent } from './app.component';
import { AuthComponent } from './core/auth/auth.component';
import { HeaderComponent } from './core/header/header.component';
import { FooterComponent } from './core/footer/footer.component';
import { StartComponent } from './core/start/start.component';
import { PageNotFoundComponent } from './core/page-not-found/page-not-found.component';

// FEATURE MODULES
import { HomeModule } from './features/home/home.module';
import { HumeModule } from './features/hume/hume.module';
import { DeviceModule } from './features/device/device.module';
import { DashboardModule } from './features/dashboard/dashboard.module';
import { StatisticsModule } from './features/statistics/statistics.module';
import { UserModule } from './features/user/user.module';
import { EventModule } from './features/event/event.module';

@NgModule({
  declarations: [
    AppComponent,
    AuthComponent,

    HeaderComponent,
    StartComponent,
    PageNotFoundComponent,
    FooterComponent
  ],
  imports: [
    BrowserModule,

    HomeModule,
    HumeModule,
    DeviceModule,
    DashboardModule,
    StatisticsModule,
    UserModule,
    EventModule,

    // NEEDS TO DECLARED LAST OR CATCH ALL ROUTE REGISTERS BEFORE CHILD ROUTES!
    AppRoutingModule
    // NEEDS TO DECLARED LAST OR CATCH ALL ROUTE REGISTERS BEFORE CHILD ROUTES!
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
