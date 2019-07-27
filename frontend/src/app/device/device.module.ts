import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

// COMPONENTS
import { DeviceComponent } from './device.component';
import { DeviceListComponent } from './device-list/device-list.component';

// SERVICES
import { DeviceService } from './device.service';

// MODULES
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

  ],
  providers: [DeviceService]
})
export class DeviceModule {}
