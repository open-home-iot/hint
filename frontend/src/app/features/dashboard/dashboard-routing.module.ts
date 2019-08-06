import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { DashboardStartComponent } from './pages/dashboard-start/dashboard-start.component';

const routes: Routes = [
  { path: 'dashboard', component: DashboardStartComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class DashboardRoutingModule {}
