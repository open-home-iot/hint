import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

// COMPONENTS
import { HomeDevicesComponent } from './home-devices/home-devices.component';
import { RoomDevicesComponent } from './room-devices/room-devices.component';

// PAGES

// SERVICES
import { DeviceService } from './device.service';

// MODULES
import { DeviceRoutingModule } from './device-routing.module';
import { DeviceListComponent } from './device-list/device-list.component';
import { DeviceDetailComponent } from './device-detail/device-detail.component';

@NgModule({
  declarations: [
    HomeDevicesComponent,
    RoomDevicesComponent,
    DeviceListComponent,
    DeviceDetailComponent
  ],
  imports: [
    DeviceRoutingModule,
    CommonModule
  ],
  exports: [
    HomeDevicesComponent,
    RoomDevicesComponent
  ],
  providers: [DeviceService]
})
export class DeviceModule {}
