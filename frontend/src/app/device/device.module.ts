import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { DeviceComponent } from './device.component';
import { DeviceListComponent } from './device-list/device-list.component';

import { DeviceRoutingModule } from './device-routing.module';

@NgModule({
  declarations: [
    DeviceComponent,
    DeviceListComponent
  ],
  imports: [
    DeviceRoutingModule,
    CommonModule
  ],
  exports: [
    
  ]
})
export class DeviceModule {}
