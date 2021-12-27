import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';

// ROUTING
import { AppRoutingModule } from './app-routing.module';

// CORE COMPONENTS, CORE SERVICES ARE PROVIDED IN ROOT IN THEIR RESPECTIVE TYPE-
// SCRIPT FILES.
import { AppComponent } from './app.component';
import { AuthLoginComponent } from './core/auth/auth-login/auth-login.component';
import { AuthSignUpComponent } from './core/auth/auth-sign-up/auth-sign-up.component';
import { AuthLogoutComponent } from './core/auth/auth-logout/auth-logout.component';
import { HeaderComponent } from './core/header/header.component';
import { FooterComponent } from './core/footer/footer.component';
import { StartComponent } from './core/start/start.component';
import { PageNotFoundComponent } from './core/page-not-found/page-not-found.component';

// INTERCEPTORS
import { AuthRequestInterceptor } from './core/auth/auth.interceptor';

// FEATURE MODULES
import { HomeModule } from './features/home/home.module';
import { HumeModule } from './features/hume/hume.module';
import { DeviceModule } from './features/device/device.module';
import { UserModule } from './features/user/user.module';
import { EventModule } from './features/event/event.module';
import { IconComponent } from './core/icon/icon.component';


@NgModule({
  declarations: [
    AppComponent,

    HeaderComponent,
    StartComponent,
    PageNotFoundComponent,
    FooterComponent,
    AuthLoginComponent,
    AuthLogoutComponent,
    AuthSignUpComponent,
    IconComponent,
  ],
  imports: [
    // ANGULAR IMPORTS
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,

    // FEATURE MODULE IMPORTS
    HomeModule,
    HumeModule,
    DeviceModule,
    UserModule,
    EventModule,

    // CORE ROUTING MODULE, DO NOT REMOVE!
    // NEEDS TO DECLARED LAST OR CATCH ALL ROUTE REGISTERS BEFORE CHILD ROUTES!
    AppRoutingModule
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthRequestInterceptor,
      multi: true
    }
  ],
  exports: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
