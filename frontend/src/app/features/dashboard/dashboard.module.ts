import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

// COMPONENTS
import { DashboardStartComponent } from './pages/dashboard-start/dashboard-start.component';

// SERVICES

// MODULES
import { DashboardRoutingModule } from './dashboard-routing.module';

@NgModule({
  declarations: [
    DashboardStartComponent
  ],
  imports: [
    DashboardRoutingModule,
    CommonModule
  ],
  exports: [

  ],
  providers: []
})
export class DashboardModule {}
