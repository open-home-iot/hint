import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

// COMPONENTS

// PAGES

// SERVICES
import { DeviceService } from './device.service';

// MODULES
import { DeviceRoutingModule } from './device-routing.module';

@NgModule({
  declarations: [
  ],
  imports: [
    DeviceRoutingModule,
    CommonModule
  ],
  exports: [

  ],
  providers: [DeviceService]
})
export class DeviceModule {}
