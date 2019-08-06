import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { DeviceOverviewComponent } from './pages/device-overview/device-overview.component';

const routes: Routes = [
  { path: 'device', component: DeviceOverviewComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class DeviceRoutingModule {}
