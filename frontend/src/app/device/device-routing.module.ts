import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { DeviceComponent } from './device.component';

const routes: Routes = [
  { path: 'device', component: DeviceComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class DeviceRoutingModule {}
